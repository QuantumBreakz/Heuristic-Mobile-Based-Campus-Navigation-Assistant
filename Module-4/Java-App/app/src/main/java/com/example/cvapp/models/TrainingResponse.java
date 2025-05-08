package com.example.cvapp.models;

public class TrainingResponse {
    private String message;
    private String buildingName;

    public TrainingResponse(String message, String buildingName) {
        this.message = message;
        this.buildingName = buildingName;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public String getBuildingName() {
        return buildingName;
    }

    public void setBuildingName(String buildingName) {
        this.buildingName = buildingName;
    }
} 