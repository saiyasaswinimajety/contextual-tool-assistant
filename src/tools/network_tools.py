"""
Network telemetry and system reliability tools.
Monitors airline inflight broadband connectivity, satellite link latency, and gateway health.
"""
from typing import Dict, Any
from pydantic import BaseModel, Field
from src.tools.registry import registry


class GatewayTelemetryInput(BaseModel):
    gateway_id: str = Field(..., description="Satellite ground station or aircraft gateway ID, e.g. 'GW-ORD-01'")
    lookback_minutes: int = Field(15, ge=1, le=1440, description="Telemetry monitoring window in minutes")


# Mock telemetry database simulating Viasat Ka-band / terminal metrics
GATEWAY_METRICS = {
    "GW-ORD-01": {
        "gateway_id": "GW-ORD-01",
        "region": "US-Midwest",
        "status": "HEALTHY",
        "uptime_percent": 99.995,
        "round_trip_latency_ms": 142.3,
        "packet_loss_percent": 0.002,
        "active_aircraft_terminals": 184,
        "beam_carrier_snr_db": 14.8
    },
    "GW-LHR-02": {
        "gateway_id": "GW-LHR-02",
        "region": "Europe-West",
        "status": "DEGRADED",
        "uptime_percent": 98.420,
        "round_trip_latency_ms": 388.7,
        "packet_loss_percent": 1.450,
        "active_aircraft_terminals": 92,
        "beam_carrier_snr_db": 8.2
    }
}


@registry.register(
    name="query_network_gateway_telemetry",
    description="Retrieve live satellite broadband gateway health, packet loss, and latency telemetry.",
    input_model=GatewayTelemetryInput
)
def query_network_gateway_telemetry(gateway_id: str, lookback_minutes: int = 15) -> Dict[str, Any]:
    """Inspect real-time telemetry from simulated airline connectivity endpoint."""
    gw_clean = gateway_id.strip().upper()
    if gw_clean not in GATEWAY_METRICS:
        return {
            "found": False,
            "gateway_id": gw_clean,
            "status": "UNKNOWN",
            "message": f"Gateway '{gw_clean}' not found in active telecommunication registry."
        }
        
    metric = dict(GATEWAY_METRICS[gw_clean])
    metric["found"] = True
    metric["telemetry_window_minutes"] = lookback_minutes
    return metric
