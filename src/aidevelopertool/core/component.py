"""Base component interface for modular architecture."""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class Component(ABC):
    """Base class for all modular components.
    
    This abstract class defines the interface that all components must implement
    to ensure consistent behavior across the AIDeveloperTool ecosystem.
    """

    def __init__(self, name: str, config: Optional[Dict[str, Any]] = None):
        """Initialize a component.
        
        Args:
            name: Unique identifier for the component
            config: Optional configuration dictionary
        """
        self.name = name
        self.config = config or {}
        self._initialized = False
        self._enabled = True

    @abstractmethod
    def initialize(self) -> bool:
        """Initialize the component.
        
        Returns:
            True if initialization was successful, False otherwise
        """
        pass

    @abstractmethod
    def validate(self) -> bool:
        """Validate component configuration and state.
        
        Returns:
            True if component is valid and ready to use, False otherwise
        """
        pass

    @abstractmethod
    def get_status(self) -> Dict[str, Any]:
        """Get current status of the component.
        
        Returns:
            Dictionary containing status information
        """
        pass

    def enable(self) -> None:
        """Enable this component."""
        self._enabled = True

    def disable(self) -> None:
        """Disable this component."""
        self._enabled = False

    def is_enabled(self) -> bool:
        """Check if component is enabled.
        
        Returns:
            True if component is enabled, False otherwise
        """
        return self._enabled

    def is_initialized(self) -> bool:
        """Check if component is initialized.
        
        Returns:
            True if component is initialized, False otherwise
        """
        return self._initialized

    def cleanup(self) -> None:
        """Clean up component resources.
        
        Override this method to implement custom cleanup logic.
        """
        pass

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name}, enabled={self._enabled})"
