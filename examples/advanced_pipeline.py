"""Example: Advanced pipeline with complex workflows."""

from aidevelopertool import AIProject, PipelineManager, FeedbackTracker
from aidevelopertool.pipeline import Task
import time


def simulate_ml_workflow():
    """Demonstrate a complete ML workflow using pipelines."""
    
    print("=" * 70)
    print("Advanced ML Workflow Pipeline Example")
    print("=" * 70)
    
    # Set up project
    project = AIProject("ml-workflow-demo")
    
    # Add feedback tracker
    feedback = FeedbackTracker(config={"enable_console": True})
    project.add_component(feedback)
    
    # Add pipeline manager
    pipeline_mgr = PipelineManager()
    project.add_component(pipeline_mgr)
    
    project.initialize()
    
    # Create ML pipeline
    ml_pipeline = pipeline_mgr.create_pipeline(
        "ml_training",
        "Complete ML training workflow"
    )
    
    # Define workflow tasks
    def collect_data(context):
        feedback.log_event("Collecting training data", level="info", category="data")
        time.sleep(0.5)  # Simulate work
        context["dataset_size"] = 10000
        feedback.update_metric("dataset_size", 10000)
        return "Collected 10,000 samples"
    
    def preprocess_data(context):
        feedback.log_event("Preprocessing data", level="info", category="data")
        time.sleep(0.5)
        context["features_extracted"] = 256
        feedback.update_metric("features", 256)
        return "Extracted 256 features"
    
    def split_data(context):
        feedback.log_event("Splitting train/test sets", level="info", category="data")
        time.sleep(0.3)
        context["train_size"] = int(context["dataset_size"] * 0.8)
        context["test_size"] = int(context["dataset_size"] * 0.2)
        return "Split into train/test"
    
    def train_model(context):
        feedback.log_event("Training model", level="info", category="training")
        time.sleep(1.0)  # Simulate training
        context["model_trained"] = True
        context["training_accuracy"] = 0.92
        feedback.update_metric("training_accuracy", 0.92)
        return "Model trained (92% accuracy)"
    
    def validate_model(context):
        feedback.log_event("Validating model", level="info", category="validation")
        time.sleep(0.5)
        context["validation_accuracy"] = 0.89
        feedback.update_metric("validation_accuracy", 0.89)
        return "Validation complete (89% accuracy)"
    
    def test_model(context):
        feedback.log_event("Testing model", level="info", category="testing")
        time.sleep(0.5)
        context["test_accuracy"] = 0.87
        feedback.update_metric("test_accuracy", 0.87)
        return "Testing complete (87% accuracy)"
    
    def generate_report(context):
        feedback.log_event("Generating report", level="info", category="reporting")
        time.sleep(0.3)
        context["report_generated"] = True
        return "Report generated"
    
    # Build pipeline with dependencies
    ml_pipeline.add_task(Task(
        "collect",
        collect_data,
        "Collect training data"
    ))
    
    ml_pipeline.add_task(Task(
        "preprocess",
        preprocess_data,
        "Preprocess and clean data",
        dependencies=["collect"]
    ))
    
    ml_pipeline.add_task(Task(
        "split",
        split_data,
        "Split into train/test sets",
        dependencies=["preprocess"]
    ))
    
    ml_pipeline.add_task(Task(
        "train",
        train_model,
        "Train the model",
        dependencies=["split"]
    ))
    
    ml_pipeline.add_task(Task(
        "validate",
        validate_model,
        "Validate model performance",
        dependencies=["train"]
    ))
    
    ml_pipeline.add_task(Task(
        "test",
        test_model,
        "Test model on test set",
        dependencies=["train"]
    ))
    
    ml_pipeline.add_task(Task(
        "report",
        generate_report,
        "Generate final report",
        dependencies=["validate", "test"]
    ))
    
    # Add milestones
    feedback.add_milestone("data_ready", "Data collection and preprocessing")
    feedback.add_milestone("model_trained", "Model training complete")
    feedback.add_milestone("model_evaluated", "Model evaluation complete")
    
    # Execute pipeline
    print("\nExecuting ML pipeline...\n")
    results = pipeline_mgr.execute_pipeline("ml_training")
    
    # Update milestones based on results
    if "preprocess" in results["completed_tasks"]:
        feedback.complete_milestone("data_ready")
    
    if "train" in results["completed_tasks"]:
        feedback.complete_milestone("model_trained")
    
    if "test" in results["completed_tasks"]:
        feedback.complete_milestone("model_evaluated")
    
    # Display results
    print("\n" + "=" * 70)
    print("Pipeline Execution Results")
    print("=" * 70)
    
    print(f"\nSuccess: {results['success']}")
    print(f"Completed Tasks: {len(results['completed_tasks'])}")
    print(f"Failed Tasks: {len(results['failed_tasks'])}")
    print(f"\nExecution Order:")
    for i, task_name in enumerate(results['execution_order'], 1):
        print(f"  {i}. {task_name}")
    
    # Show feedback summary
    print("\n" + "=" * 70)
    print("Progress Summary")
    print("=" * 70)
    
    summary = feedback.get_progress_summary()
    print(f"\nMilestones: {summary['milestones']['completed']}/{summary['milestones']['total']}")
    print(f"Completion: {summary['milestones']['percentage']:.1f}%")
    
    print("\nKey Metrics:")
    for metric_name, metric_data in summary['metrics'].items():
        print(f"  - {metric_name}: {metric_data['value']}")
    
    # Export report
    report_path = feedback.export_report()
    print(f"\n✓ Detailed report exported to: {report_path}")
    
    # Cleanup
    project.cleanup()
    print("\n✓ Workflow completed successfully!")


if __name__ == "__main__":
    simulate_ml_workflow()
