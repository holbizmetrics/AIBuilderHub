"""Tests for core components."""
import pytest
from pathlib import Path
from aidevelopertool.core.component import Component
from aidevelopertool.core.project import AIProject


class MockComponent(Component):
    """Mock component for testing."""
    
    def initialize(self) -> bool:
        self._initialized = True
        return True
    
    def validate(self) -> bool:
        return self._initialized
    
    def get_status(self):
        return {
            "initialized": self._initialized,
            "enabled": self._enabled,
        }


def test_component_creation():
    """Test component creation and initialization."""
    comp = MockComponent("test_component", {"key": "value"})
    assert comp.name == "test_component"
    assert comp.config["key"] == "value"
    assert not comp.is_initialized()
    assert comp.is_enabled()


def test_component_initialization():
    """Test component initialization."""
    comp = MockComponent("test")
    assert comp.initialize()
    assert comp.is_initialized()


def test_component_enable_disable():
    """Test component enable/disable."""
    comp = MockComponent("test")
    comp.initialize()
    
    assert comp.is_enabled()
    comp.disable()
    assert not comp.is_enabled()
    comp.enable()
    assert comp.is_enabled()


def test_aiproject_creation():
    """Test AIProject creation."""
    project = AIProject("test-project")
    assert project.name == "test-project"
    assert len(project.components) == 0


def test_aiproject_add_component():
    """Test adding components to project."""
    project = AIProject("test-project")
    comp1 = MockComponent("comp1")
    comp2 = MockComponent("comp2")
    
    project.add_component(comp1)
    project.add_component(comp2)
    
    assert len(project.components) == 2
    assert project.get_component("comp1") == comp1
    assert project.get_component("comp2") == comp2


def test_aiproject_remove_component():
    """Test removing components from project."""
    project = AIProject("test-project")
    comp = MockComponent("comp")
    
    project.add_component(comp)
    assert len(project.components) == 1
    
    project.remove_component("comp")
    assert len(project.components) == 0


def test_aiproject_initialization():
    """Test project initialization."""
    project = AIProject("test-project")
    comp1 = MockComponent("comp1")
    comp2 = MockComponent("comp2")
    
    project.add_component(comp1)
    project.add_component(comp2)
    
    assert project.initialize()
    assert comp1.is_initialized()
    assert comp2.is_initialized()


def test_aiproject_validation():
    """Test project validation."""
    project = AIProject("test-project")
    comp1 = MockComponent("comp1")
    comp2 = MockComponent("comp2")
    
    project.add_component(comp1)
    project.add_component(comp2)
    project.initialize()
    
    results = project.validate()
    assert results["comp1"]
    assert results["comp2"]


def test_aiproject_status():
    """Test project status reporting."""
    project = AIProject("test-project")
    comp = MockComponent("comp")
    
    project.add_component(comp)
    project.initialize()
    
    status = project.get_status()
    assert status["project"] == "test-project"
    assert status["initialized"]
    assert "comp" in status["components"]


def test_aiproject_config_save_load(tmp_path):
    """Test saving and loading project configuration."""
    config_path = tmp_path / "test_project.yaml"
    
    # Create and save project
    project = AIProject("test-project", tmp_path)
    comp = MockComponent("test_comp", {"setting": "value"})
    project.add_component(comp)
    project.save_config(config_path)
    
    assert config_path.exists()
    
    # Load project
    loaded_project = AIProject.load_config(config_path)
    assert loaded_project.name == "test-project"
    assert loaded_project.project_dir == tmp_path


def test_aiproject_cleanup():
    """Test project cleanup."""
    project = AIProject("test-project")
    comp = MockComponent("comp")
    project.add_component(comp)
    project.initialize()
    
    # Should not raise any errors
    project.cleanup()
