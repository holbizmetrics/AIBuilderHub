"""Context manager for sharing state between tasks."""
import json
from typing import Dict, Any, Optional, List
from pathlib import Path
from datetime import datetime
from contextlib import contextmanager

from ..core.component import Component


class ContextManager(Component):
    """Manages shared context across tasks and components.
    
    Enables seamless information sharing between different parts of the
    AI development workflow, reducing duplication and improving collaboration.
    """

    def __init__(self, name: str = "context", config: Optional[Dict[str, Any]] = None):
        """Initialize context manager.
        
        Args:
            name: Component name
            config: Configuration dictionary with:
                - storage_dir: Directory to store context files
                - auto_save: Whether to auto-save context changes
        """
        super().__init__(name, config)
        self.contexts: Dict[str, Dict[str, Any]] = {}
        self.context_history: List[Dict[str, Any]] = []
        self.storage_dir = Path(self.config.get("storage_dir", ".ai_context"))
        self.auto_save = self.config.get("auto_save", True)

    def initialize(self) -> bool:
        """Initialize the context manager."""
        if self.storage_dir:
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._initialized = True
        return True

    def validate(self) -> bool:
        """Validate context manager state."""
        if self.storage_dir and not self.storage_dir.exists():
            return False
        return True

    def create_context(self, context_id: str, data: Optional[Dict[str, Any]] = None) -> None:
        """Create a new context.
        
        Args:
            context_id: Unique identifier for the context
            data: Initial context data
        """
        self.contexts[context_id] = {
            "id": context_id,
            "data": data or {},
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "version": 1,
        }
        
        if self.auto_save:
            self.save_context(context_id)

    def get_context(self, context_id: str) -> Optional[Dict[str, Any]]:
        """Retrieve a context by ID.
        
        Args:
            context_id: Context identifier
            
        Returns:
            Context data or None if not found
        """
        return self.contexts.get(context_id)

    def update_context(self, context_id: str, data: Dict[str, Any], merge: bool = True) -> None:
        """Update an existing context.
        
        Args:
            context_id: Context identifier
            data: New data to add to context
            merge: If True, merge with existing data; if False, replace
        """
        if context_id not in self.contexts:
            self.create_context(context_id, data)
            return

        context = self.contexts[context_id]
        
        if merge:
            context["data"].update(data)
        else:
            context["data"] = data
        
        context["updated_at"] = datetime.now().isoformat()
        context["version"] += 1
        
        # Store in history
        self.context_history.append({
            "context_id": context_id,
            "timestamp": datetime.now().isoformat(),
            "version": context["version"],
            "changes": list(data.keys()),
        })
        
        if self.auto_save:
            self.save_context(context_id)

    def delete_context(self, context_id: str) -> bool:
        """Delete a context.
        
        Args:
            context_id: Context identifier
            
        Returns:
            True if deleted, False if not found
        """
        if context_id in self.contexts:
            del self.contexts[context_id]
            
            # Delete from storage
            context_file = self.storage_dir / f"{context_id}.json"
            if context_file.exists():
                context_file.unlink()
            
            return True
        return False

    def save_context(self, context_id: str) -> None:
        """Save a context to disk.
        
        Args:
            context_id: Context identifier
        """
        if context_id not in self.contexts:
            return

        context = self.contexts[context_id]
        context_file = self.storage_dir / f"{context_id}.json"
        
        with open(context_file, "w") as f:
            json.dump(context, f, indent=2)

    def load_context(self, context_id: str) -> bool:
        """Load a context from disk.
        
        Args:
            context_id: Context identifier
            
        Returns:
            True if loaded successfully, False otherwise
        """
        context_file = self.storage_dir / f"{context_id}.json"
        
        if not context_file.exists():
            return False

        try:
            with open(context_file, "r") as f:
                self.contexts[context_id] = json.load(f)
            return True
        except Exception:
            return False

    def list_contexts(self) -> List[str]:
        """List all available context IDs.
        
        Returns:
            List of context identifiers
        """
        return list(self.contexts.keys())

    def share_between_contexts(self, source_id: str, target_id: str, keys: List[str]) -> bool:
        """Share specific data between contexts.
        
        Args:
            source_id: Source context identifier
            target_id: Target context identifier
            keys: List of keys to share
            
        Returns:
            True if successful, False otherwise
        """
        source = self.get_context(source_id)
        if not source:
            return False

        shared_data = {}
        for key in keys:
            if key in source["data"]:
                shared_data[key] = source["data"][key]

        if shared_data:
            self.update_context(target_id, shared_data)
            return True
        return False

    @contextmanager
    def temp_context(self, context_id: str):
        """Create a temporary context that is automatically cleaned up.
        
        Args:
            context_id: Temporary context identifier
            
        Yields:
            Context data dictionary
        """
        self.create_context(context_id)
        try:
            yield self.contexts[context_id]["data"]
        finally:
            self.delete_context(context_id)

    def get_status(self) -> Dict[str, Any]:
        """Get current context manager status."""
        return {
            "enabled": self.is_enabled(),
            "initialized": self.is_initialized(),
            "contexts_count": len(self.contexts),
            "contexts": list(self.contexts.keys()),
            "storage_dir": str(self.storage_dir),
            "auto_save": self.auto_save,
            "history_count": len(self.context_history),
        }

    def cleanup(self) -> None:
        """Clean up context manager resources."""
        if self.auto_save:
            for context_id in self.contexts:
                self.save_context(context_id)
