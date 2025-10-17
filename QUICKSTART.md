# Quick Start Guide

Get up and running with AIDeveloperTool in 5 minutes!

## Installation

### Option 1: From Source (Recommended for Development)

```bash
git clone https://github.com/holbizmetrics/AIBuilderHub.git
cd AIBuilderHub
pip install -e .
```

### Option 2: Production Install

```bash
pip install aidevelopertool
```

## Your First Project

### 1. Initialize a Project

```bash
# Create and navigate to your project directory
mkdir my-ai-project
cd my-ai-project

# Initialize the project
aideveloper init "My AI Project"
```

This creates:
- `ai_project.yaml` - Project configuration
- `.ai_context/` - Context storage directory
- `logs/` - Log files directory

### 2. Check Your Environment

```bash
# Basic environment check
aideveloper check

# Check specific requirements
aideveloper check --python-version 3.9 \
                  --packages numpy,pandas \
                  --directories data,models

# Auto-fix issues
aideveloper check --directories data,models,notebooks --auto-fix
```

### 3. View Project Status

```bash
aideveloper status
```

Output:
```
Project: My AI Project
Initialized: True

Components:
  ✓ environment
  ✓ context
  ✓ feedback
  ✓ pipeline
```

## Your First Script

Create `train_model.py`:

```python
from aidevelopertool import (
    AIProject,
    FeedbackTracker,
    PipelineManager,
)
from aidevelopertool.pipeline import Task

# Create project
project = AIProject("ml-training")

# Add feedback tracking
feedback = FeedbackTracker()
project.add_component(feedback)

# Add pipeline management
pipeline_mgr = PipelineManager()
project.add_component(pipeline_mgr)

# Initialize
project.initialize()

# Create pipeline
pipeline = pipeline_mgr.create_pipeline("training", "ML training workflow")

# Define tasks
def load_data(ctx):
    feedback.log_event("Loading data...", level="info")
    ctx["data"] = "loaded"
    return "Data loaded"

def train_model(ctx):
    feedback.log_event("Training model...", level="info")
    ctx["model"] = "trained"
    return "Model trained"

def evaluate(ctx):
    feedback.log_event("Evaluating...", level="success")
    return "Evaluation complete"

# Build pipeline
pipeline.add_task(Task("load", load_data))
pipeline.add_task(Task("train", train_model, dependencies=["load"]))
pipeline.add_task(Task("evaluate", evaluate, dependencies=["train"]))

# Execute
result = pipeline_mgr.execute_pipeline("training")
print(f"Success: {result['success']}")
```

Run it:
```bash
python train_model.py
```

## Common Use Cases

### For Data Scientists

```python
from aidevelopertool import AIProject, EnvironmentChecker

project = AIProject("data-science")

# Validate data science environment
env = EnvironmentChecker(config={
    "python_version": "3.9",
    "required_packages": ["pandas", "numpy", "scikit-learn", "jupyter"],
    "directories": ["data", "notebooks", "models"]
})
project.add_component(env)
project.initialize()

if not env.validate():
    print(env.get_report())
    env.auto_fix()
```

### For ML Engineers

```python
from aidevelopertool import AIProject, PipelineManager
from aidevelopertool.pipeline import Task

project = AIProject("ml-pipeline")
pipeline_mgr = PipelineManager()
project.add_component(pipeline_mgr)
project.initialize()

# Create production pipeline
pipeline = pipeline_mgr.create_pipeline("production", "ML production workflow")

# Add your tasks
pipeline.add_task(Task("preprocess", preprocess_data))
pipeline.add_task(Task("train", train_model, dependencies=["preprocess"]))
pipeline.add_task(Task("deploy", deploy_model, dependencies=["train"]))

# Execute
pipeline_mgr.execute_pipeline("production")
```

### For Team Leads

```python
from aidevelopertool import AIProject, FeedbackTracker
from aidevelopertool.feedback import FeedbackLevel

project = AIProject("team-project")
tracker = FeedbackTracker()
project.add_component(tracker)
project.initialize()

# Track team progress
tracker.add_milestone("data_prep", "Data preparation", completed=True)
tracker.add_milestone("model_dev", "Model development", completed=False)

# Get executive summary
summary = tracker.get_progress_summary(FeedbackLevel.EXECUTIVE)
print(f"Progress: {summary['milestones']['percentage']}%")
```

## Configuration

Edit `ai_project.yaml` to customize:

```yaml
project:
  name: my-project

components:
  environment:
    config:
      python_version: '3.9'
      required_packages:
        - numpy
        - pandas
      directories:
        - data
        - models
  
  feedback:
    config:
      default_level: technical
      enable_console: true
```

## Next Steps

1. **Read the Full Documentation**
   - [API Reference](docs/API.md)
   - [Configuration Guide](docs/CONFIGURATION.md)

2. **Explore Examples**
   - [Basic Usage](examples/basic_usage.py)
   - [Advanced Pipeline](examples/advanced_pipeline.py)

3. **Contribute**
   - [Contributing Guide](CONTRIBUTING.md)

## Need Help?

- Check the [README](README.md) for detailed information
- Look at [examples](examples/) for common patterns
- Review [tests](tests/) for usage patterns
- Open an issue on GitHub

## Quick Reference

### CLI Commands
```bash
aideveloper init <name>              # Initialize project
aideveloper check [options]          # Check environment
aideveloper status                   # Show status
aideveloper feedback [--level LEVEL] # Show progress
```

### Python API
```python
from aidevelopertool import (
    AIProject,           # Main project manager
    Component,           # Base component class
    EnvironmentChecker,  # Environment validation
    ContextManager,      # Context sharing
    FeedbackTracker,     # Progress tracking
    PipelineManager,     # Workflow automation
)
```

Happy coding! 🚀
