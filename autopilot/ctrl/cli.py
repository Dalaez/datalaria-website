#!/usr/bin/env python3
"""
Autopilot-Ctrl CLI - AI Agent Content Auditor

A CLI tool that uses GitHub Copilot CLI to audit and fix 
AI-generated social media content.

Usage:
    autopilot-ctrl audit <content_file>      # Audit content quality
    autopilot-ctrl fix <content_file>        # Suggest improvements  
    autopilot-ctrl report <content_file>     # Generate detailed report

Built for the GitHub Copilot CLI Challenge 2026
https://dev.to/challenges/github-2026-01-21
"""
import json
import sys
import os
from pathlib import Path
from typing import Optional

# Fix Windows console encoding for UTF-8
if sys.platform == 'win32':
    os.system('chcp 65001 > nul 2>&1')
    if hasattr(sys.stdout, 'reconfigure'):
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')

import click
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich import box

from .auditor import CopilotAuditor, AuditReport, AuditResult
from .fixer import CopilotFixer, apply_fixes_to_file

console = Console(force_terminal=True)

# Status display (ASCII-safe for Windows)
STATUS_DISPLAY = {
    "PASS": ("[OK]", "green"),
    "WARN": ("[!!]", "yellow"),
    "FAIL": ("[XX]", "red"),
    "UNKNOWN": ("[??]", "dim"),
}


def print_banner():
    """Print the CLI banner."""
    console.print("="*50, style="bold cyan")
    console.print("  AUTOPILOT-CTRL", style="bold cyan") 
    console.print("  AI Agent Content Auditor", style="cyan")
    console.print("  Powered by GitHub Copilot CLI", style="cyan")
    console.print("="*50, style="bold cyan")
    console.print()


def load_content_file(filepath: str) -> dict:
    """Load content from JSON file."""
    path = Path(filepath)
    if not path.exists():
        console.print(f"[red]❌ File not found: {filepath}[/red]")
        sys.exit(1)
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        console.print(f"[red]❌ Invalid JSON: {e}[/red]")
        sys.exit(1)


def display_audit_result(result: AuditResult):
    """Display a single audit result."""
    emoji, color = STATUS_DISPLAY.get(result.status, ("❓", "dim"))
    
    console.print(f"\n[bold]{emoji} {result.platform.upper()}[/bold]", style=color)
    console.print(f"   Score: [bold]{result.total_score:.1f}/10[/bold]")
    
    if result.issues:
        console.print("   Issues:", style="yellow")
        for issue in result.issues:
            console.print(f"      • {issue}")
    
    if result.suggestions:
        console.print("   Suggestions:", style="cyan")
        for suggestion in result.suggestions:
            console.print(f"      💡 {suggestion}")


def display_audit_table(report: AuditReport):
    """Display audit results as a table."""
    table = Table(
        title="📊 Audit Results",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold magenta"
    )
    
    table.add_column("Platform", style="cyan", width=12)
    table.add_column("Score", justify="center", width=8)
    table.add_column("Status", justify="center", width=10)
    table.add_column("Issues", width=40)
    
    for result in report.results:
        emoji, color = STATUS_DISPLAY.get(result.status, ("❓", "dim"))
        issues_str = ", ".join(result.issues[:2]) if result.issues else "-"
        if len(result.issues) > 2:
            issues_str += f" (+{len(result.issues) - 2} more)"
        
        table.add_row(
            result.platform.capitalize(),
            f"[bold]{result.total_score:.1f}[/bold]/10",
            f"[{color}]{emoji} {result.status}[/{color}]",
            issues_str
        )
    
    console.print()
    console.print(table)
    
    # Overall status
    overall_emoji, overall_color = STATUS_DISPLAY.get(report.overall_status, ("❓", "dim"))
    console.print(f"\n[bold]Overall: [{overall_color}]{overall_emoji} {report.overall_status}[/{overall_color}][/bold]")
    
    if not report.all_passed:
        console.print(
            f"\n[yellow]💡 Tip: Run [bold]autopilot-ctrl fix {'{file}'}[/bold] to improve failing content[/yellow]"
        )


@click.group()
@click.version_option(version="0.1.0", prog_name="autopilot-ctrl")
def cli():
    """🤖 Autopilot-Ctrl: Audit your AI agents with GitHub Copilot CLI"""
    pass


@cli.command()
@click.argument('content_file', type=click.Path(exists=True))
@click.option('--platform', '-p', type=click.Choice(['twitter', 'linkedin', 'newsletter', 'all']),
              default='all', help='Platform to audit (default: all)')
@click.option('--force-pass', is_flag=True, help='Mark as passed regardless of score')
@click.option('--json-output', '-j', is_flag=True, help='Output results as JSON')
def audit(content_file: str, platform: str, force_pass: bool, json_output: bool):
    """
    Audit AI-generated content using GitHub Copilot CLI.
    
    Evaluates content quality against platform-specific criteria
    and returns actionable feedback.
    
    Example:
        autopilot-ctrl audit generated_content.json
        autopilot-ctrl audit -p twitter generated_content.json
    """
    if not json_output:
        print_banner()
        console.print(f"[dim]Auditing: {content_file}[/dim]\n")
    
    content = load_content_file(content_file)
    auditor = CopilotAuditor()
    
    # Filter platforms if specified
    if platform != 'all':
        content = {platform: content.get(platform, "")}
    
    # Run audit with progress indicator
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        if not json_output:
            task = progress.add_task("🔍 Calling GitHub Copilot CLI...", total=None)
        
        report = auditor.audit_all(content)
    
    if json_output:
        # JSON output for scripting
        output = {
            "overall_status": report.overall_status,
            "all_passed": report.all_passed,
            "results": [
                {
                    "platform": r.platform,
                    "score": r.total_score,
                    "status": r.status,
                    "issues": r.issues,
                    "suggestions": r.suggestions
                }
                for r in report.results
            ]
        }
        click.echo(json.dumps(output, indent=2))
    else:
        display_audit_table(report)
        
        # Show detailed results
        for result in report.results:
            if result.status != "PASS":
                display_audit_result(result)
    
    # Exit code based on status
    if force_pass:
        sys.exit(0)
    elif report.overall_status == "FAIL":
        sys.exit(1)
    else:
        sys.exit(0)


@cli.command()
@click.argument('content_file', type=click.Path(exists=True))
@click.option('--platform', '-p', type=click.Choice(['twitter', 'linkedin', 'newsletter', 'all']),
              default='all', help='Platform to fix (default: all failing)')
@click.option('--apply', 'apply_fix', is_flag=True, help='Apply fixes to a new file')
@click.option('--preview', is_flag=True, help='Preview fixes without saving')
def fix(content_file: str, platform: str, apply_fix: bool, preview: bool):
    """
    Generate improved content using GitHub Copilot CLI.
    
    Analyzes failing content and generates improvements
    based on the identified issues.
    
    Example:
        autopilot-ctrl fix generated_content.json
        autopilot-ctrl fix --apply generated_content.json
    """
    print_banner()
    console.print(f"[dim]Fixing: {content_file}[/dim]\n")
    
    content = load_content_file(content_file)
    auditor = CopilotAuditor()
    fixer = CopilotFixer()
    
    # First, audit to find issues
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        progress.add_task("🔍 Auditing content first...", total=None)
        
        if platform != 'all':
            audit_content = {platform: content.get(platform, "")}
        else:
            audit_content = content
        
        report = auditor.audit_all(audit_content)
    
    # Show what needs fixing
    failing = [r for r in report.results if r.status != "PASS"]
    
    if not failing:
        console.print("[green]✅ All content passes! Nothing to fix.[/green]")
        sys.exit(0)
    
    console.print(f"[yellow]Found {len(failing)} platform(s) that need improvement:[/yellow]")
    for r in failing:
        console.print(f"   • {r.platform}: {', '.join(r.issues[:2])}")
    
    # Generate fixes
    console.print("\n[cyan]🤖 Generating improvements with Copilot CLI...[/cyan]\n")
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        task = progress.add_task("Calling Copilot...", total=len(failing))
        
        fixes = fixer.fix_all(report)
        progress.update(task, completed=len(failing))
    
    # Display fixes
    for platform_name, fix_result in fixes.items():
        if fix_result.success:
            console.print(Panel(
                fix_result.fixed_content,
                title=f"[green]✨ {platform_name.upper()} - Improved[/green]",
                border_style="green"
            ))
        else:
            console.print(f"[red]❌ Failed to fix {platform_name}: {fix_result.error}[/red]")
    
    # Apply if requested
    if apply_fix and not preview:
        content_path = Path(content_file)
        fixed_file = apply_fixes_to_file(content_path, fixes)
        console.print(f"\n[green]💾 Fixed content saved to: {fixed_file}[/green]")
    elif preview:
        console.print("\n[dim]Preview mode - no changes saved.[/dim]")
    else:
        console.print(
            f"\n[yellow]💡 Run with [bold]--apply[/bold] to save fixes to file[/yellow]"
        )


@cli.command()
@click.argument('content_file', type=click.Path(exists=True))
@click.option('--output', '-o', type=click.Path(), help='Save report to file')
def report(content_file: str, output: Optional[str]):
    """
    Generate a detailed audit report.
    
    Creates a comprehensive report with all scores, issues,
    and recommendations for improvement.
    """
    print_banner()
    
    content = load_content_file(content_file)
    auditor = CopilotAuditor()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
        transient=True
    ) as progress:
        progress.add_task("🔍 Running comprehensive audit...", total=None)
        audit_report = auditor.audit_all(content)
    
    # Build report
    report_lines = [
        "# Autopilot-Ctrl Audit Report",
        f"\n**File:** {content_file}",
        f"**Overall Status:** {audit_report.overall_status}",
        "\n## Results by Platform\n"
    ]
    
    for result in audit_report.results:
        emoji, _ = STATUS_DISPLAY.get(result.status, ("❓", "dim"))
        report_lines.append(f"### {result.platform.capitalize()} {emoji}")
        report_lines.append(f"- **Score:** {result.total_score:.1f}/10")
        report_lines.append(f"- **Status:** {result.status}")
        
        if result.issues:
            report_lines.append("- **Issues:**")
            for issue in result.issues:
                report_lines.append(f"  - {issue}")
        
        if result.suggestions:
            report_lines.append("- **Suggestions:**")
            for suggestion in result.suggestions:
                report_lines.append(f"  - {suggestion}")
        
        report_lines.append("")
    
    report_content = "\n".join(report_lines)
    
    if output:
        with open(output, 'w', encoding='utf-8') as f:
            f.write(report_content)
        console.print(f"[green]📄 Report saved to: {output}[/green]")
    else:
        console.print(report_content)


@cli.command()
def check():
    """
    Check if GitHub Copilot CLI is installed and working.
    """
    print_banner()
    console.print("Checking GitHub Copilot CLI setup...\n")
    
    import subprocess
    
    # Check gh CLI
    try:
        result = subprocess.run(['gh', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            console.print(f"[green]✅ GitHub CLI installed[/green]")
            console.print(f"   {result.stdout.split(chr(10))[0]}")
        else:
            console.print("[red]❌ GitHub CLI not working[/red]")
            sys.exit(1)
    except FileNotFoundError:
        console.print("[red]❌ GitHub CLI (gh) not found[/red]")
        console.print("   Install from: https://cli.github.com/")
        sys.exit(1)
    
    # Check Copilot extension
    try:
        result = subprocess.run(['gh', 'copilot', '--help'], capture_output=True, text=True)
        if result.returncode == 0:
            console.print("[green]✅ Copilot CLI extension installed[/green]")
        else:
            console.print("[yellow]⚠️ Copilot CLI extension may need setup[/yellow]")
            console.print("   Run: gh extension install github/copilot-cli")
    except Exception:
        console.print("[yellow]⚠️ Could not verify Copilot CLI extension[/yellow]")
    
    console.print("\n[green]✅ Setup looks good![/green]")


def main():
    """Entry point for the CLI."""
    cli()


if __name__ == '__main__':
    main()
