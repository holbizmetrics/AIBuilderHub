"""AIDeveloperTool - Universal tool for AI development.

A modular framework supporting coders, creators, and CEOs in managing AI projects.
Provides setup automation, context sharing, actionable feedback, and pipeline management.
"""

__version__ = "0.1.0"

from .core.project import AIProject
from .core.component import Component
from .setup.environment import EnvironmentChecker
from .context.manager import ContextManager
from .feedback.tracker import FeedbackTracker
from .pipeline.manager import PipelineManager

__all__ = [
    "AIProject",
    "Component",
    "EnvironmentChecker",
    "ContextManager",
    "FeedbackTracker",
    "PipelineManager",
]
