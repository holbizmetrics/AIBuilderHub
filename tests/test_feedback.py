"""Tests for feedback tracker."""
import pytest
from pathlib import Path
from aidevelopertool.feedback.tracker import FeedbackTracker, FeedbackLevel


def test_feedback_tracker_creation(tmp_path):
    """Test feedback tracker creation."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    assert tracker.initialize()


def test_log_event(tmp_path):
    """Test logging events."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    tracker.initialize()
    
    tracker.log_event("Test event", level="info", category="test")
    assert len(tracker.events) == 1
    assert tracker.events[0]["message"] == "Test event"
    assert tracker.events[0]["level"] == "info"


def test_add_milestone(tmp_path):
    """Test adding milestones."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    tracker.initialize()
    
    tracker.add_milestone("test_milestone", "Test description", completed=False)
    assert len(tracker.milestones) == 1
    assert tracker.milestones[0]["name"] == "test_milestone"
    assert not tracker.milestones[0]["completed"]


def test_complete_milestone(tmp_path):
    """Test completing milestones."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    tracker.initialize()
    
    tracker.add_milestone("test", "Test milestone", completed=False)
    assert tracker.complete_milestone("test")
    assert tracker.milestones[0]["completed"]
    assert tracker.milestones[0]["completed_at"] is not None


def test_update_metric(tmp_path):
    """Test updating metrics."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    tracker.initialize()
    
    tracker.update_metric("accuracy", 0.95)
    assert "accuracy" in tracker.metrics
    assert tracker.metrics["accuracy"]["value"] == 0.95


def test_progress_summary(tmp_path):
    """Test progress summary generation."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    tracker.initialize()
    
    tracker.add_milestone("m1", "Milestone 1", completed=True)
    tracker.add_milestone("m2", "Milestone 2", completed=False)
    tracker.add_milestone("m3", "Milestone 3", completed=True)
    
    summary = tracker.get_progress_summary()
    assert summary["milestones"]["total"] == 3
    assert summary["milestones"]["completed"] == 2
    assert summary["milestones"]["percentage"] == pytest.approx(66.67, rel=0.1)


def test_technical_feedback(tmp_path):
    """Test technical-level feedback."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False,
        "default_level": "technical"
    })
    tracker.initialize()
    
    tracker.log_event("Event 1", level="info")
    tracker.add_milestone("m1", "Milestone", completed=True)
    
    summary = tracker.get_progress_summary(FeedbackLevel.TECHNICAL)
    assert "all_events" in summary
    assert "all_milestones" in summary


def test_executive_feedback(tmp_path):
    """Test executive-level feedback."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    tracker.initialize()
    
    tracker.add_milestone(
        "m1",
        "Important milestone",
        completed=True,
        metadata={"executive_visibility": True}
    )
    
    summary = tracker.get_progress_summary(FeedbackLevel.EXECUTIVE)
    assert "key_milestones" in summary


def test_creative_feedback(tmp_path):
    """Test creative-level feedback."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    tracker.initialize()
    
    tracker.add_milestone("m1", "Milestone 1", completed=True)
    tracker.add_milestone("m2", "Milestone 2", completed=False)
    
    summary = tracker.get_progress_summary(FeedbackLevel.CREATIVE)
    assert "story" in summary
    assert "milestones achieved" in summary["story"]


def test_explainable_status(tmp_path):
    """Test explainable status."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    tracker.initialize()
    
    tracker.add_milestone("test_milestone", "Test description", completed=True)
    
    status = tracker.get_explainable_status("test_milestone")
    assert status["type"] == "milestone"
    assert status["status"] == "completed"
    assert "explanation" in status


def test_export_report(tmp_path):
    """Test exporting feedback report."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    tracker.initialize()
    
    tracker.log_event("Test event", level="info")
    tracker.add_milestone("m1", "Milestone", completed=True)
    
    report_path = tracker.export_report()
    assert report_path.exists()
    assert report_path.suffix == ".json"


def test_listener(tmp_path):
    """Test event listeners."""
    tracker = FeedbackTracker(config={
        "log_dir": str(tmp_path / "logs"),
        "enable_console": False
    })
    tracker.initialize()
    
    events_received = []
    
    def listener(event):
        events_received.append(event)
    
    tracker.add_listener(listener)
    tracker.log_event("Test event", level="info")
    
    assert len(events_received) == 1
    assert events_received[0]["message"] == "Test event"
