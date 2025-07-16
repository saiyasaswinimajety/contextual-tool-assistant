package com.assistant;

import com.assistant.model.ToolExecutionRequest;
import com.assistant.model.ToolExecutionResponse;
import com.assistant.service.BatchValidationService;
import org.junit.jupiter.api.Test;

import java.util.Map;

import static org.junit.jupiter.api.Assertions.*;

public class BatchValidationServiceTest {

    private final BatchValidationService service = new BatchValidationService();

    @Test
    public void testValidateBatchApproved() {
        ToolExecutionRequest request = new ToolExecutionRequest(
                "validateBatch",
                Map.of("batch_id", "BATCH-9021"),
                "session-java-01"
        );

        ToolExecutionResponse response = service.validateBatch(request);

        assertNotNull(response);
        assertEquals("success", response.getStatus());
        assertEquals("APPROVED", response.getResult().get("status"));
        assertEquals("21 CFR Part 11 Compliant", response.getResult().get("releaseAuthorization"));
    }

    @Test
    public void testValidateBatchNotFound() {
        ToolExecutionRequest request = new ToolExecutionRequest(
                "validateBatch",
                Map.of("batch_id", "NON-EXISTENT"),
                "session-java-02"
        );

        ToolExecutionResponse response = service.validateBatch(request);

        assertNotNull(response);
        assertEquals("NOT_FOUND", response.getResult().get("status"));
    }
}
