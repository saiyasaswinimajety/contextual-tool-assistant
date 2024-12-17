"""
Tests for agent interaction and intent-driven tool orchestration.
"""
import pytest
from src.agent import ContextualAgent
from src.persistence import StatePersistenceManager


def test_agent_pharma_tool_interaction(tmp_path):
    db_file = str(tmp_path / "agent_test.sqlite")
    mgr = StatePersistenceManager(db_path=db_file)
    agent = ContextualAgent(persistence_manager=mgr)
    
    response = agent.interact("session-eval-01", "Please verify status for batch BATCH-9021")
    assert response.session_id == "session-eval-01"
    assert len(response.tools_executed) == 1
    assert response.tools_executed[0].tool_name == "verify_pharma_batch_status"
    assert "APPROVED" in response.response
    
    # Verify persisted in database
    session = mgr.get_or_create_session("session-eval-01")
    assert len(session.messages) == 2
    assert session.total_tool_calls == 1


def test_agent_telemetry_tool_interaction(tmp_path):
    db_file = str(tmp_path / "agent_test.sqlite")
    mgr = StatePersistenceManager(db_path=db_file)
    agent = ContextualAgent(persistence_manager=mgr)
    
    response = agent.interact("session-eval-02", "Check telemetry for gateway GW-ORD-01")
    assert len(response.tools_executed) == 1
    assert response.tools_executed[0].tool_name == "query_network_gateway_telemetry"
    assert "HEALTHY" in response.response
