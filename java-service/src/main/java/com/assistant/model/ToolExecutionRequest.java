package com.assistant.model;

import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.util.Map;

public class ToolExecutionRequest {

    @NotBlank(message = "Tool name cannot be blank")
    private String toolName;

    @NotNull(message = "Arguments map is required")
    private Map<String, Object> arguments;

    private String sessionId;

    public ToolExecutionRequest() {}

    public ToolExecutionRequest(String toolName, Map<String, Object> arguments, String sessionId) {
        this.toolName = toolName;
        this.arguments = arguments;
        this.sessionId = sessionId;
    }

    public String getToolName() { return toolName; }
    public void setToolName(String toolName) { this.toolName = toolName; }

    public Map<String, Object> getArguments() { return arguments; }
    public void setArguments(Map<String, Object> arguments) { this.arguments = arguments; }

    public String getSessionId() { return sessionId; }
    public void setSessionId(String sessionId) { this.sessionId = sessionId; }
}
