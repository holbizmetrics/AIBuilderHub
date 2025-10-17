# AIBuilderHub

**Universal AIDeveloperTool for Coders, Creators, and CEOs**

A modular framework for managing AI development projects that reduces friction through automated setup, shared context, actionable feedback, and streamlined pipeline management.

## 🎯 Key Features

- **Setup Automation**: Automatic environment checks and validation
- **Context Sharing**: Seamless information sharing between tasks
- **Actionable Feedback**: Progress tracking with explainable results for all user types
- **Pipeline Management**: Automated workflow orchestration
- **Modular Design**: Extensible architecture with clean interfaces
- **Multi-User Support**: Tailored views for coders, creators, and CEOs

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/holbizmetrics/AIBuilderHub.git
cd AIBuilderHub

# Install the package
pip install -e .

# Or install with development dependencies
pip install -e ".[dev]"
```

### Initialize a New Project

```bash
# Create a new AI project
aideveloper init my-ai-project

# This creates:
# - Project structure
# - Configuration file (ai_project.yaml)
# - Default components (environment checker, context manager, feedback tracker, pipeline manager)
```

### Check Environment

```bash
# Validate your development environment
aideveloper check --python-version 3.8 \
  --directories data,models,notebooks \
  --auto-fix

# Output:
# Environment Check Report
# ========================================
# ✓ PASS - python_version
# ✓ PASS - packages
# ✓ PASS - tools
# ✓ PASS - directories
```

### View Project Status

```bash
# See comprehensive project status
aideveloper status

# View feedback at different detail levels
aideveloper feedback --level executive
aideveloper feedback --level technical
aideveloper feedback --level creative
```

## 📦 Architecture

The AIDeveloperTool is built with a modular architecture consisting of:

### Core Components

#### 1. **Component Base Class**
All modules inherit from the `Component` base class, ensuring consistent behavior:

```python
from aidevelopertool.core.component import Component

class MyComponent(Component):
    def initialize(self) -> bool:
        # Setup logic
        return True
    
    def validate(self) -> bool:
        # Validation logic
        return True
    
    def get_status(self) -> dict:
        # Status reporting
        return {"status": "ok"}
```

#### 2. **AIProject Manager**
Central coordinator for all components:

```python
from aidevelopertool import AIProject

project = AIProject("my-project")
project.add_component(my_component)
project.initialize()
```

### Functional Modules

#### 1. **Setup Automation** (`aidevelopertool.setup`)
Automates environment validation and setup:

```python
from aidevelopertool.setup import EnvironmentChecker

checker = EnvironmentChecker(config={
    "python_version": "3.8",
    "required_packages": ["numpy", "pandas"],
    "required_tools": ["git", "docker"],
    "directories": ["data", "models"]
})

checker.initialize()
if checker.validate():
    print("Environment ready!")
else:
    print(checker.get_report())
    checker.auto_fix()  # Attempt automatic fixes
```

#### 2. **Context Management** (`aidevelopertool.context`)
Share state and information between tasks:

```python
from aidevelopertool.context import ContextManager

context_mgr = ContextManager()
context_mgr.initialize()

# Create and update contexts
context_mgr.create_context("training", {
    "model": "gpt-4",
    "dataset": "custom-data",
    "hyperparameters": {"lr": 0.001}
})

# Share between contexts
context_mgr.share_between_contexts(
    "training", "evaluation", ["model", "dataset"]
)

# Use temporary contexts
with context_mgr.temp_context("temp_task") as ctx:
    ctx["result"] = process_data()
```

#### 3. **Feedback Tracking** (`aidevelopertool.feedback`)
Actionable, explainable progress tracking for all user types:

```python
from aidevelopertool.feedback import FeedbackTracker, FeedbackLevel

tracker = FeedbackTracker()
tracker.initialize()

# Log events
tracker.log_event("Model training started", level="info", category="training")

# Track milestones
tracker.add_milestone(
    "data_prep",
    "Data preparation and cleaning completed",
    completed=True
)

# Get tailored summaries
exec_summary = tracker.get_progress_summary(FeedbackLevel.EXECUTIVE)
tech_summary = tracker.get_progress_summary(FeedbackLevel.TECHNICAL)

# Get explainable status
status = tracker.get_explainable_status("data_prep")
print(status["explanation"])
```

#### 4. **Pipeline Management** (`aidevelopertool.pipeline`)
Orchestrate complex workflows with dependencies:

```python
from aidevelopertool.pipeline import PipelineManager, Task

pipeline_mgr = PipelineManager()
pipeline_mgr.initialize()

# Create a pipeline
pipeline = pipeline_mgr.create_pipeline("ml-workflow", "ML training pipeline")

# Define tasks
def prepare_data(context):
    context["data"] = load_and_clean_data()
    return "Data prepared"

def train_model(context):
    model = train(context["data"])
    context["model"] = model
    return "Model trained"

def evaluate_model(context):
    results = evaluate(context["model"])
    return results

# Add tasks with dependencies
pipeline.add_task(Task("prepare", prepare_data, "Prepare training data"))
pipeline.add_task(Task("train", train_model, "Train the model", dependencies=["prepare"]))
pipeline.add_task(Task("evaluate", evaluate_model, "Evaluate model", dependencies=["train"]))

# Execute pipeline
results = pipeline_mgr.execute_pipeline("ml-workflow")
print(f"Success: {results['success']}")
print(f"Completed: {results['completed_tasks']}")
```

## 💡 Usage Examples

### For Coders

```python
from aidevelopertool import AIProject, EnvironmentChecker, FeedbackTracker

# Set up project with technical detail
project = AIProject("ml-service")

# Detailed environment validation
env = EnvironmentChecker(config={
    "python_version": "3.9",
    "required_packages": ["torch", "transformers", "fastapi"],
    "required_tools": ["git", "docker", "kubectl"]
})
project.add_component(env)

# Detailed technical feedback
feedback = FeedbackTracker(config={"default_level": "technical"})
project.add_component(feedback)

project.initialize()

# Get detailed technical status
status = project.get_status()
print(f"All components: {status['components']}")
```

### For Creators

```python
from aidevelopertool import AIProject, FeedbackTracker
from aidevelopertool.feedback import FeedbackLevel

# Set up project with creative narrative
project = AIProject("ai-art-generator")

# Creative feedback with storytelling
feedback = FeedbackTracker(config={"default_level": "creative"})
project.add_component(feedback)

feedback.add_milestone("concept", "Conceptual design complete", completed=True)
feedback.add_milestone("prototype", "Working prototype created", completed=True)
feedback.add_milestone("refinement", "Refining user experience")

# Get narrative progress
summary = feedback.get_progress_summary(FeedbackLevel.CREATIVE)
print(summary["story"])  # "Journey so far: 2 milestones achieved | Next up: refinement - Refining user experience"
```

### For CEOs

```python
from aidevelopertool import AIProject, FeedbackTracker
from aidevelopertool.feedback import FeedbackLevel

# Set up project with executive summary
project = AIProject("ai-product-launch")

# High-level executive feedback
feedback = FeedbackTracker(config={"default_level": "executive"})
project.add_component(feedback)

# Track key business milestones
feedback.add_milestone(
    "mvp",
    "Minimum viable product completed",
    completed=True,
    metadata={"executive_visibility": True}
)

# Get executive summary
summary = feedback.get_progress_summary(FeedbackLevel.EXECUTIVE)
print(f"Progress: {summary['milestones']['percentage']}%")
```

## 🧪 Testing

```bash
# Run tests
pytest tests/

# Run with coverage
pytest --cov=aidevelopertool tests/

# Run specific test
pytest tests/test_core.py -v
```

## 🔧 Development

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run linter
flake8 src/

# Run type checker
mypy src/

# Format code
black src/ tests/
```

## 📚 Documentation

### Module Structure

```
src/aidevelopertool/
├── __init__.py          # Main package exports
├── cli.py               # Command-line interface
├── core/
│   ├── component.py     # Base component interface
│   └── project.py       # Project management
├── setup/
│   └── environment.py   # Environment automation
├── context/
│   └── manager.py       # Context sharing
├── feedback/
│   └── tracker.py       # Feedback tracking
└── pipeline/
    └── manager.py       # Pipeline orchestration
```

### Configuration

Projects are configured via `ai_project.yaml`:

```yaml
project:
  name: my-ai-project
  metadata:
    created_at: '2024-01-01T00:00:00'
    version: '0.1.0'

components:
  environment:
    type: EnvironmentChecker
    config:
      python_version: '3.8'
      required_packages:
        - numpy
        - pandas
    enabled: true

  context:
    type: ContextManager
    config:
      storage_dir: .ai_context
      auto_save: true
    enabled: true
```

## 🤝 Contributing

Contributions are welcome! The modular architecture makes it easy to add new components:

1. Create a new module inheriting from `Component`
2. Implement required methods: `initialize()`, `validate()`, `get_status()`
3. Add tests
4. Update documentation

## 📄 License

This project is part of AIBuilderHub.

## 🎯 Design Principles

1. **Modularity**: Each component is independent and can be used separately
2. **Extensibility**: Easy to add new components and functionality
3. **Clarity**: Explainable feedback at all levels
4. **Automation**: Reduce manual setup and configuration
5. **Collaboration**: Support for multiple user types with different needs
6. **Minimal Friction**: Streamline common AI development workflows
