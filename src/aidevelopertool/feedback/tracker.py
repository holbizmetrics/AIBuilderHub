"""Feedback tracker for actionable, explainable progress tracking."""
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum
from pathlib import Path
import json

from ..core.component import Component


class FeedbackLevel(Enum):
    """Feedback detail level for different user types."""
    TECHNICAL = "technical"  # Detailed for coders
    EXECUTIVE = "executive"  # High-level for CEOs
    CREATIVE = "creative"    # Visual/narrative for creators


class FeedbackTracker(Component):
    """Tracks and delivers actionable, explainable feedback.
    
    Provides progress tracking with different detail levels for
    coders, creators, and CEOs. Makes AI development transparent
    and accessible to all stakeholders.
    """

    def __init__(self, name: str = "feedback", config: Optional[Dict[str, Any]] = None):
        """Initialize feedback tracker.
        
        Args:
            name: Component name
            config: Configuration dictionary with:
                - default_level: Default feedback level
                - log_dir: Directory to store feedback logs
                - enable_console: Whether to print to console
        """
        super().__init__(name, config)
        self.events: List[Dict[str, Any]] = []
        self.milestones: List[Dict[str, Any]] = []
        self.metrics: Dict[str, Any] = {}
        self.log_dir = Path(self.config.get("log_dir", "logs"))
        self.default_level = FeedbackLevel(
            self.config.get("default_level", "technical")
        )
        self.enable_console = self.config.get("enable_console", True)
        self.listeners: List[Callable] = []

    def initialize(self) -> bool:
        """Initialize the feedback tracker."""
        if self.log_dir:
            self.log_dir.mkdir(parents=True, exist_ok=True)
        self._initialized = True
        return True

    def validate(self) -> bool:
        """Validate feedback tracker state."""
        if self.log_dir and not self.log_dir.exists():
            return False
        return True

    def log_event(
        self,
        message: str,
        level: str = "info",
        metadata: Optional[Dict[str, Any]] = None,
        category: str = "general"
    ) -> None:
        """Log an event with context.
        
        Args:
            message: Event message
            level: Event level (info, warning, error, success)
            metadata: Additional event metadata
            category: Event category for filtering
        """
        event = {
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "level": level,
            "category": category,
            "metadata": metadata or {},
        }
        
        self.events.append(event)
        
        if self.enable_console:
            self._print_event(event)
        
        # Notify listeners
        for listener in self.listeners:
            listener(event)

    def add_milestone(
        self,
        name: str,
        description: str,
        completed: bool = False,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Add a project milestone.
        
        Args:
            name: Milestone name
            description: Milestone description
            completed: Whether milestone is completed
            metadata: Additional milestone metadata
        """
        milestone = {
            "name": name,
            "description": description,
            "completed": completed,
            "created_at": datetime.now().isoformat(),
            "completed_at": datetime.now().isoformat() if completed else None,
            "metadata": metadata or {},
        }
        
        self.milestones.append(milestone)
        
        if completed:
            self.log_event(
                f"Milestone completed: {name}",
                level="success",
                category="milestone"
            )

    def complete_milestone(self, name: str) -> bool:
        """Mark a milestone as completed.
        
        Args:
            name: Milestone name
            
        Returns:
            True if found and updated, False otherwise
        """
        for milestone in self.milestones:
            if milestone["name"] == name and not milestone["completed"]:
                milestone["completed"] = True
                milestone["completed_at"] = datetime.now().isoformat()
                self.log_event(
                    f"Milestone completed: {name}",
                    level="success",
                    category="milestone"
                )
                return True
        return False

    def update_metric(self, key: str, value: Any) -> None:
        """Update a project metric.
        
        Args:
            key: Metric key
            value: Metric value
        """
        self.metrics[key] = {
            "value": value,
            "updated_at": datetime.now().isoformat(),
        }

    def get_progress_summary(self, level: Optional[FeedbackLevel] = None) -> Dict[str, Any]:
        """Get progress summary tailored to user level.
        
        Args:
            level: Feedback level (defaults to configured level)
            
        Returns:
            Progress summary dictionary
        """
        level = level or self.default_level
        
        total_milestones = len(self.milestones)
        completed_milestones = sum(1 for m in self.milestones if m["completed"])
        
        summary = {
            "level": level.value,
            "timestamp": datetime.now().isoformat(),
            "milestones": {
                "total": total_milestones,
                "completed": completed_milestones,
                "percentage": (completed_milestones / total_milestones * 100) 
                             if total_milestones > 0 else 0,
            },
            "recent_events": self.events[-5:] if self.events else [],
            "metrics": self.metrics,
        }
        
        if level == FeedbackLevel.TECHNICAL:
            summary["all_events"] = self.events
            summary["all_milestones"] = self.milestones
        elif level == FeedbackLevel.EXECUTIVE:
            summary["key_milestones"] = [
                m for m in self.milestones 
                if m.get("metadata", {}).get("executive_visibility", False)
            ]
        elif level == FeedbackLevel.CREATIVE:
            summary["story"] = self._generate_story()
        
        return summary

    def _generate_story(self) -> str:
        """Generate a narrative story from events and milestones."""
        story_parts = []
        
        if self.milestones:
            completed = [m for m in self.milestones if m["completed"]]
            pending = [m for m in self.milestones if not m["completed"]]
            
            story_parts.append(
                f"Journey so far: {len(completed)} milestones achieved"
            )
            
            if pending:
                story_parts.append(
                    f"Next up: {pending[0]['name']} - {pending[0]['description']}"
                )
        
        return " | ".join(story_parts)

    def get_explainable_status(self, item: str) -> Dict[str, Any]:
        """Get explainable status for a specific item.
        
        Args:
            item: Item to explain (milestone name, metric key, etc.)
            
        Returns:
            Explainable status with reasoning
        """
        # Check milestones
        for milestone in self.milestones:
            if milestone["name"] == item:
                return {
                    "item": item,
                    "type": "milestone",
                    "status": "completed" if milestone["completed"] else "pending",
                    "explanation": milestone["description"],
                    "timeline": {
                        "created": milestone["created_at"],
                        "completed": milestone.get("completed_at"),
                    },
                }
        
        # Check metrics
        if item in self.metrics:
            return {
                "item": item,
                "type": "metric",
                "value": self.metrics[item]["value"],
                "explanation": f"Current value: {self.metrics[item]['value']}",
                "last_updated": self.metrics[item]["updated_at"],
            }
        
        return {
            "item": item,
            "type": "unknown",
            "status": "not_found",
            "explanation": f"No information available for: {item}",
        }

    def add_listener(self, callback: Callable) -> None:
        """Add a listener for feedback events.
        
        Args:
            callback: Function to call on events
        """
        self.listeners.append(callback)

    def export_report(self, filepath: Optional[Path] = None) -> Path:
        """Export full feedback report to JSON.
        
        Args:
            filepath: Optional output file path
            
        Returns:
            Path to exported report
        """
        if filepath is None:
            filepath = self.log_dir / f"feedback_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            "generated_at": datetime.now().isoformat(),
            "events": self.events,
            "milestones": self.milestones,
            "metrics": self.metrics,
            "summary": self.get_progress_summary(),
        }
        
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w") as f:
            json.dump(report, f, indent=2)
        
        return filepath

    def _print_event(self, event: Dict[str, Any]) -> None:
        """Print event to console with formatting."""
        level_symbols = {
            "info": "ℹ",
            "warning": "⚠",
            "error": "✗",
            "success": "✓",
        }
        symbol = level_symbols.get(event["level"], "•")
        print(f"{symbol} [{event['category']}] {event['message']}")

    def get_status(self) -> Dict[str, Any]:
        """Get current feedback tracker status."""
        return {
            "enabled": self.is_enabled(),
            "initialized": self.is_initialized(),
            "events_count": len(self.events),
            "milestones_count": len(self.milestones),
            "metrics_count": len(self.metrics),
            "log_dir": str(self.log_dir),
        }
