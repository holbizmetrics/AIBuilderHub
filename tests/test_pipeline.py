"""Tests for pipeline manager."""
import pytest
from aidevelopertool.pipeline.manager import (
    PipelineManager,
    Pipeline,
    Task,
    TaskStatus
)


def test_task_creation():
    """Test task creation."""
    def dummy_func(context):
        return "result"
    
    task = Task("test_task", dummy_func, "Test description")
    assert task.name == "test_task"
    assert task.description == "Test description"
    assert task.status == TaskStatus.PENDING


def test_task_execution():
    """Test task execution."""
    def test_func(context):
        context["result"] = "success"
        return "completed"
    
    task = Task("test", test_func)
    context = {}
    
    result = task.execute(context)
    assert result == "completed"
    assert task.status == TaskStatus.COMPLETED
    assert context["result"] == "success"


def test_task_dependencies():
    """Test task dependency checking."""
    task = Task("task", lambda ctx: None, dependencies=["dep1", "dep2"])
    
    assert not task.can_run([])
    assert not task.can_run(["dep1"])
    assert task.can_run(["dep1", "dep2"])


def test_pipeline_creation():
    """Test pipeline creation."""
    pipeline = Pipeline("test_pipeline", "Test description")
    assert pipeline.name == "test_pipeline"
    assert pipeline.description == "Test description"
    assert len(pipeline.tasks) == 0


def test_pipeline_add_remove_task():
    """Test adding and removing tasks."""
    pipeline = Pipeline("test")
    task = Task("task1", lambda ctx: None)
    
    pipeline.add_task(task)
    assert len(pipeline.tasks) == 1
    
    pipeline.remove_task("task1")
    assert len(pipeline.tasks) == 0


def test_pipeline_validation():
    """Test pipeline validation."""
    pipeline = Pipeline("test")
    
    task1 = Task("task1", lambda ctx: None)
    task2 = Task("task2", lambda ctx: None, dependencies=["task1"])
    
    pipeline.add_task(task1)
    pipeline.add_task(task2)
    
    errors = pipeline.validate()
    assert len(errors) == 0


def test_pipeline_missing_dependency():
    """Test validation with missing dependency."""
    pipeline = Pipeline("test")
    
    task = Task("task", lambda ctx: None, dependencies=["missing"])
    pipeline.add_task(task)
    
    errors = pipeline.validate()
    assert len(errors) > 0
    assert "missing task" in errors[0]


def test_pipeline_execution():
    """Test pipeline execution."""
    pipeline = Pipeline("test")
    
    execution_order = []
    
    def task1_func(context):
        execution_order.append("task1")
        context["data"] = "processed"
        return "task1_done"
    
    def task2_func(context):
        execution_order.append("task2")
        assert context["data"] == "processed"
        return "task2_done"
    
    task1 = Task("task1", task1_func)
    task2 = Task("task2", task2_func, dependencies=["task1"])
    
    pipeline.add_task(task1)
    pipeline.add_task(task2)
    
    result = pipeline.execute()
    
    assert result["success"]
    assert len(result["completed_tasks"]) == 2
    assert execution_order == ["task1", "task2"]


def test_pipeline_execution_failure():
    """Test pipeline execution with failures."""
    pipeline = Pipeline("test")
    
    def failing_task(context):
        raise ValueError("Task failed")
    
    def dependent_task(context):
        return "should not execute"
    
    task1 = Task("failing", failing_task)
    task2 = Task("dependent", dependent_task, dependencies=["failing"])
    
    pipeline.add_task(task1)
    pipeline.add_task(task2)
    
    result = pipeline.execute()
    
    assert not result["success"]
    assert len(result["failed_tasks"]) == 1
    assert "failing" in result["failed_tasks"]


def test_pipeline_manager_creation():
    """Test pipeline manager creation."""
    mgr = PipelineManager()
    assert mgr.initialize()


def test_pipeline_manager_create_pipeline():
    """Test creating pipelines."""
    mgr = PipelineManager()
    mgr.initialize()
    
    pipeline = mgr.create_pipeline("test_pipeline", "Test description")
    assert pipeline.name == "test_pipeline"
    assert mgr.get_pipeline("test_pipeline") == pipeline


def test_pipeline_manager_delete_pipeline():
    """Test deleting pipelines."""
    mgr = PipelineManager()
    mgr.initialize()
    
    mgr.create_pipeline("test")
    assert mgr.get_pipeline("test") is not None
    
    assert mgr.delete_pipeline("test")
    assert mgr.get_pipeline("test") is None


def test_pipeline_manager_execute():
    """Test executing pipeline through manager."""
    mgr = PipelineManager()
    mgr.initialize()
    
    pipeline = mgr.create_pipeline("test")
    task = Task("task", lambda ctx: "result")
    pipeline.add_task(task)
    
    result = mgr.execute_pipeline("test")
    assert result["success"]


def test_pipeline_manager_list_pipelines():
    """Test listing pipelines."""
    mgr = PipelineManager()
    mgr.initialize()
    
    mgr.create_pipeline("pipeline1")
    mgr.create_pipeline("pipeline2")
    
    pipelines = mgr.list_pipelines()
    assert len(pipelines) == 2
    assert "pipeline1" in pipelines
    assert "pipeline2" in pipelines


def test_pipeline_manager_status():
    """Test pipeline manager status."""
    mgr = PipelineManager()
    mgr.initialize()
    
    mgr.create_pipeline("test")
    
    status = mgr.get_status()
    assert status["enabled"]
    assert status["initialized"]
    assert status["pipelines_count"] == 1
    assert "test" in status["pipelines"]
