"""
Tests for SQLite structured state persistence.
"""
import pytest
from src.persistence import StatePersistenceManager
from src.schema import Message, ToolExecutionRecord


def test_session_creation_and_retrieval(tmp_path):
    db_file = str(tmp_path / "test_state.sqlite")
    mgr = StatePersistenceManager(db_path=db_file)
    
    session = mgr.get_or_create_session("session-test-01")
    assert session.session_id == "session-test-01"
    assert len(session.messages) == 0
    assert session.total_tool_calls == 0


def test_append_messages_with_tool_records(tmp_path):
    db_file = str(tmp_path / "test_state.sqlite")
    mgr = StatePersistenceManager(db_path=db_file)
    
    mgr.append_message("session-test-02", Message(role="user", content="Check batch status"))
    
    tool_rec = ToolExecutionRecord(
        tool_name="verify_pharma_batch_status",
        arguments={"batch_id": "BATCH-9021"},
        result={"status": "APPROVED"},
        status="success",
        execution_time_ms=12.5
    )
    mgr.append_message(
        "session-test-02",
        Message(role="assistant", content="Batch is approved.", tool_results=[tool_rec])
    )
    
    loaded = mgr.get_or_create_session("session-test-02")
    assert len(loaded.messages) == 2
    assert loaded.messages[0].role == "user"
    assert loaded.messages[1].role == "assistant"
    assert len(loaded.messages[1].tool_results) == 1
    assert loaded.messages[1].tool_results[0].tool_name == "verify_pharma_batch_status"
    assert loaded.total_tool_calls == 1


def test_context_variables(tmp_path):
    db_file = str(tmp_path / "test_state.sqlite")
    mgr = StatePersistenceManager(db_path=db_file)
    
    mgr.get_or_create_session("session-test-03")
    mgr.set_context_variable("session-test-03", "current_patient_id", "PATIENT-8812")
    
    loaded = mgr.get_or_create_session("session-test-03")
    assert loaded.context_variables.get("current_patient_id") == "PATIENT-8812"
