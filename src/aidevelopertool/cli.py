"""Command-line interface for AIDeveloperTool."""
import argparse
import sys
from pathlib import Path
from typing import Optional

try:
    from rich.console import Console
    from rich.table import Table
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False

from .core.project import AIProject
from .setup.environment import EnvironmentChecker
from .context.manager import ContextManager
from .feedback.tracker import FeedbackTracker, FeedbackLevel
from .pipeline.manager import PipelineManager


console = Console() if RICH_AVAILABLE else None


def print_output(message: str, style: str = "") -> None:
    """Print output with optional styling."""
    if console:
        console.print(message, style=style)
    else:
        print(message)


def cmd_init(args) -> int:
    """Initialize a new AI project."""
    print_output(f"Initializing project: {args.name}", style="bold green")
    
    project = AIProject(args.name, Path.cwd())
    
    # Add default components
    env_checker = EnvironmentChecker(config={
        "python_version": "3.8",
        "directories": ["data", "models", "notebooks"],
    })
    project.add_component(env_checker)
    
    context_mgr = ContextManager()
    project.add_component(context_mgr)
    
    feedback = FeedbackTracker()
    project.add_component(feedback)
    
    pipeline_mgr = PipelineManager()
    project.add_component(pipeline_mgr)
    
    # Initialize project
    if project.initialize():
        print_output("✓ Project initialized successfully", style="green")
        
        # Save configuration
        project.save_config()
        print_output(f"✓ Configuration saved to ai_project.yaml", style="green")
        
        return 0
    else:
        print_output("✗ Failed to initialize project", style="red")
        return 1


def cmd_check(args) -> int:
    """Check environment setup."""
    print_output("Checking environment...", style="bold")
    
    config = {
        "python_version": args.python_version or "3.8",
        "required_packages": args.packages.split(",") if args.packages else [],
        "required_tools": args.tools.split(",") if args.tools else [],
        "directories": args.directories.split(",") if args.directories else [],
    }
    
    checker = EnvironmentChecker(config=config)
    checker.initialize()
    
    is_valid = checker.validate()
    
    print_output("\n" + checker.get_report())
    
    if not is_valid and args.auto_fix:
        print_output("\nAttempting auto-fix...", style="yellow")
        fixes = checker.auto_fix()
        
        for fix_name, success in fixes.items():
            status = "✓" if success else "✗"
            print_output(f"{status} {fix_name}")
        
        # Re-validate
        is_valid = checker.validate()
    
    return 0 if is_valid else 1


def cmd_status(args) -> int:
    """Show project status."""
    config_path = Path(args.config or "ai_project.yaml")
    
    if not config_path.exists():
        print_output("✗ No project configuration found", style="red")
        print_output("  Run 'aideveloper init' to create a project", style="yellow")
        return 1
    
    project = AIProject.load_config(config_path)
    status = project.get_status()
    
    print_output(f"\nProject: {status['project']}", style="bold")
    print_output(f"Initialized: {status['initialized']}")
    
    print_output("\nComponents:", style="bold")
    for comp_name, comp_status in status["components"].items():
        enabled = "✓" if comp_status.get("enabled") else "✗"
        print_output(f"  {enabled} {comp_name}")
    
    return 0


def cmd_feedback(args) -> int:
    """Show feedback and progress."""
    tracker = FeedbackTracker()
    tracker.initialize()
    
    # Load from config if available
    config_path = Path(args.config or "ai_project.yaml")
    if config_path.exists():
        project = AIProject.load_config(config_path)
        feedback_comp = project.get_component("feedback")
        if feedback_comp:
            tracker = feedback_comp
    
    level = FeedbackLevel(args.level) if args.level else None
    summary = tracker.get_progress_summary(level)
    
    print_output("\nProgress Summary", style="bold")
    print_output(f"Level: {summary['level']}")
    
    if "milestones" in summary:
        milestones = summary["milestones"]
        print_output(
            f"\nMilestones: {milestones['completed']}/{milestones['total']} "
            f"({milestones['percentage']:.1f}%)"
        )
    
    if summary.get("recent_events"):
        print_output("\nRecent Events:", style="bold")
        for event in summary["recent_events"]:
            print_output(f"  [{event['category']}] {event['message']}")
    
    return 0


def main() -> int:
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="AIDeveloperTool - Universal tool for AI development",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Init command
    init_parser = subparsers.add_parser("init", help="Initialize a new AI project")
    init_parser.add_argument("name", help="Project name")
    init_parser.set_defaults(func=cmd_init)
    
    # Check command
    check_parser = subparsers.add_parser("check", help="Check environment setup")
    check_parser.add_argument("--python-version", help="Minimum Python version")
    check_parser.add_argument("--packages", help="Required packages (comma-separated)")
    check_parser.add_argument("--tools", help="Required tools (comma-separated)")
    check_parser.add_argument("--directories", help="Required directories (comma-separated)")
    check_parser.add_argument("--auto-fix", action="store_true", help="Attempt to auto-fix issues")
    check_parser.set_defaults(func=cmd_check)
    
    # Status command
    status_parser = subparsers.add_parser("status", help="Show project status")
    status_parser.add_argument("--config", help="Path to project config")
    status_parser.set_defaults(func=cmd_status)
    
    # Feedback command
    feedback_parser = subparsers.add_parser("feedback", help="Show feedback and progress")
    feedback_parser.add_argument(
        "--level",
        choices=["technical", "executive", "creative"],
        help="Feedback detail level"
    )
    feedback_parser.add_argument("--config", help="Path to project config")
    feedback_parser.set_defaults(func=cmd_feedback)
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return 1
    
    try:
        return args.func(args)
    except Exception as e:
        print_output(f"Error: {e}", style="red bold")
        return 1


if __name__ == "__main__":
    sys.exit(main())
