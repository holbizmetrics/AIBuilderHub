"""Pipeline manager for workflow automation."""
from typing import Dict, Any, List, Optional, Callable
from datetime import datetime
from enum import Enum
import asyncio

from ..core.component import Component


class TaskStatus(Enum):
    """Status of a pipeline task."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    SKIPPED = "skipped"


class Task:
    """Represents a single task in a pipeline."""

    def __init__(
        self,
        name: str,
        func: Callable,
        description: str = "",
        dependencies: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None
    ):
        """Initialize a task.
        
        Args:
            name: Task name
            func: Function to execute
            description: Task description
            dependencies: List of task names this depends on
            metadata: Additional task metadata
        """
        self.name = name
        self.func = func
        self.description = description
        self.dependencies = dependencies or []
        self.metadata = metadata or {}
        self.status = TaskStatus.PENDING
        self.result = None
        self.error = None
        self.started_at: Optional[str] = None
        self.completed_at: Optional[str] = None

    def can_run(self, completed_tasks: List[str]) -> bool:
        """Check if this task can run based on dependencies.
        
        Args:
            completed_tasks: List of completed task names
            
        Returns:
            True if all dependencies are satisfied
        """
        return all(dep in completed_tasks for dep in self.dependencies)

    def execute(self, context: Dict[str, Any]) -> Any:
        """Execute the task.
        
        Args:
            context: Shared context for task execution
            
        Returns:
            Task result
        """
        self.status = TaskStatus.RUNNING
        self.started_at = datetime.now().isoformat()
        
        try:
            self.result = self.func(context)
            self.status = TaskStatus.COMPLETED
            return self.result
        except Exception as e:
            self.status = TaskStatus.FAILED
            self.error = str(e)
            raise
        finally:
            self.completed_at = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert task to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "dependencies": self.dependencies,
            "status": self.status.value,
            "result": self.result,
            "error": self.error,
            "started_at": self.started_at,
            "completed_at": self.completed_at,
            "metadata": self.metadata,
        }


class Pipeline:
    """Represents a workflow pipeline."""

    def __init__(self, name: str, description: str = ""):
        """Initialize a pipeline.
        
        Args:
            name: Pipeline name
            description: Pipeline description
        """
        self.name = name
        self.description = description
        self.tasks: Dict[str, Task] = {}
        self.execution_order: List[str] = []
        self.context: Dict[str, Any] = {}

    def add_task(self, task: Task) -> None:
        """Add a task to the pipeline.
        
        Args:
            task: Task to add
        """
        self.tasks[task.name] = task

    def remove_task(self, name: str) -> None:
        """Remove a task from the pipeline.
        
        Args:
            name: Task name
        """
        if name in self.tasks:
            del self.tasks[name]

    def validate(self) -> List[str]:
        """Validate pipeline configuration.
        
        Returns:
            List of validation errors (empty if valid)
        """
        errors = []
        
        # Check for circular dependencies
        for task_name, task in self.tasks.items():
            if self._has_circular_dependency(task_name):
                errors.append(f"Circular dependency detected for task: {task_name}")
        
        # Check for missing dependencies
        for task_name, task in self.tasks.items():
            for dep in task.dependencies:
                if dep not in self.tasks:
                    errors.append(f"Task '{task_name}' depends on missing task '{dep}'")
        
        return errors

    def _has_circular_dependency(self, task_name: str, visited: Optional[set] = None) -> bool:
        """Check if a task has circular dependencies."""
        if visited is None:
            visited = set()
        
        if task_name in visited:
            return True
        
        visited.add(task_name)
        task = self.tasks.get(task_name)
        
        if not task:
            return False
        
        for dep in task.dependencies:
            if self._has_circular_dependency(dep, visited.copy()):
                return True
        
        return False

    def execute(self, initial_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Execute the pipeline.
        
        Args:
            initial_context: Initial context for pipeline execution
            
        Returns:
            Execution results
        """
        self.context = initial_context or {}
        completed_tasks = []
        failed_tasks = []
        
        # Validate before execution
        errors = self.validate()
        if errors:
            return {
                "success": False,
                "errors": errors,
                "completed_tasks": [],
                "failed_tasks": [],
            }
        
        # Execute tasks in order
        while len(completed_tasks) + len(failed_tasks) < len(self.tasks):
            runnable_tasks = [
                task for task in self.tasks.values()
                if task.status == TaskStatus.PENDING and task.can_run(completed_tasks)
            ]
            
            if not runnable_tasks:
                # Check if we're stuck
                pending_tasks = [
                    task for task in self.tasks.values()
                    if task.status == TaskStatus.PENDING
                ]
                if pending_tasks:
                    # Mark remaining as skipped
                    for task in pending_tasks:
                        task.status = TaskStatus.SKIPPED
                break
            
            for task in runnable_tasks:
                try:
                    task.execute(self.context)
                    completed_tasks.append(task.name)
                    self.execution_order.append(task.name)
                except Exception:
                    failed_tasks.append(task.name)
        
        return {
            "success": len(failed_tasks) == 0,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "execution_order": self.execution_order,
            "context": self.context,
        }

    def get_status(self) -> Dict[str, Any]:
        """Get pipeline status."""
        status_counts = {status: 0 for status in TaskStatus}
        for task in self.tasks.values():
            status_counts[task.status] += 1
        
        return {
            "name": self.name,
            "description": self.description,
            "total_tasks": len(self.tasks),
            "status_counts": {k.value: v for k, v in status_counts.items()},
            "execution_order": self.execution_order,
            "tasks": {name: task.to_dict() for name, task in self.tasks.items()},
        }


class PipelineManager(Component):
    """Manages multiple pipelines for workflow automation.
    
    Streamlines AI development by automating complex workflows
    and making pipeline management accessible to all users.
    """

    def __init__(self, name: str = "pipeline", config: Optional[Dict[str, Any]] = None):
        """Initialize pipeline manager.
        
        Args:
            name: Component name
            config: Configuration dictionary
        """
        super().__init__(name, config)
        self.pipelines: Dict[str, Pipeline] = {}

    def initialize(self) -> bool:
        """Initialize the pipeline manager."""
        self._initialized = True
        return True

    def validate(self) -> bool:
        """Validate pipeline manager state."""
        for pipeline in self.pipelines.values():
            errors = pipeline.validate()
            if errors:
                return False
        return True

    def create_pipeline(self, name: str, description: str = "") -> Pipeline:
        """Create a new pipeline.
        
        Args:
            name: Pipeline name
            description: Pipeline description
            
        Returns:
            Created pipeline
        """
        pipeline = Pipeline(name, description)
        self.pipelines[name] = pipeline
        return pipeline

    def get_pipeline(self, name: str) -> Optional[Pipeline]:
        """Get a pipeline by name.
        
        Args:
            name: Pipeline name
            
        Returns:
            Pipeline or None if not found
        """
        return self.pipelines.get(name)

    def delete_pipeline(self, name: str) -> bool:
        """Delete a pipeline.
        
        Args:
            name: Pipeline name
            
        Returns:
            True if deleted, False if not found
        """
        if name in self.pipelines:
            del self.pipelines[name]
            return True
        return False

    def execute_pipeline(
        self,
        name: str,
        context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Execute a pipeline by name.
        
        Args:
            name: Pipeline name
            context: Initial context
            
        Returns:
            Execution results
        """
        pipeline = self.get_pipeline(name)
        if not pipeline:
            return {
                "success": False,
                "error": f"Pipeline not found: {name}",
            }
        
        return pipeline.execute(context)

    def list_pipelines(self) -> List[str]:
        """List all pipeline names.
        
        Returns:
            List of pipeline names
        """
        return list(self.pipelines.keys())

    def get_status(self) -> Dict[str, Any]:
        """Get pipeline manager status."""
        return {
            "enabled": self.is_enabled(),
            "initialized": self.is_initialized(),
            "pipelines_count": len(self.pipelines),
            "pipelines": {
                name: pipeline.get_status()
                for name, pipeline in self.pipelines.items()
            },
        }
