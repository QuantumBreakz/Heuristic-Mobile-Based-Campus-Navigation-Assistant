package com.example.cvapp.models;

public class VisualizationConfigResponse {
    private String message;
    private VisualizationConfig config;

    public VisualizationConfigResponse(String message, VisualizationConfig config) {
        this.message = message;
        this.config = config;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public VisualizationConfig getConfig() {
        return config;
    }

    public void setConfig(VisualizationConfig config) {
        this.config = config;
    }
} 