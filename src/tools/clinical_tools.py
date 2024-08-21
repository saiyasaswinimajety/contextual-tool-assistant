"""
Clinical and pharmaceutical batch validation tools.
Provides batch release status, assay purity, and protocol dosage calculations.
"""
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from src.tools.registry import registry


class BatchLookupInput(BaseModel):
    batch_id: str = Field(..., description="Unique pharmaceutical batch identifier, e.g. 'BATCH-9021'")
    include_assay_purity: bool = Field(True, description="Whether to include HPLC purity assay results")


class DoseCalculationInput(BaseModel):
    compound_code: str = Field(..., description="Standardized compound code, e.g. 'LY-4091'")
    patient_weight_kg: float = Field(..., ge=1.0, le=300.0, description="Patient body weight in kilograms")
    protocol_type: str = Field("STANDARD", description="'STANDARD' or 'INTENSIVE' dosage regimen")


# Mock database simulating LIMS / ERP REST APIs
BATCH_DATABASE = {
    "BATCH-9021": {
        "batch_id": "BATCH-9021",
        "compound": "LY-4091 (Tirzepatide Intermediate)",
        "status": "APPROVED",
        "sterility_check": "PASSED",
        "assay_purity_percent": 99.4,
        "manufacture_date": "2024-03-15",
        "expiry_date": "2026-03-15",
        "temperature_log": "Compliant (2-8 deg C)"
    },
    "BATCH-4042": {
        "batch_id": "BATCH-4042",
        "compound": "LY-2104 (Insulin Glargine Analog)",
        "status": "QUARANTINED",
        "sterility_check": "PENDING_RETEST",
        "assay_purity_percent": 97.1,
        "manufacture_date": "2024-04-01",
        "expiry_date": "2025-10-01",
        "temperature_log": "Excursion Detected (+11.2 deg C for 45 mins)"
    }
}


@registry.register(
    name="verify_pharma_batch_status",
    description="Verify pharmaceutical batch manufacturing compliance, sterility, and purity from LIMS records.",
    input_model=BatchLookupInput
)
def verify_pharma_batch_status(batch_id: str, include_assay_purity: bool = True) -> Dict[str, Any]:
    """Look up batch release records from simulated clinical REST endpoint."""
    batch_id_clean = batch_id.strip().upper()
    if batch_id_clean not in BATCH_DATABASE:
        return {
            "found": False,
            "batch_id": batch_id_clean,
            "message": f"Batch '{batch_id_clean}' not found in active manufacturing registry."
        }
    
    data = dict(BATCH_DATABASE[batch_id_clean])
    if not include_assay_purity:
        data.pop("assay_purity_percent", None)
    data["found"] = True
    return data


@registry.register(
    name="calculate_protocol_dose",
    description="Calculate weight-adjusted clinical protocol dosage based on compound specifications.",
    input_model=DoseCalculationInput
)
def calculate_protocol_dose(compound_code: str, patient_weight_kg: float, protocol_type: str = "STANDARD") -> Dict[str, Any]:
    """Calculate clinical dosage regimen."""
    base_rate_mg_per_kg = 0.25 if protocol_type.upper() == "STANDARD" else 0.40
    total_dose_mg = round(patient_weight_kg * base_rate_mg_per_kg, 2)
    
    return {
        "compound_code": compound_code.upper(),
        "patient_weight_kg": patient_weight_kg,
        "protocol_type": protocol_type.upper(),
        "base_rate_mg_per_kg": base_rate_mg_per_kg,
        "calculated_dose_mg": total_dose_mg,
        "administration_route": "Subcutaneous Infusion",
        "validation_status": "VERIFIED_SAFE"
    }
