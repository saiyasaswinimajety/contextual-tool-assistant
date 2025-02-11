"""
Streamlit Web Application: Contextual Tool Execution Assistant.
Interactive dashboard for tool execution, JSON schema inspection, and session state persistence.
"""
import streamlit as st
from src.agent import ContextualAgent
from src.tools.registry import registry

st.set_page_config(
    page_title="Contextual Tool Execution Assistant",
    page_icon="🛠️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        color: #1E3A8A;
        margin-bottom: 0.2rem;
    }
    .sub-header {
        font-size: 1.05rem;
        color: #4B5563;
        margin-bottom: 1.5rem;
    }
    .tool-badge {
        display: inline-block;
        padding: 0.25rem 0.6rem;
        border-radius: 0.375rem;
        font-size: 0.85rem;
        font-weight: 600;
        background-color: #ECFDF5;
        color: #065F46;
        border: 1px solid #A7F3D0;
        margin-right: 0.5rem;
    }
    .tool-box {
        background-color: #F8FAFC;
        border: 1px solid #E2E8F0;
        border-left: 4px solid #10B981;
        padding: 0.75rem 1rem;
        border-radius: 0.375rem;
        margin-top: 0.5rem;
        margin-bottom: 0.75rem;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def get_agent():
    return ContextualAgent()

agent = get_agent()

# Sidebar: Session & Tool Management
with st.sidebar:
    st.image("https://img.shields.io/badge/Architecture-LangChain%20%2B%20FastAPI%20%2B%20SQLite-blue?style=for-the-badge", use_column_width=True)
    st.markdown("### 🗂️ Persistent Session Management")
    
    # Session Selector
    sessions = agent.persistence.list_sessions()
    session_options = [s["session_id"] for s in sessions] if sessions else ["session-default"]
    
    selected_session = st.selectbox(
        "Active Session ID:",
        options=session_options + ["+ Create New Session"],
        index=0
    )
    
    if selected_session == "+ Create New Session":
        new_session_name = st.text_input("Enter new session ID:", value="session-pharma-01")
        active_session_id = new_session_name
    else:
        active_session_id = selected_session

    st.markdown(f"**Connected Database:** `agent_state.sqlite`")
    
    st.markdown("---")
    st.markdown("### 🛠️ Registered Tools")
    tool_schemas = registry.get_tool_schemas()
    st.metric("Active Tools", len(tool_schemas))
    for t in tool_schemas:
        st.markdown(f"- `{t['function']['name']}`")

    st.markdown("---")
    st.markdown("<small>Authored by **Sai Yasaswini Majety**</small>", unsafe_allow_html=True)


# Main Content Area
st.markdown('<div class="main-header">Contextual Tool Execution Assistant</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="sub-header">Modular Conversational Agent with REST API Tool-Calling, Structured State Persistence & Schema Validation</div>',
    unsafe_allow_html=True
)

st.markdown("""
<div style="margin-bottom: 1.5rem;">
    <span class="tool-badge">🛡️ Pydantic v2 Schema Validation</span>
    <span class="tool-badge">💾 SQLite ACID State Persistence</span>
    <span class="tool-badge">🌐 External REST Tool Integration</span>
    <span class="tool-badge">⚡ Real-Time Latency Telemetry</span>
    <span class="tool-badge">☕ Enterprise Java Adapter Ready</span>
</div>
""", unsafe_allow_html=True)

# Tabs: Interactive Chat vs Tool Schemas vs Session Audit
tab_chat, tab_schemas, tab_audit = st.tabs(["💬 Interactive Chat & Tool Execution", "📋 Tool Schema Registry", "📊 Session State & Audit Log"])

with tab_chat:
    # Quick action prompt seeds
    st.markdown("**Sample Directives:**")
    col_q1, col_q2, col_q3 = st.columns(3)
    with col_q1:
        if st.button("💊 Verify Batch BATCH-9021", use_container_width=True):
            st.session_state["preset_prompt"] = "Verify pharmaceutical manufacturing status for batch BATCH-9021"
    with col_q2:
        if st.button("📡 Check Gateway GW-ORD-01", use_container_width=True):
            st.session_state["preset_prompt"] = "Check telemetry status and latency for satellite gateway GW-ORD-01"
    with col_q3:
        if st.button("⚖️ Calculate Dose for LY-4091", use_container_width=True):
            st.session_state["preset_prompt"] = "Calculate protocol dosage of compound LY-4091 for an 80kg patient"

    preset = st.session_state.get("preset_prompt", "")
    user_input = st.text_input("Enter command or question for the agent:", value=preset, placeholder="e.g. Verify batch status for BATCH-9021...")

    if st.button("Send Directive", type="primary") and user_input:
        with st.spinner("Agent evaluating intent and executing required tools..."):
            chat_res = agent.interact(active_session_id, user_input)

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.metric("Total Execution Latency", f"{chat_res.execution_latency_ms} ms")
        with col_m2:
            st.metric("Tools Executed", len(chat_res.tools_executed))

        st.markdown("### 💬 Agent Response")
        st.success(chat_res.response)

        if chat_res.tools_executed:
            st.markdown("### ⚙️ Executed Tool Details & Validation Trace")
            for rec in chat_res.tools_executed:
                with st.expander(f"Tool: `{rec.tool_name}` (Status: {rec.status.upper()} in {rec.execution_time_ms}ms)", expanded=True):
                    st.json({
                        "tool_name": rec.tool_name,
                        "arguments": rec.arguments,
                        "result": rec.result,
                        "execution_time_ms": rec.execution_time_ms,
                        "timestamp": rec.timestamp
                    })

with tab_schemas:
    st.markdown("### OpenAPI / JSON Schemas for Tool Calling")
    st.write("All registered tools export deterministic JSON Schema contracts validated through Pydantic v2:")
    for t in tool_schemas:
        st.markdown(f"#### Tool: `{t['function']['name']}`")
        st.markdown(f"*{t['function']['description']}*")
        st.json(t["function"]["parameters"])

with tab_audit:
    st.markdown(f"### Persisted Session State for `{active_session_id}`")
    session_data = agent.persistence.get_or_create_session(active_session_id)
    
    st.markdown(f"- **Created At:** `{session_data.created_at}`")
    st.markdown(f"- **Last Updated:** `{session_data.updated_at}`")
    st.markdown(f"- **Total Messages in Session:** `{len(session_data.messages)}`")
    st.markdown(f"- **Total Tool Calls Tracked:** `{session_data.total_tool_calls}`")
    
    st.markdown("#### Message History & Audit Trail:")
    for idx, msg in enumerate(session_data.messages):
        with st.chat_message(msg.role):
            st.markdown(f"**[{msg.role.upper()}]** ({msg.timestamp})")
            st.write(msg.content)
            if msg.tool_results:
                st.caption(f"Executed {len(msg.tool_results)} tool(s)")
