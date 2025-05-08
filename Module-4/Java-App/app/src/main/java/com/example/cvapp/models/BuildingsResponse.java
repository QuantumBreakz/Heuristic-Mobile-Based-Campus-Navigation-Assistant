package com.example.cvapp.models;

import java.util.Map;

public class BuildingsResponse {
    private Map<String, Building> buildings;

    public BuildingsResponse(Map<String, Building> buildings) {
        this.buildings = buildings;
    }

    public Map<String, Building> getBuildings() {
        return buildings;
    }

    public void setBuildings(Map<String, Building> buildings) {
        this.buildings = buildings;
    }
} 