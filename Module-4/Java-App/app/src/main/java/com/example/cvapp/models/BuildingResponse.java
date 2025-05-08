package com.example.cvapp.models;

public class BuildingResponse {
    private String buildingName;
    private String buildingType;
    private Coordinates coordinates;

    public BuildingResponse(String buildingName, String buildingType, Coordinates coordinates) {
        this.buildingName = buildingName;
        this.buildingType = buildingType;
        this.coordinates = coordinates;
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

    public Coordinates getCoordinates() {
        return coordinates;
    }

    public void setCoordinates(Coordinates coordinates) {
        this.coordinates = coordinates;
    }
} 