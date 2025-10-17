"""Environment checker for automated setup validation."""
import sys
import subprocess
import shutil
from typing import Dict, Any, List, Optional
from pathlib import Path

from ..core.component import Component


class EnvironmentChecker(Component):
    """Automates environment checks and setup validation.
    
    Reduces friction by automatically verifying:
    - Python version compatibility
    - Required dependencies
    - System tools availability
    - Project directory structure
    """

    def __init__(self, name: str = "environment", config: Optional[Dict[str, Any]] = None):
        """Initialize environment checker.
        
        Args:
            name: Component name
            config: Configuration dictionary with:
                - python_version: Minimum Python version (e.g., "3.8")
                - required_packages: List of required Python packages
                - required_tools: List of required system tools
                - directories: List of required directories
        """
        super().__init__(name, config)
        self.checks_passed: Dict[str, bool] = {}
        self.issues: List[str] = []

    def initialize(self) -> bool:
        """Initialize the environment checker."""
        self._initialized = True
        return True

    def validate(self) -> bool:
        """Validate the environment.
        
        Returns:
            True if all checks pass, False otherwise
        """
        self.checks_passed = {}
        self.issues = []

        # Check Python version
        self.checks_passed["python_version"] = self._check_python_version()
        
        # Check required packages
        self.checks_passed["packages"] = self._check_packages()
        
        # Check required tools
        self.checks_passed["tools"] = self._check_tools()
        
        # Check directories
        self.checks_passed["directories"] = self._check_directories()

        return all(self.checks_passed.values())

    def _check_python_version(self) -> bool:
        """Check if Python version meets requirements."""
        required = self.config.get("python_version", "3.8")
        current = f"{sys.version_info.major}.{sys.version_info.minor}"
        
        required_parts = [int(x) for x in required.split(".")]
        current_parts = [sys.version_info.major, sys.version_info.minor]
        
        if current_parts < required_parts:
            self.issues.append(
                f"Python version {current} is below required {required}"
            )
            return False
        return True

    def _check_packages(self) -> bool:
        """Check if required packages are installed."""
        required_packages = self.config.get("required_packages", [])
        all_installed = True

        for package in required_packages:
            try:
                __import__(package)
            except ImportError:
                self.issues.append(f"Required package not installed: {package}")
                all_installed = False

        return all_installed

    def _check_tools(self) -> bool:
        """Check if required system tools are available."""
        required_tools = self.config.get("required_tools", [])
        all_available = True

        for tool in required_tools:
            if not shutil.which(tool):
                self.issues.append(f"Required tool not found: {tool}")
                all_available = False

        return all_available

    def _check_directories(self) -> bool:
        """Check if required directories exist."""
        required_dirs = self.config.get("directories", [])
        all_exist = True

        for dir_path in required_dirs:
            path = Path(dir_path)
            if not path.exists():
                self.issues.append(f"Required directory not found: {dir_path}")
                all_exist = False
            elif not path.is_dir():
                self.issues.append(f"Path is not a directory: {dir_path}")
                all_exist = False

        return all_exist

    def auto_fix(self) -> Dict[str, bool]:
        """Attempt to automatically fix environment issues.
        
        Returns:
            Dictionary mapping fix actions to success status
        """
        fixes = {}

        # Create missing directories
        required_dirs = self.config.get("directories", [])
        for dir_path in required_dirs:
            path = Path(dir_path)
            if not path.exists():
                try:
                    path.mkdir(parents=True, exist_ok=True)
                    fixes[f"create_dir_{dir_path}"] = True
                except Exception as e:
                    fixes[f"create_dir_{dir_path}"] = False
                    self.issues.append(f"Failed to create directory {dir_path}: {e}")

        return fixes

    def get_status(self) -> Dict[str, Any]:
        """Get current environment status."""
        return {
            "enabled": self.is_enabled(),
            "initialized": self.is_initialized(),
            "checks_passed": self.checks_passed,
            "issues": self.issues,
            "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        }

    def get_report(self) -> str:
        """Generate a human-readable environment report.
        
        Returns:
            Formatted report string
        """
        lines = ["Environment Check Report", "=" * 40]
        
        for check_name, passed in self.checks_passed.items():
            status = "✓ PASS" if passed else "✗ FAIL"
            lines.append(f"{status} - {check_name}")
        
        if self.issues:
            lines.append("\nIssues Found:")
            for issue in self.issues:
                lines.append(f"  - {issue}")
        else:
            lines.append("\nNo issues found!")
        
        return "\n".join(lines)
