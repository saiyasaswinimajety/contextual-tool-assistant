# Contextual Tool Execution Assistant (`contextual-tool-assistant`)

[![CI Pipeline](https://github.com/saiyasaswinimajety/contextual-tool-assistant/actions/workflows/ci.yml/badge.svg)](https://github.com/saiyasaswinimajety/contextual-tool-assistant/actions)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue.svg)](https://www.python.org/)
[![Java 17+](https://img.shields.io/badge/Java-17%2B-orange.svg)](https://www.oracle.com/java/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.111%2B-teal.svg)](https://fastapi.tiangolo.com/)
[![LangChain](https://img.shields.io/badge/LangChain-Agent-orange.svg)](https://www.langchain.com/)
[![Pydantic v2](https://img.shields.io/badge/Schema-Pydantic%20v2-green.svg)](https://docs.pydantic.dev/)
[![SQLite](https://img.shields.io/badge/Persistence-SQLite%20ACID-lightblue.svg)](https://www.sqlite.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

An enterprise-grade modular conversational agent integrating **REST API tool-calling capabilities**, **Pydantic v2 JSON Schema validation**, and **ACID-compliant structured state persistence** with cross-language support for **Python** and **Java (Spring Boot)**.

---

## 🎯 Architectural Overview

```
                           ┌───────────────────────────┐
                           │ User / Client Application │
                           └─────────────┬─────────────┘
                                         │  HTTP / REST
                                         ▼
                           ┌───────────────────────────┐
                           │    FastAPI Gateway &      │
                           │   Streamlit Web Client    │
                           └─────────────┬─────────────┘
                                         │
                                         ▼
                           ┌───────────────────────────┐
                           │ Contextual Agent Engine   │
                           │ (LangChain / OpenAI API)  │
                           └───────┬───────────┬───────┘
                                   │           │
                 Tool Invocations  │           │ State Reads/Writes
                                   ▼           ▼
        ┌─────────────────────────────┐     ┌─────────────────────────────┐
        │ Dynamic Tool Registry       │     │ State Persistence Manager   │
        │ • Pydantic Schema Validator │     │ • SQLite ACID Storage       │
        │ • Real-Time Latency Profiler│     │ • Conversation Turns        │
        └──────────────┬──────────────┘     │ • Tool Audit Trail Logs     │
                       │                    └─────────────────────────────┘
      ┌────────────────┼────────────────┐
      ▼                ▼                ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Pharma LIMS  │ │ SRE Network  │ │ Engineering  │
│  Batch API   │ │ Telemetry API│ │ Unit Convert │
└──────────────┘ └──────────────┘ └──────────────┘
```

---

## ⚡ Key Engineering Capabilities

1. **Modular Dynamic Tool Registry with Schema Validation:**
   - Every executable tool defines its interface using Pydantic v2 models, automatically compiled into OpenAPI and JSON Schema specifications.
   - Enforces strict parameter boundary checks (ranges, regex patterns, types) before tool execution dispatch.

2. **ACID-Compliant Structured State Persistence:**
   - Conversation sessions, message sequences, and tool execution logs are persisted across process restarts via SQLite (`agent_state.sqlite`).
   - Maintains an auditable execution trace recording tool names, JSON input payloads, execution outputs, and millisecond latency timers.

3. **Multi-Domain Enterprise Tool Suites:**
   - **Pharmaceutical / Clinical Batch Validation:** Queries batch release status, HPLC assay purity, sterility certifications, and cold-chain temperature excursion logs.
   - **Clinical Protocol Dose Calculator:** Computes weight-adjusted protocol dosages based on compound specifications.
   - **Satellite Network Telemetry (SRE):** Monitors real-time gateway availability, packet loss, and round-trip latency.
   - **Engineering Unit Conversion:** High-precision scientific and network bandwidth conversions.

4. **Dual Python & Java Enterprise Interoperability:**
   - **Python Core:** FastAPI REST service + LangChain agent runtime with deterministic fallback.
   - **Java Enterprise Module (`java-service`):** Spring Boot microservice implementing `BatchValidationService` with Jakarta Bean Validation and Jackson JSON mapping.

---

## 📁 Repository Structure

```
contextual-tool-assistant/
├── app.py                      # Interactive Streamlit UI
├── server.py                   # FastAPI REST API server
├── config.py                   # Runtime configuration parameters
├── requirements.txt            # Production dependencies
├── Dockerfile                  # Container definition
├── docker-compose.yml          # Container orchestration
├── src/
│   ├── __init__.py
│   ├── agent.py                # Conversational agent & tool coordinator
│   ├── persistence.py          # SQLite structured state store
│   ├── schema.py               # Pydantic data contracts
│   └── tools/
│       ├── __init__.py
│       ├── registry.py         # Dynamic registry & schema generator
│       ├── clinical_tools.py   # Pharma & batch status verification
│       ├── network_tools.py    # Satellite network telemetry
│       └── utility_tools.py    # Unit conversion & calculations
├── tests/
│   ├── __init__.py
│   ├── test_agent.py           # Agent interaction test suite
│   ├── test_tools.py           # Tool execution & schema validation tests
│   └── test_persistence.py    # SQLite state persistence tests
└── java-service/               # Enterprise Spring Boot module
    ├── pom.xml                 # Maven configuration
    └── src/
        ├── main/java/com/assistant/
        │   ├── ContextualToolApplication.java
        │   ├── model/          # DTOs with Jakarta validation
        │   └── service/        # Java batch verification service
        └── test/java/com/assistant/
            └── BatchValidationServiceTest.java
```

---

## 🛠️ Quickstart Installation

### Option 1: Python Agent & API Server

```bash
# Clone the repository
git clone https://github.com/saiyasaswinimajety/contextual-tool-assistant.git
cd contextual-tool-assistant

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run pytest test suite
pytest -v

# Start FastAPI server (runs on port 8000)
python server.py

# Launch Streamlit interactive dashboard (runs on port 8501)
streamlit run app.py
```

### Option 2: Java Spring Boot Service

```bash
cd java-service
mvn clean test
mvn spring-boot:run
```

---

## 📡 REST API Specifications

### 1. Interact with Agent
```http
POST /api/chat
Content-Type: application/json

{
  "session_id": "session-pharma-01",
  "message": "Verify status for batch BATCH-9021"
}
```

**Response:**
```json
{
  "session_id": "session-pharma-01",
  "response": "Verified batch record for BATCH-9021:\n- Compound: LY-4091 (Tirzepatide Intermediate)\n- Status: APPROVED\n- Sterility Check: PASSED\n- Assay Purity: 99.4%",
  "tools_executed": [
    {
      "tool_name": "verify_pharma_batch_status",
      "arguments": { "batch_id": "BATCH-9021" },
      "result": { "status": "APPROVED", "assay_purity_percent": 99.4 },
      "status": "success",
      "execution_time_ms": 1.2
    }
  ],
  "execution_latency_ms": 14.8
}
```

### 2. Inspect Tool Schemas
```http
GET /api/tools
```

### 3. Retrieve Session State & Audit History
```http
GET /api/sessions/session-pharma-01
```

---

## 🧪 Testing & Validation

The test suite validates:
- Pydantic schema validation boundaries and type enforcement.
- ACID-compliant SQLite session state and message recording.
- Real-time latency measurement and status reporting.
- Java enterprise batch validation service with JUnit 5.

```bash
# Python tests
pytest -v --durations=10

# Java tests
cd java-service && mvn test
```

---

## 👩‍💻 Author

**Sai Yasaswini Majety**  
- **LinkedIn:** [linkedin.com/in/saiyasaswinimajety](https://www.linkedin.com/in/saiyasaswinimajety)  
- **GitHub:** [github.com/saiyasaswinimajety](https://github.com/saiyasaswinimajety)  
- **Portfolio:** [saiyasaswini.me](https://saiyasaswini.me/)  

---

## 📄 License

Distributed under the MIT License. See [LICENSE](LICENSE) for details.

