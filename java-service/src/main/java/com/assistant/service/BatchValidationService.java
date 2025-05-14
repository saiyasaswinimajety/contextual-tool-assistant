package com.assistant.service;

import com.assistant.model.ToolExecutionRequest;
import com.assistant.model.ToolExecutionResponse;
import org.springframework.stereotype.Service;

import java.util.HashMap;
import java.util.Map;

@Service
public class BatchValidationService {

    public ToolExecutionResponse validateBatch(ToolExecutionRequest request) {
        long startTime = System.currentTimeMillis();
        Map<String, Object> args = request.getArguments();
        
        String batchId = (String) args.getOrDefault("batch_id", "UNKNOWN");
        Map<String, Object> result = new HashMap<>();
        
        if ("BATCH-9021".equalsIgnoreCase(batchId)) {
            result.put("batchId", "BATCH-9021");
            result.put("status", "APPROVED");
            result.put("sterility", "PASSED");
            result.put("purity", 99.4);
            result.put("releaseAuthorization", "21 CFR Part 11 Compliant");
        } else {
            result.put("batchId", batchId);
            result.put("status", "NOT_FOUND");
            result.put("message", "Batch record not found in Java validation service");
        }

        long elapsed = System.currentTimeMillis() - startTime;
        return new ToolExecutionResponse(request.getToolName(), "success", result, elapsed);
    }
}
