"""
FastAPI REST API server exposing agent endpoints and tool execution schemas.
"""
from typing import List, Dict, Any
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from src.schema import ChatRequest, ChatResponse, SessionState
from src.agent import ContextualAgent
from src.tools.registry import registry

app = FastAPI(
    title="Contextual Tool Execution Assistant API",
    description="Enterprise REST API for conversational agent with tool-calling and structured state persistence.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

agent = ContextualAgent()


@app.get("/health")
def health_check():
    """Service liveness probe."""
    return {"status": "HEALTHY", "service": "contextual-tool-assistant"}


@app.get("/api/tools", response_model=List[Dict[str, Any]])
def list_available_tools():
    """Retrieve OpenAPI function schemas for all registered executable tools."""
    return registry.get_tool_schemas()


@app.post("/api/chat", response_model=ChatResponse)
def execute_chat_turn(request: ChatRequest):
    """Interact with agent, execute required tools, and persist session turn."""
    try:
        response = agent.interact(request.session_id, request.message)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/sessions/{session_id}", response_model=SessionState)
def get_session_history(session_id: str):
    """Retrieve persistent conversation history and tool execution audit trail."""
    session = agent.persistence.get_or_create_session(session_id)
    return session


@app.get("/api/sessions")
def list_persisted_sessions():
    """List all persisted sessions with message and tool call counters."""
    return agent.persistence.list_sessions()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
