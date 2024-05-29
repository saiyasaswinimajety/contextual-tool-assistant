"""
Dynamic Tool Registry with JSON Schema introspection and execution dispatch.
"""
import inspect
import time
from typing import Callable, Dict, Any, List, Type
from pydantic import BaseModel, create_model
from src.schema import ToolSchema, ToolExecutionRecord


class ToolRegistry:
    """
    Central catalog of executable tools with automated schema generation and validation.
    Conforms to OpenAI / LangChain function-calling standards.
    """
    def __init__(self):
        self._tools: Dict[str, Callable] = {}
        self._schemas: Dict[str, ToolSchema] = {}
        self._input_models: Dict[str, Type[BaseModel]] = {}

    def register(self, name: str, description: str, input_model: Type[BaseModel] = None):
        """Decorator to register a tool function with strict schema validation."""
        def decorator(func: Callable):
            self._tools[name] = func
            
            # Infer JSON Schema from Pydantic model or function docstring
            if input_model is not None:
                schema_dict = input_model.model_json_schema()
                self._input_models[name] = input_model
            else:
                schema_dict = {"type": "object", "properties": {}, "required": []}

            self._schemas[name] = ToolSchema(
                name=name,
                description=description.strip(),
                parameters=schema_dict
            )
            return func
        return decorator

    def get_tool_schemas(self) -> List[Dict[str, Any]]:
        """Export tools in OpenAI / LangChain function-calling format."""
        openai_tools = []
        for name, schema in self._schemas.items():
            openai_tools.append({
                "type": "function",
                "function": {
                    "name": schema.name,
                    "description": schema.description,
                    "parameters": schema.parameters
                }
            })
        return openai_tools

    def execute_tool(self, name: str, arguments: Dict[str, Any]) -> ToolExecutionRecord:
        """
        Execute tool with input validation and latency profiling.
        """
        if name not in self._tools:
            return ToolExecutionRecord(
                tool_name=name,
                arguments=arguments,
                result={"error": f"Tool '{name}' not found in registry"},
                status="error",
                execution_time_ms=0.0
            )

        start_time = time.perf_counter()
        try:
            # Validate through Pydantic model if registered
            if name in self._input_models:
                validated_model = self._input_models[name](**arguments)
                func_args = validated_model.model_dump()
            else:
                func_args = arguments

            result = self._tools[name](**func_args)
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0

            return ToolExecutionRecord(
                tool_name=name,
                arguments=arguments,
                result=result if isinstance(result, dict) else {"output": result},
                status="success",
                execution_time_ms=round(elapsed_ms, 2)
            )
        except Exception as e:
            elapsed_ms = (time.perf_counter() - start_time) * 1000.0
            return ToolExecutionRecord(
                tool_name=name,
                arguments=arguments,
                result={"error": str(e)},
                status="error",
                execution_time_ms=round(elapsed_ms, 2)
            )

registry = ToolRegistry()
