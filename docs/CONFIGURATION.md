# Configuration Guide

## Overview

AIDeveloperTool uses YAML configuration files to manage project settings and component configurations.

## Project Configuration

The main project configuration is stored in `ai_project.yaml` in your project root.

### Basic Structure

```yaml
project:
  name: my-ai-project
  metadata:
    created_at: '2024-01-01T00:00:00'
    version: '0.1.0'
    description: 'My AI project description'

components:
  environment:
    type: EnvironmentChecker
    config:
      python_version: '3.8'
      required_packages:
        - numpy
        - pandas
        - scikit-learn
      required_tools:
        - git
        - docker
      directories:
        - data
        - models
        - notebooks
    enabled: true

  context:
    type: ContextManager
    config:
      storage_dir: .ai_context
      auto_save: true
    enabled: true

  feedback:
    type: FeedbackTracker
    config:
      log_dir: logs
      enable_console: true
      default_level: technical
    enabled: true

  pipeline:
    type: PipelineManager
    config: {}
    enabled: true
```

## Component Configurations

### EnvironmentChecker

```yaml
environment:
  type: EnvironmentChecker
  config:
    python_version: '3.9'  # Minimum Python version
    required_packages:      # Python packages
      - torch
      - transformers
    required_tools:         # System tools
      - git
      - docker
    directories:            # Required directories
      - data/raw
      - data/processed
      - models
```

### ContextManager

```yaml
context:
  type: ContextManager
  config:
    storage_dir: .ai_context  # Where to store contexts
    auto_save: true            # Auto-save on updates
```

### FeedbackTracker

```yaml
feedback:
  type: FeedbackTracker
  config:
    log_dir: logs              # Log directory
    enable_console: true       # Print to console
    default_level: technical   # technical/executive/creative
```

### PipelineManager

```yaml
pipeline:
  type: PipelineManager
  config: {}  # No specific configuration needed
```

## Environment Variables

You can override configuration with environment variables:

```bash
export AI_PROJECT_NAME="my-project"
export AI_LOG_DIR="logs"
export AI_CONTEXT_DIR=".ai_context"
```

## Examples

### Data Science Project

```yaml
project:
  name: data-science-project
  metadata:
    version: '1.0.0'

components:
  environment:
    type: EnvironmentChecker
    config:
      python_version: '3.9'
      required_packages:
        - pandas
        - numpy
        - scikit-learn
        - jupyter
      directories:
        - data/raw
        - data/processed
        - notebooks
        - models
```

### ML Production Project

```yaml
project:
  name: ml-production
  metadata:
    version: '2.0.0'

components:
  environment:
    type: EnvironmentChecker
    config:
      python_version: '3.10'
      required_packages:
        - fastapi
        - torch
        - transformers
      required_tools:
        - docker
        - kubectl
      directories:
        - models
        - api
```

## Best Practices

1. **Version Control**: Commit `ai_project.yaml` to version control
2. **Secrets**: Never store secrets in configuration files
3. **Environments**: Use different configs for dev/staging/prod
4. **Documentation**: Document custom configuration options
5. **Validation**: Run `aideveloper check` after config changes
