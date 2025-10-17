"""Example: Basic usage of AIDeveloperTool components."""

from aidevelopertool import (
    AIProject,
    EnvironmentChecker,
    ContextManager,
    FeedbackTracker,
    PipelineManager,
)
from aidevelopertool.pipeline import Task


def main():
    """Demonstrate basic AIDeveloperTool usage."""
    
    # Create a new AI project
    print("=" * 60)
    print("Creating AI Project")
    print("=" * 60)
    
    project = AIProject("demo-project")
    
    # Add environment checker
    env_checker = EnvironmentChecker(config={
        "python_version": "3.8",
        "directories": ["data", "models", "outputs"],
    })
    project.add_component(env_checker)
    
    # Add context manager
    context_mgr = ContextManager(config={
        "storage_dir": ".demo_context",
        "auto_save": True,
    })
    project.add_component(context_mgr)
    
    # Add feedback tracker
    feedback = FeedbackTracker(config={
        "log_dir": "logs",
        "enable_console": True,
    })
    project.add_component(feedback)
    
    # Add pipeline manager
    pipeline_mgr = PipelineManager()
    project.add_component(pipeline_mgr)
    
    # Initialize project
    print("\nInitializing project...")
    if project.initialize():
        print("✓ Project initialized successfully\n")
    
    # Demonstrate environment checking
    print("=" * 60)
    print("Environment Check")
    print("=" * 60)
    
    env_checker.validate()
    print(env_checker.get_report())
    
    # Auto-fix any issues
    print("\nAttempting auto-fix...")
    fixes = env_checker.auto_fix()
    for fix_name, success in fixes.items():
        print(f"  {'✓' if success else '✗'} {fix_name}")
    
    # Demonstrate context management
    print("\n" + "=" * 60)
    print("Context Management")
    print("=" * 60)
    
    # Create a context for data processing
    context_mgr.create_context("data_processing", {
        "input_path": "data/raw",
        "output_path": "data/processed",
        "batch_size": 32,
    })
    print("✓ Created 'data_processing' context")
    
    # Create a context for model training
    context_mgr.create_context("model_training", {
        "model_type": "transformer",
        "epochs": 10,
        "learning_rate": 0.001,
    })
    print("✓ Created 'model_training' context")
    
    # Share data between contexts
    context_mgr.share_between_contexts(
        "data_processing",
        "model_training",
        ["output_path"]
    )
    print("✓ Shared context between tasks")
    
    # Show all contexts
    print(f"\nActive contexts: {', '.join(context_mgr.list_contexts())}")
    
    # Demonstrate feedback tracking
    print("\n" + "=" * 60)
    print("Feedback Tracking")
    print("=" * 60)
    
    # Add milestones
    feedback.add_milestone(
        "setup",
        "Project setup and environment validation",
        completed=True
    )
    
    feedback.add_milestone(
        "data_prep",
        "Data collection and preprocessing",
        completed=False
    )
    
    feedback.add_milestone(
        "model_dev",
        "Model development and training",
        completed=False
    )
    
    # Log some events
    feedback.log_event("Project initialization complete", level="success", category="setup")
    feedback.log_event("Starting data preprocessing", level="info", category="data")
    
    # Get progress summary
    summary = feedback.get_progress_summary()
    print(f"\nProgress: {summary['milestones']['completed']}/{summary['milestones']['total']} milestones")
    print(f"Completion: {summary['milestones']['percentage']:.1f}%")
    
    # Demonstrate pipeline management
    print("\n" + "=" * 60)
    print("Pipeline Management")
    print("=" * 60)
    
    # Create a simple data processing pipeline
    pipeline = pipeline_mgr.create_pipeline(
        "data_pipeline",
        "Data preprocessing and validation pipeline"
    )
    
    # Define tasks
    def load_data(context):
        print("  → Loading data...")
        context["data_loaded"] = True
        return "Data loaded"
    
    def validate_data(context):
        print("  → Validating data...")
        context["data_valid"] = True
        return "Data validated"
    
    def process_data(context):
        print("  → Processing data...")
        context["data_processed"] = True
        return "Data processed"
    
    # Add tasks to pipeline
    pipeline.add_task(Task("load", load_data, "Load raw data"))
    pipeline.add_task(Task(
        "validate",
        validate_data,
        "Validate data quality",
        dependencies=["load"]
    ))
    pipeline.add_task(Task(
        "process",
        process_data,
        "Process and transform data",
        dependencies=["validate"]
    ))
    
    # Execute pipeline
    print("\nExecuting pipeline...")
    results = pipeline_mgr.execute_pipeline("data_pipeline")
    
    if results["success"]:
        print(f"✓ Pipeline completed successfully")
        print(f"  Execution order: {' → '.join(results['execution_order'])}")
    
    # Show comprehensive status
    print("\n" + "=" * 60)
    print("Project Status")
    print("=" * 60)
    
    status = project.get_status()
    print(f"\nProject: {status['project']}")
    print(f"Initialized: {status['initialized']}")
    print(f"\nComponents ({len(status['components'])}):")
    for name, comp_status in status['components'].items():
        enabled = "✓" if comp_status.get("enabled") else "✗"
        print(f"  {enabled} {name}")
    
    # Save project configuration
    print("\n" + "=" * 60)
    print("Saving Configuration")
    print("=" * 60)
    
    project.save_config()
    print("✓ Project configuration saved to ai_project.yaml")
    
    # Cleanup
    project.cleanup()
    print("\n✓ Demo completed successfully!")


if __name__ == "__main__":
    main()
