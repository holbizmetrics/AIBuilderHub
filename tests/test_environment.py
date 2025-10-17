"""Tests for environment checker."""
import pytest
import sys
from pathlib import Path
from aidevelopertool.setup.environment import EnvironmentChecker


def test_environment_checker_creation():
    """Test environment checker creation."""
    checker = EnvironmentChecker(config={
        "python_version": "3.8",
        "required_packages": [],
        "required_tools": [],
        "directories": []
    })
    assert checker.name == "environment"
    assert checker.initialize()


def test_python_version_check():
    """Test Python version validation."""
    current_version = f"{sys.version_info.major}.{sys.version_info.minor}"
    
    # Should pass with current version
    checker = EnvironmentChecker(config={"python_version": current_version})
    checker.initialize()
    assert checker.validate()
    assert checker.checks_passed.get("python_version")


def test_package_check():
    """Test package availability check."""
    # Test with a package that should exist (sys is built-in)
    checker = EnvironmentChecker(config={"required_packages": ["sys"]})
    checker.initialize()
    checker.validate()
    assert checker.checks_passed.get("packages")


def test_directory_check(tmp_path):
    """Test directory existence check."""
    test_dir = tmp_path / "test_directory"
    test_dir.mkdir()
    
    checker = EnvironmentChecker(config={
        "directories": [str(test_dir)]
    })
    checker.initialize()
    assert checker.validate()
    assert checker.checks_passed.get("directories")


def test_missing_directory_check(tmp_path):
    """Test handling of missing directories."""
    missing_dir = tmp_path / "missing_directory"
    
    checker = EnvironmentChecker(config={
        "directories": [str(missing_dir)]
    })
    checker.initialize()
    assert not checker.validate()
    assert not checker.checks_passed.get("directories")
    assert len(checker.issues) > 0


def test_auto_fix_directories(tmp_path):
    """Test auto-fix for missing directories."""
    missing_dir = tmp_path / "auto_created_dir"
    
    checker = EnvironmentChecker(config={
        "directories": [str(missing_dir)]
    })
    checker.initialize()
    
    # Should fail initially
    assert not checker.validate()
    
    # Auto-fix should create the directory
    fixes = checker.auto_fix()
    assert any("create_dir" in key for key in fixes.keys())
    
    # Should pass after auto-fix
    assert missing_dir.exists()


def test_status_report():
    """Test status reporting."""
    checker = EnvironmentChecker()
    checker.initialize()
    checker.validate()
    
    status = checker.get_status()
    assert "enabled" in status
    assert "initialized" in status
    assert "checks_passed" in status
    assert "python_version" in status


def test_human_readable_report():
    """Test human-readable report generation."""
    checker = EnvironmentChecker()
    checker.initialize()
    checker.validate()
    
    report = checker.get_report()
    assert "Environment Check Report" in report
    assert "python_version" in report
