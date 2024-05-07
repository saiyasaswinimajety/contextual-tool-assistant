"""
Structured schemas and data contracts for tool execution and state persistence.
Strict validation adhering to JSON Schema standards.
"""
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from pydantic import BaseModel, Field


class ToolParameterProperty(BaseModel):
    """JSON Schema property specification."""
    type: str
    description: str
    enum: Optional[List[str]] = None


class ToolSchema(BaseModel):
    """OpenAPI/JSON Schema definition for an executable tool."""
    name: str = Field(..., description="Unique tool name")
    description: str = Field(..., description="Semantic purpose of the tool")
    parameters: Dict[str, Any] = Field(..., description="JSON Schema object defining inputs")


class ToolExecutionRecord(BaseModel):
    """Auditable log entry of a single tool execution."""
    tool_name: str
    arguments: Dict[str, Any]
    result: Dict[str, Any]
    status: str = Field("success", description="'success' or 'error'")
    execution_time_ms: float
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class Message(BaseModel):
    """A conversational turn in the session."""
    role: str = Field(..., description="'user', 'assistant', 'system', or 'tool'")
    content: str
    tool_calls: Optional[List[Dict[str, Any]]] = None
    tool_results: Optional[List[ToolExecutionRecord]] = None
    timestamp: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())


class SessionState(BaseModel):
    """Persistent session state capturing conversation history and metadata."""
    session_id: str
    created_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())
    updated_at: str = Field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    messages: List[Message] = Field(default_factory=list)
    context_variables: Dict[str, Any] = Field(default_factory=dict)
    total_tool_calls: int = 0


class ChatRequest(BaseModel):
    """REST API input contract for agent interaction."""
    session_id: str = Field(..., description="Unique user session identifier")
    message: str = Field(..., description="User prompt or instruction")


class ChatResponse(BaseModel):
    """REST API response contract containing agent answer and executed tools."""
    session_id: str
    response: str
    tools_executed: List[ToolExecutionRecord] = Field(default_factory=list)
    execution_latency_ms: float
