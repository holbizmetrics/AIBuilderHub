# API Reference

## Core Module

### AIProject

Main project management class.

```python
from aidevelopertool import AIProject

project = AIProject(name: str, project_dir: Optional[Path] = None)
```

#### Methods

- `add_component(component: Component)` - Add a component to the project
- `remove_component(name: str)` - Remove a component
- `get_component(name: str) -> Optional[Component]` - Get component by name
- `initialize() -> bool` - Initialize project and all components
- `validate() -> Dict[str, bool]` - Validate all components
- `get_status() -> Dict[str, Any]` - Get comprehensive status
- `save_config(config_path: Optional[Path])` - Save configuration
- `load_config(config_path: Path) -> AIProject` - Load from config (class method)
- `cleanup()` - Clean up resources

### Component

Base class for all modular components.

```python
from aidevelopertool.core.component import Component

class MyComponent(Component):
    def initialize(self) -> bool: ...
    def validate(self) -> bool: ...
    def get_status(self) -> Dict[str, Any]: ...
```

#### Methods

- `initialize() -> bool` - Initialize the component (abstract)
- `validate() -> bool` - Validate component state (abstract)
- `get_status() -> Dict[str, Any]` - Get status (abstract)
- `enable()` - Enable the component
- `disable()` - Disable the component
- `is_enabled() -> bool` - Check if enabled
- `is_initialized() -> bool` - Check if initialized
- `cleanup()` - Clean up resources

## Setup Module

### EnvironmentChecker

Automates environment validation.

```python
from aidevelopertool.setup import EnvironmentChecker

checker = EnvironmentChecker(
    name: str = "environment",
    config: Optional[Dict[str, Any]] = None
)
```

#### Configuration

```python
config = {
    "python_version": "3.8",
    "required_packages": ["numpy", "pandas"],
    "required_tools": ["git", "docker"],
    "directories": ["data", "models"]
}
```

#### Methods

- `validate() -> bool` - Validate environment
- `auto_fix() -> Dict[str, bool]` - Attempt automatic fixes
- `get_report() -> str` - Get human-readable report

## Context Module

### ContextManager

Manages shared context across tasks.

```python
from aidevelopertool.context import ContextManager

mgr = ContextManager(
    name: str = "context",
    config: Optional[Dict[str, Any]] = None
)
```

#### Methods

- `create_context(context_id: str, data: Optional[Dict])` - Create context
- `get_context(context_id: str) -> Optional[Dict]` - Get context
- `update_context(context_id: str, data: Dict, merge: bool = True)` - Update context
- `delete_context(context_id: str) -> bool` - Delete context
- `save_context(context_id: str)` - Save to disk
- `load_context(context_id: str) -> bool` - Load from disk
- `list_contexts() -> List[str]` - List all contexts
- `share_between_contexts(source_id: str, target_id: str, keys: List[str]) -> bool` - Share data
- `temp_context(context_id: str)` - Temporary context (context manager)

## Feedback Module

### FeedbackTracker

Tracks actionable, explainable feedback.

```python
from aidevelopertool.feedback import FeedbackTracker, FeedbackLevel

tracker = FeedbackTracker(
    name: str = "feedback",
    config: Optional[Dict[str, Any]] = None
)
```

#### FeedbackLevel Enum

- `FeedbackLevel.TECHNICAL` - Detailed technical feedback
- `FeedbackLevel.EXECUTIVE` - High-level executive summary
- `FeedbackLevel.CREATIVE` - Narrative/visual feedback

#### Methods

- `log_event(message: str, level: str = "info", metadata: Optional[Dict] = None, category: str = "general")` - Log event
- `add_milestone(name: str, description: str, completed: bool = False, metadata: Optional[Dict] = None)` - Add milestone
- `complete_milestone(name: str) -> bool` - Complete milestone
- `update_metric(key: str, value: Any)` - Update metric
- `get_progress_summary(level: Optional[FeedbackLevel] = None) -> Dict` - Get progress summary
- `get_explainable_status(item: str) -> Dict` - Get explainable status
- `add_listener(callback: Callable)` - Add event listener
- `export_report(filepath: Optional[Path] = None) -> Path` - Export report

## Pipeline Module

### PipelineManager

Manages workflow pipelines.

```python
from aidevelopertool.pipeline import PipelineManager, Task, Pipeline

mgr = PipelineManager(
    name: str = "pipeline",
    config: Optional[Dict[str, Any]] = None
)
```

#### Methods

- `create_pipeline(name: str, description: str = "") -> Pipeline` - Create pipeline
- `get_pipeline(name: str) -> Optional[Pipeline]` - Get pipeline
- `delete_pipeline(name: str) -> bool` - Delete pipeline
- `execute_pipeline(name: str, context: Optional[Dict] = None) -> Dict` - Execute pipeline
- `list_pipelines() -> List[str]` - List all pipelines

### Pipeline

Represents a workflow pipeline.

```python
pipeline = Pipeline(name: str, description: str = "")
```

#### Methods

- `add_task(task: Task)` - Add task
- `remove_task(name: str)` - Remove task
- `validate() -> List[str]` - Validate pipeline
- `execute(initial_context: Optional[Dict] = None) -> Dict` - Execute pipeline
- `get_status() -> Dict` - Get status

### Task

Represents a single task in a pipeline.

```python
task = Task(
    name: str,
    func: Callable,
    description: str = "",
    dependencies: Optional[List[str]] = None,
    metadata: Optional[Dict[str, Any]] = None
)
```

#### Methods

- `can_run(completed_tasks: List[str]) -> bool` - Check if can run
- `execute(context: Dict) -> Any` - Execute task
- `to_dict() -> Dict` - Convert to dictionary

#### TaskStatus Enum

- `TaskStatus.PENDING` - Not started
- `TaskStatus.RUNNING` - Currently running
- `TaskStatus.COMPLETED` - Successfully completed
- `TaskStatus.FAILED` - Failed
- `TaskStatus.SKIPPED` - Skipped due to dependencies

## CLI

### Commands

```bash
# Initialize project
aideveloper init <name>

# Check environment
aideveloper check [--python-version VERSION] [--packages PACKAGES] [--tools TOOLS] [--directories DIRS] [--auto-fix]

# Show status
aideveloper status [--config PATH]

# Show feedback
aideveloper feedback [--level LEVEL] [--config PATH]
```
