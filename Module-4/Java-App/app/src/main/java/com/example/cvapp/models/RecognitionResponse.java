package com.example.cvapp.models;

public class RecognitionResponse {
    private String buildingName;
    private String buildingType;
    private double confidence;

    public RecognitionResponse() {
    }

    public RecognitionResponse(String buildingName, String buildingType, double confidence) {
        this.buildingName = buildingName;
        this.buildingType = buildingType;
        this.confidence = confidence;
    }

    public String getBuildingName() {
        return buildingName;
    }

    public void setBuildingName(String buildingName) {
        this.buildingName = buildingName;
    }

    public String getBuildingType() {
        return buildingType;
    }

    public void setBuildingType(String buildingType) {
        this.buildingType = buildingType;
    }

    public double getConfidence() {
        return confidence;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }
} 