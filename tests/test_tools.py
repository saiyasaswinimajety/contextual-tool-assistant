"""
Tests for tool schema validation and execution dispatch.
"""
import pytest
from src.tools.registry import registry
import src.tools.clinical_tools
import src.tools.network_tools
import src.tools.utility_tools


def test_tool_schemas_conformance():
    schemas = registry.get_tool_schemas()
    assert len(schemas) >= 4
    
    names = [s["function"]["name"] for s in schemas]
    assert "verify_pharma_batch_status" in names
    assert "calculate_protocol_dose" in names
    assert "query_network_gateway_telemetry" in names
    assert "convert_engineering_units" in names
    
    for s in schemas:
        fn = s["function"]
        assert "name" in fn
        assert "description" in fn
        assert "parameters" in fn
        assert fn["parameters"]["type"] == "object"


def test_clinical_batch_tool_execution():
    res = registry.execute_tool("verify_pharma_batch_status", {"batch_id": "BATCH-9021"})
    assert res.status == "success"
    assert res.result["found"] is True
    assert res.result["status"] == "APPROVED"
    assert res.execution_time_ms >= 0.0


def test_dose_calculation_tool_execution():
    res = registry.execute_tool(
        "calculate_protocol_dose",
        {"compound_code": "LY-4091", "patient_weight_kg": 80.0, "protocol_type": "STANDARD"}
    )
    assert res.status == "success"
    assert res.result["calculated_dose_mg"] == 20.0
    assert res.result["validation_status"] == "VERIFIED_SAFE"


def test_tool_schema_validation_error():
    # Pass invalid patient weight (< 1.0 kg)
    res = registry.execute_tool(
        "calculate_protocol_dose",
        {"compound_code": "LY-4091", "patient_weight_kg": -10.0}
    )
    assert res.status == "error"
    assert "error" in res.result
