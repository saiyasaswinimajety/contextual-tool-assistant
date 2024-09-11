"""
Structured state persistence module using SQLite.
Guarantees thread-safe conversation history, tool audit trails, and context variables.
"""
import sqlite3
import json
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from src.schema import SessionState, Message, ToolExecutionRecord


class StatePersistenceManager:
    """
    Manages persistent conversational sessions and audit-ready tool execution logs.
    Utilizes ACID-compliant SQLite transactions with JSON serialization.
    """
    def __init__(self, db_path: str = "agent_state.sqlite"):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        """Create tables for sessions and message logs."""
        with self._get_connection() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS sessions (
                session_id TEXT PRIMARY KEY,
                created_at TEXT NOT NULL,
                updated_at TEXT NOT NULL,
                context_variables TEXT NOT NULL,
                total_tool_calls INTEGER DEFAULT 0
            );
            """)
            conn.execute("""
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                session_id TEXT NOT NULL,
                role TEXT NOT NULL,
                content TEXT NOT NULL,
                tool_calls TEXT,
                tool_results TEXT,
                timestamp TEXT NOT NULL,
                FOREIGN KEY (session_id) REFERENCES sessions (session_id)
            );
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_msg_session ON messages(session_id);")

    def _ensure_session_exists(self, conn: sqlite3.Connection, session_id: str):
        """Ensure session row exists in database."""
        cursor = conn.cursor()
        cursor.execute("SELECT session_id FROM sessions WHERE session_id = ?", (session_id,))
        if not cursor.fetchone():
            now = datetime.now(timezone.utc).isoformat()
            cursor.execute(
                "INSERT INTO sessions (session_id, created_at, updated_at, context_variables, total_tool_calls) VALUES (?, ?, ?, ?, ?)",
                (session_id, now, now, json.dumps({}), 0)
            )

    def get_or_create_session(self, session_id: str) -> SessionState:
        """Retrieve existing session or instantiate a new one."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            
            if not row:
                now = datetime.now(timezone.utc).isoformat()
                cursor.execute(
                    "INSERT INTO sessions (session_id, created_at, updated_at, context_variables, total_tool_calls) VALUES (?, ?, ?, ?, ?)",
                    (session_id, now, now, json.dumps({}), 0)
                )
                conn.commit()
                return SessionState(session_id=session_id, created_at=now, updated_at=now)

            # Load messages
            cursor.execute(
                "SELECT role, content, tool_calls, tool_results, timestamp FROM messages WHERE session_id = ? ORDER BY id ASC",
                (session_id,)
            )
            msg_rows = cursor.fetchall()
            messages = []
            for m in msg_rows:
                tool_calls = json.loads(m["tool_calls"]) if m["tool_calls"] else None
                tool_results = None
                if m["tool_results"]:
                    tool_results = [ToolExecutionRecord(**r) for r in json.loads(m["tool_results"])]
                messages.append(
                    Message(
                        role=m["role"],
                        content=m["content"],
                        tool_calls=tool_calls,
                        tool_results=tool_results,
                        timestamp=m["timestamp"]
                    )
                )

            return SessionState(
                session_id=row["session_id"],
                created_at=row["created_at"],
                updated_at=row["updated_at"],
                context_variables=json.loads(row["context_variables"]),
                total_tool_calls=row["total_tool_calls"],
                messages=messages
            )

    def append_message(self, session_id: str, message: Message):
        """Append a message turn to the session with tool execution details."""
        with self._get_connection() as conn:
            self._ensure_session_exists(conn, session_id)
            cursor = conn.cursor()
            now = datetime.now(timezone.utc).isoformat()
            
            tool_calls_json = json.dumps(message.tool_calls) if message.tool_calls else None
            tool_results_json = None
            if message.tool_results:
                tool_results_json = json.dumps([r.model_dump() for r in message.tool_results])
                
            cursor.execute(
                "INSERT INTO messages (session_id, role, content, tool_calls, tool_results, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                (session_id, message.role, message.content, tool_calls_json, tool_results_json, message.timestamp)
            )
            
            # Increment tool call counter if tool results exist
            tool_count_inc = len(message.tool_results) if message.tool_results else 0
            cursor.execute(
                "UPDATE sessions SET updated_at = ?, total_tool_calls = total_tool_calls + ? WHERE session_id = ?",
                (now, tool_count_inc, session_id)
            )
            conn.commit()

    def set_context_variable(self, session_id: str, key: str, value: Any):
        """Persist arbitrary context variables across conversation turns."""
        with self._get_connection() as conn:
            self._ensure_session_exists(conn, session_id)
            cursor = conn.cursor()
            cursor.execute("SELECT context_variables FROM sessions WHERE session_id = ?", (session_id,))
            row = cursor.fetchone()
            if row:
                ctx = json.loads(row["context_variables"])
                ctx[key] = value
                cursor.execute(
                    "UPDATE sessions SET context_variables = ?, updated_at = ? WHERE session_id = ?",
                    (json.dumps(ctx), datetime.now(timezone.utc).isoformat(), session_id)
                )
                conn.commit()

    def list_sessions(self) -> List[Dict[str, Any]]:
        """List summary of all persisted sessions."""
        with self._get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT session_id, created_at, updated_at, total_tool_calls FROM sessions ORDER BY updated_at DESC")
            return [dict(row) for row in cursor.fetchall()]

