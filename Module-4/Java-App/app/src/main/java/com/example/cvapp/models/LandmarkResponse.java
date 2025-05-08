package com.example.cvapp.models;

public class LandmarkResponse {
    private String message;
    private String buildingName;
    private Coordinates position;

    public LandmarkResponse(String message, String buildingName, Coordinates position) {
        this.message = message;
        this.buildingName = buildingName;
        this.position = position;
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

    public Coordinates getPosition() {
        return position;
    }

    public void setPosition(Coordinates position) {
        this.position = position;
    }
} 