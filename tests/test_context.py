"""Tests for context manager."""
import pytest
from pathlib import Path
from aidevelopertool.context.manager import ContextManager


def test_context_manager_creation(tmp_path):
    """Test context manager creation."""
    mgr = ContextManager(config={
        "storage_dir": str(tmp_path / "context"),
        "auto_save": False
    })
    assert mgr.initialize()


def test_create_context(tmp_path):
    """Test creating a new context."""
    mgr = ContextManager(config={
        "storage_dir": str(tmp_path / "context"),
        "auto_save": False
    })
    mgr.initialize()
    
    mgr.create_context("test_context", {"key": "value"})
    context = mgr.get_context("test_context")
    
    assert context is not None
    assert context["data"]["key"] == "value"
    assert "id" in context
    assert "created_at" in context


def test_update_context(tmp_path):
    """Test updating context."""
    mgr = ContextManager(config={
        "storage_dir": str(tmp_path / "context"),
        "auto_save": False
    })
    mgr.initialize()
    
    mgr.create_context("test", {"key1": "value1"})
    mgr.update_context("test", {"key2": "value2"})
    
    context = mgr.get_context("test")
    assert context["data"]["key1"] == "value1"
    assert context["data"]["key2"] == "value2"
    assert context["version"] == 2


def test_delete_context(tmp_path):
    """Test deleting context."""
    mgr = ContextManager(config={
        "storage_dir": str(tmp_path / "context"),
        "auto_save": False
    })
    mgr.initialize()
    
    mgr.create_context("test", {"key": "value"})
    assert mgr.get_context("test") is not None
    
    assert mgr.delete_context("test")
    assert mgr.get_context("test") is None


def test_share_between_contexts(tmp_path):
    """Test sharing data between contexts."""
    mgr = ContextManager(config={
        "storage_dir": str(tmp_path / "context"),
        "auto_save": False
    })
    mgr.initialize()
    
    mgr.create_context("source", {"shared_key": "shared_value", "other_key": "other"})
    mgr.create_context("target", {"existing_key": "existing"})
    
    assert mgr.share_between_contexts("source", "target", ["shared_key"])
    
    target = mgr.get_context("target")
    assert target["data"]["shared_key"] == "shared_value"
    assert target["data"]["existing_key"] == "existing"
    assert "other_key" not in target["data"]


def test_save_and_load_context(tmp_path):
    """Test saving and loading context from disk."""
    storage_dir = tmp_path / "context"
    mgr = ContextManager(config={
        "storage_dir": str(storage_dir),
        "auto_save": False
    })
    mgr.initialize()
    
    mgr.create_context("test", {"key": "value"})
    mgr.save_context("test")
    
    context_file = storage_dir / "test.json"
    assert context_file.exists()
    
    # Create new manager and load
    mgr2 = ContextManager(config={
        "storage_dir": str(storage_dir),
        "auto_save": False
    })
    mgr2.initialize()
    assert mgr2.load_context("test")
    
    context = mgr2.get_context("test")
    assert context["data"]["key"] == "value"


def test_temp_context(tmp_path):
    """Test temporary context."""
    mgr = ContextManager(config={
        "storage_dir": str(tmp_path / "context"),
        "auto_save": False
    })
    mgr.initialize()
    
    with mgr.temp_context("temp") as ctx:
        ctx["temp_data"] = "temp_value"
        assert mgr.get_context("temp") is not None
    
    # Should be deleted after context manager exits
    assert mgr.get_context("temp") is None


def test_list_contexts(tmp_path):
    """Test listing contexts."""
    mgr = ContextManager(config={
        "storage_dir": str(tmp_path / "context"),
        "auto_save": False
    })
    mgr.initialize()
    
    mgr.create_context("ctx1", {})
    mgr.create_context("ctx2", {})
    mgr.create_context("ctx3", {})
    
    contexts = mgr.list_contexts()
    assert len(contexts) == 3
    assert "ctx1" in contexts
    assert "ctx2" in contexts
    assert "ctx3" in contexts


def test_status_reporting(tmp_path):
    """Test context manager status reporting."""
    mgr = ContextManager(config={
        "storage_dir": str(tmp_path / "context"),
        "auto_save": True
    })
    mgr.initialize()
    
    mgr.create_context("test", {})
    
    status = mgr.get_status()
    assert status["enabled"]
    assert status["initialized"]
    assert status["contexts_count"] == 1
    assert status["auto_save"]
    assert "test" in status["contexts"]
