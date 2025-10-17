"""AIProject class for managing AI development projects."""
from typing import Dict, Any, List, Optional
from pathlib import Path
import yaml
from datetime import datetime

from .component import Component


class AIProject:
    """Main project management class.
    
    Coordinates components and provides a unified interface for managing
    AI development projects. Supports coders, creators, and CEOs with
    different needs.
    """

    def __init__(self, name: str, project_dir: Optional[Path] = None):
        """Initialize an AI project.
        
        Args:
            name: Project name
            project_dir: Optional project directory path
        """
        self.name = name
        self.project_dir = project_dir or Path.cwd()
        self.components: Dict[str, Component] = {}
        self.metadata: Dict[str, Any] = {
            "name": name,
            "created_at": datetime.now().isoformat(),
            "version": "0.1.0",
        }
        self._initialized = False

    def add_component(self, component: Component) -> None:
        """Add a component to the project.
        
        Args:
            component: Component instance to add
        """
        self.components[component.name] = component

    def remove_component(self, name: str) -> None:
        """Remove a component from the project.
        
        Args:
            name: Name of the component to remove
        """
        if name in self.components:
            self.components[name].cleanup()
            del self.components[name]

    def get_component(self, name: str) -> Optional[Component]:
        """Get a component by name.
        
        Args:
            name: Name of the component
            
        Returns:
            Component instance or None if not found
        """
        return self.components.get(name)

    def initialize(self) -> bool:
        """Initialize the project and all components.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        if self._initialized:
            return True

        success = True
        for component in self.components.values():
            if not component.initialize():
                success = False
                print(f"Failed to initialize component: {component.name}")

        self._initialized = success
        return success

    def validate(self) -> Dict[str, bool]:
        """Validate all components.
        
        Returns:
            Dictionary mapping component names to validation results
        """
        results = {}
        for name, component in self.components.items():
            results[name] = component.validate()
        return results

    def get_status(self) -> Dict[str, Any]:
        """Get comprehensive project status.
        
        Returns:
            Dictionary containing project and component status
        """
        component_status = {}
        for name, component in self.components.items():
            component_status[name] = component.get_status()

        return {
            "project": self.name,
            "initialized": self._initialized,
            "components": component_status,
            "metadata": self.metadata,
        }

    def save_config(self, config_path: Optional[Path] = None) -> None:
        """Save project configuration to YAML file.
        
        Args:
            config_path: Optional path to save config, defaults to project_dir/ai_project.yaml
        """
        if config_path is None:
            config_path = self.project_dir / "ai_project.yaml"

        config = {
            "project": {
                "name": self.name,
                "metadata": self.metadata,
            },
            "components": {
                name: {
                    "type": component.__class__.__name__,
                    "config": component.config,
                    "enabled": component.is_enabled(),
                }
                for name, component in self.components.items()
            },
        }

        config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(config_path, "w") as f:
            yaml.dump(config, f, default_flow_style=False)

    @classmethod
    def load_config(cls, config_path: Path) -> "AIProject":
        """Load project from configuration file.
        
        Args:
            config_path: Path to configuration file
            
        Returns:
            AIProject instance
        """
        with open(config_path, "r") as f:
            config = yaml.safe_load(f)

        project_config = config.get("project", {})
        project = cls(
            name=project_config.get("name", "unnamed"),
            project_dir=config_path.parent,
        )
        project.metadata.update(project_config.get("metadata", {}))

        return project

    def cleanup(self) -> None:
        """Clean up all project resources."""
        for component in self.components.values():
            component.cleanup()

    def __repr__(self) -> str:
        return f"AIProject(name={self.name}, components={len(self.components)})"
