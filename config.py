"""
Configuration settings for Contextual Tool Execution Assistant.
"""
import os
from dataclasses import dataclass

@dataclass
class AppConfig:
    # Model configuration
    MODEL_NAME: str = "gpt-4o-mini"
    TEMPERATURE: float = 0.0
    
    # State Persistence
    DB_PATH: str = os.getenv("STATE_DB_PATH", os.path.join(os.path.dirname(__file__), "agent_state.sqlite"))
    MAX_SESSION_HISTORY: int = 50
    
    # API Server
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    
    # Tool settings
    MOCK_LATENCY_SIMULATION: bool = False

config = AppConfig()
