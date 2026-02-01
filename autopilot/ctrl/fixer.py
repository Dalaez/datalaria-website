"""
Quick-fix engine that uses GitHub Copilot CLI to improve failing content.
"""
import subprocess
import json
from dataclasses import dataclass
from typing import Optional
from pathlib import Path

import yaml

from .auditor import AuditResult, AuditReport


@dataclass
class FixResult:
    """Result of fixing content for a platform."""
    platform: str
    original_content: str
    fixed_content: str
    issues_addressed: list[str]
    success: bool
    error: Optional[str] = None


class CopilotFixer:
    """
    Uses GitHub Copilot CLI to generate improved content.
    
    Example:
        fixer = CopilotFixer()
        result = fixer.fix_content(audit_result)
        print(f"Fixed: {result.fixed_content}")
    """
    
    def __init__(self, config_dir: Optional[Path] = None):
        if config_dir is None:
            config_dir = Path(__file__).parent / "config"
        
        self.config_dir = config_dir
        self.prompts = self._load_yaml("prompts.yaml")
    
    def _load_yaml(self, filename: str) -> dict:
        """Load a YAML config file."""
        filepath = self.config_dir / filename
        if not filepath.exists():
            return {}
        with open(filepath, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f) or {}
    
    def fix_content(self, audit_result: AuditResult) -> FixResult:
        """
        Generate improved content based on audit issues.
        
        Args:
            audit_result: The audit result with issues to fix
            
        Returns:
            FixResult with the improved content
        """
        platform = audit_result.platform
        content = audit_result.content
        issues = audit_result.issues
        
        # Build fix prompt
        prompt = self._build_fix_prompt(content, platform, issues)
        
        # Call Copilot CLI
        fixed_content = self._call_copilot_for_fix(prompt)
        
        if fixed_content and not fixed_content.startswith('{"error"'):
            return FixResult(
                platform=platform,
                original_content=content,
                fixed_content=fixed_content.strip(),
                issues_addressed=issues,
                success=True
            )
        else:
            return FixResult(
                platform=platform,
                original_content=content,
                fixed_content=content,  # Keep original on failure
                issues_addressed=[],
                success=False,
                error=fixed_content or "No response from Copilot"
            )
    
    def fix_all(self, audit_report: AuditReport) -> dict[str, FixResult]:
        """
        Fix all failing content in an audit report.
        
        Args:
            audit_report: Complete audit report
            
        Returns:
            Dict mapping platform names to FixResults
        """
        fixes = {}
        
        for result in audit_report.results:
            if result.status != "PASS":
                fix_result = self.fix_content(result)
                fixes[result.platform] = fix_result
        
        return fixes
    
    def _build_fix_prompt(self, content: str, platform: str, issues: list[str]) -> str:
        """Build the prompt for Copilot CLI fix."""
        platform_prompts = self.prompts.get("fix", {}).get(platform, {})
        template = platform_prompts.get("prompt", "")
        
        issues_str = ", ".join(issues) if issues else "general quality improvement needed"
        
        if not template:
            # Fallback generic prompt
            template = f"""
            Improve this {platform} content. Issues to fix: {{issues}}
            
            Original:
            ```
            {{content}}
            ```
            
            Return ONLY the improved text, nothing else.
            """
        
        return template.format(content=content, issues=issues_str)
    
    def _call_copilot_for_fix(self, prompt: str) -> str:
        """Execute copilot CLI for content fix."""
        try:
            # Use the new standalone Copilot CLI
            # -s: silent mode (only output response)
            # --no-ask-user: don't prompt for input
            # -p: non-interactive prompt mode (MUST BE LAST)
            result = subprocess.run(
                ['copilot', '-s', '--no-ask-user', '-p', prompt],
                capture_output=True,
                text=True,
                timeout=60,
                encoding='utf-8'
            )
            
            response = result.stdout.strip()
            
            # Clean up common Copilot CLI output artifacts
            # Remove code block markers if present
            if response.startswith("```"):
                lines = response.split("\n")
                # Remove first and last lines (``` markers)
                if len(lines) > 2:
                    response = "\n".join(lines[1:-1])
            
            return response
            
        except subprocess.TimeoutExpired:
            return '{"error": "Copilot CLI timeout"}'
        except FileNotFoundError:
            return '{"error": "copilot CLI not found. Install with: winget install GitHub.Copilot"}'
        except Exception as e:
            return f'{{"error": "{str(e)}"}}'


def apply_fixes_to_file(content_file: Path, fixes: dict[str, FixResult]) -> Path:
    """
    Apply fixes to a content JSON file and save as new file.
    
    Args:
        content_file: Path to original generated_content.json
        fixes: Dict of FixResults from CopilotFixer
        
    Returns:
        Path to the fixed content file
    """
    with open(content_file, 'r', encoding='utf-8') as f:
        content = json.load(f)
    
    # Apply fixes
    for platform, fix_result in fixes.items():
        if fix_result.success:
            content[platform] = fix_result.fixed_content
    
    # Save to new file
    fixed_file = content_file.parent / f"{content_file.stem}_fixed.json"
    
    with open(fixed_file, 'w', encoding='utf-8') as f:
        json.dump(content, f, ensure_ascii=False, indent=2)
    
    return fixed_file
