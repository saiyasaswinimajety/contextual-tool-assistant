"""
Utility tools for unit conversion and deterministic arithmetic.
"""
from typing import Dict, Any
from pydantic import BaseModel, Field
from src.tools.registry import registry


class UnitConversionInput(BaseModel):
    value: float = Field(..., description="Numeric value to convert")
    from_unit: str = Field(..., description="Source unit, e.g. 'kg', 'lb', 'celsius', 'fahrenheit', 'mbps', 'gbps'")
    to_unit: str = Field(..., description="Target unit")


@registry.register(
    name="convert_engineering_units",
    description="Convert numerical quantities between scientific, medical, and network engineering units.",
    input_model=UnitConversionInput
)
def convert_engineering_units(value: float, from_unit: str, to_unit: str) -> Dict[str, Any]:
    """Execute deterministic unit conversion."""
    f = from_unit.strip().lower()
    t = to_unit.strip().lower()
    
    # Weight
    if f in ["kg", "kilograms"] and t in ["lb", "pounds", "lbs"]:
        result = round(value * 2.20462, 3)
    elif f in ["lb", "pounds", "lbs"] and t in ["kg", "kilograms"]:
        result = round(value / 2.20462, 3)
    # Bandwidth
    elif f == "gbps" and t == "mbps":
        result = round(value * 1000.0, 2)
    elif f == "mbps" and t == "gbps":
        result = round(value / 1000.0, 4)
    # Temperature
    elif f == "celsius" and t == "fahrenheit":
        result = round((value * 9/5) + 32, 2)
    elif f == "fahrenheit" and t == "celsius":
        result = round((value - 32) * 5/9, 2)
    else:
        return {"error": f"Unsupported conversion pair from '{from_unit}' to '{to_unit}'"}

    return {
        "source_value": value,
        "from_unit": from_unit,
        "converted_value": result,
        "to_unit": to_unit
    }
