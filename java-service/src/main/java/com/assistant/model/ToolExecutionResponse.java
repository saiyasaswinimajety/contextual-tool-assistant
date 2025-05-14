package com.assistant.model;

import java.util.Map;

public class ToolExecutionResponse {

    private String toolName;
    private String status;
    private Map<String, Object> result;
    private long executionTimeMs;

    public ToolExecutionResponse() {}

    public ToolExecutionResponse(String toolName, String status, Map<String, Object> result, long executionTimeMs) {
        this.toolName = toolName;
        this.status = status;
        this.result = result;
        this.executionTimeMs = executionTimeMs;
    }

    public String getToolName() { return toolName; }
    public void setToolName(String toolName) { this.toolName = toolName; }

    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }

    public Map<String, Object> getResult() { return result; }
    public void setResult(Map<String, Object> result) { this.result = result; }

    public long getExecutionTimeMs() { return executionTimeMs; }
    public void setExecutionTimeMs(long executionTimeMs) { this.executionTimeMs = executionTimeMs; }
}
