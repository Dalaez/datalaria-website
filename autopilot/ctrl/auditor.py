"""
Core audit engine that interfaces with GitHub Copilot CLI.
Uses `gh copilot suggest` to evaluate content quality.
"""
import subprocess
import json
import re
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path

import yaml


@dataclass
class AuditResult:
    """Result of auditing a single platform's content."""
    platform: str
    content: str
    scores: dict[str, int] = field(default_factory=dict)
    total_score: float = 0.0
    max_score: float = 10.0
    status: str = "UNKNOWN"  # PASS, WARN, FAIL
    issues: list[str] = field(default_factory=list)
    suggestions: list[str] = field(default_factory=list)
    raw_response: str = ""
    
    @property
    def passed(self) -> bool:
        return self.status == "PASS"
    
    @property
    def normalized_score(self) -> float:
        """Returns score as 0-10 scale."""
        if self.max_score == 0:
            return 0
        return (self.total_score / self.max_score) * 10


@dataclass 
class AuditReport:
    """Complete audit report for all platforms."""
    results: list[AuditResult] = field(default_factory=list)
    overall_status: str = "UNKNOWN"
    
    @property
    def all_passed(self) -> bool:
        return all(r.passed for r in self.results)
    
    @property
    def failing_platforms(self) -> list[str]:
        return [r.platform for r in self.results if not r.passed]


class CopilotAuditor:
    """
    Uses GitHub Copilot CLI to evaluate content quality.
    
    Example:
        auditor = CopilotAuditor()
        result = auditor.audit_content("My tweet text", "twitter")
        print(f"Score: {result.total_score}/10")
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir is None:
            config_dir = Path(__file__).parent / "config"
        
        self.config_dir = config_dir
        self.rules = self._load_yaml("audit_rules.yaml")
        self.prompts = self._load_yaml("prompts.yaml")
        self.settings = self.rules.get("settings", {})
    
    def _load_yaml(self, filename: str) -> dict:
        """Load a YAML config file."""
        filepath = self.config_dir / filename
        if not filepath.exists():
            return {}
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def audit_content(self, content: str, platform: str) -> AuditResult:
        """
        Audit content for a specific platform using Copilot CLI.
        
        Args:
            content: The text content to audit
            platform: Platform name (twitter, linkedin, newsletter)
            
        Returns:
            AuditResult with scores, issues, and suggestions
        """
        if not content or not content.strip():
            return AuditResult(
                platform=platform,
                content=content,
                status="FAIL",
                issues=["Content is empty or whitespace only"]
            )
        
        # Build the audit prompt
        prompt = self._build_audit_prompt(content, platform)
        
        # Call Copilot CLI
        raw_response = self._call_copilot(prompt)
        
        # Parse the response
        result = self._parse_audit_response(raw_response, platform, content)
        
        return result
    
    def audit_all(self, content_dict: dict[str, str]) -> AuditReport:
        """
        Audit content for all platforms in the dict.
        
        Args:
            content_dict: Dict with platform names as keys and content as values
                          Example: {"twitter": "...", "linkedin": "..."}
        
        Returns:
            AuditReport with all results
        """
        results = []
        
        for platform, content in content_dict.items():
            if platform in ["twitter", "linkedin", "newsletter"] and content:
                result = self.audit_content(content, platform)
                results.append(result)
        
        # Determine overall status
        if not results:
            overall = "UNKNOWN"
        elif all(r.status == "PASS" for r in results):
            overall = "PASS"
        elif any(r.status == "FAIL" for r in results):
            overall = "FAIL"
        else:
            overall = "WARN"
        
        return AuditReport(results=results, overall_status=overall)
    
    def _build_audit_prompt(self, content: str, platform: str) -> str:
        """Build the prompt for Copilot CLI audit."""
        platform_prompts = self.prompts.get("audit", {}).get(platform, {})
        template = platform_prompts.get("prompt", "")
        
        if not template:
            # Fallback generic prompt
            template = f"""
            Evaluate this {platform} content for quality (1-10 scale):
            
            ```
            {{content}}
            ```
            
            Respond with JSON: {{"total": X, "issues": [], "suggestions": []}}
            """
        
        return template.format(content=content)
    
    def _call_copilot(self, prompt: str) -> str:
        """
        Execute copilot CLI command in non-interactive mode.
        
        Note: This requires:
        1. Copilot CLI installed (winget install GitHub.Copilot)
        2. Valid GitHub Copilot subscription
        3. GitHub authentication
        """
        try:
            # Use the new standalone Copilot CLI with:
            # -s: silent mode (only output agent response, good for scripting)
            # --no-ask-user: don't prompt for user input
            # -p: non-interactive prompt mode (MUST BE LAST)
            result = subprocess.run(
                ['copilot', '-s', '--no-ask-user', '-p', prompt],
                capture_output=True,
                text=True,
                timeout=self.settings.get("copilot_timeout", 60),
                encoding='utf-8'
            )
            
            if result.returncode != 0 or not result.stdout.strip():
                # Fallback: try deprecated gh copilot suggest
                result = subprocess.run(
                    ['gh', 'copilot', 'suggest', prompt],
                    capture_output=True,
                    text=True,
                    timeout=30,
                    encoding='utf-8'
                )
            
            return result.stdout + result.stderr
            
        except subprocess.TimeoutExpired:
            return '{"error": "Copilot CLI timeout", "total": 5}'
        except FileNotFoundError:
            return '{"error": "Copilot CLI not found. Install with: winget install GitHub.Copilot", "total": 0}'
        except Exception as e:
            return f'{{"error": "{str(e)}", "total": 0}}'
    
    def _parse_audit_response(self, response: str, platform: str, content: str) -> AuditResult:
        """Parse Copilot's response into an AuditResult."""
        result = AuditResult(
            platform=platform,
            content=content,
            raw_response=response
        )
        
        # Method 1: Try to extract score patterns from text first (most common)
        # Matches: "Rating: 7/10", "Score: 8/10", "7/10", "rated 6/10", etc.
        score_patterns = [
            r'(?:Rating|Score|Rated)[\s:]*(\d+(?:\.\d+)?)\s*/\s*10',  # "Rating: 7/10"
            r'\*\*(\d+(?:\.\d+)?)\s*/\s*10\*\*',  # **7/10** (markdown bold)
            r'(\d+(?:\.\d+)?)\s*/\s*10',  # Simple "7/10"
        ]
        
        score_found = False
        for pattern in score_patterns:
            score_match = re.search(pattern, response, re.IGNORECASE)
            if score_match:
                result.total_score = float(score_match.group(1))
                score_found = True
                break
        
        # Method 2: Try to extract JSON if present
        json_match = re.search(r'\{[^{}]*\}', response, re.DOTALL)
        if json_match:
            try:
                data = json.loads(json_match.group())
                
                # Extract scores from JSON if present
                if not score_found:
                    if "scores" in data:
                        result.scores = data["scores"]
                        result.total_score = sum(data["scores"].values()) / len(data["scores"])
                        score_found = True
                    elif "total" in data:
                        result.total_score = float(data["total"])
                        score_found = True
                
                result.issues = data.get("issues", [])
                result.suggestions = data.get("suggestions", [])
                
            except json.JSONDecodeError:
                pass  # JSON parse failed, use text score if found
        
        # Extract issues from bullet points in text
        if not result.issues:
            issue_patterns = [
                r'[-•]\s*\*\*([^*:]+)\*\*:',  # **Bold**: description
                r'[-•]\s*([^\n:]+):',  # - Item: description
            ]
            for pattern in issue_patterns:
                issues = re.findall(pattern, response)
                if issues:
                    result.issues = [issue.strip() for issue in issues[:5]]
                    break
        
        # If no score found after all attempts, default to middle
        if not score_found:
            result.total_score = 5.0
            result.issues.append("Could not parse score from Copilot response")
        
        # Determine status based on thresholds
        pass_threshold = self.settings.get("pass_threshold", 7)
        warn_threshold = self.settings.get("warn_threshold", 6)
        
        if result.total_score >= pass_threshold:
            result.status = "PASS"
        elif result.total_score >= warn_threshold:
            result.status = "WARN"
        else:
            result.status = "FAIL"
        
        result.max_score = 10.0
        
        return result


# Convenience function for quick audits
def quick_audit(content: str, platform: str = "twitter") -> AuditResult:
    """Quick audit of content without creating an auditor instance."""
    auditor = CopilotAuditor()
    return auditor.audit_content(content, platform)
