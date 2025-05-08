package com.example.cvapp.models;

import java.util.List;

public class BuildingTypesResponse {
    private List<String> types;

    public BuildingTypesResponse(List<String> types) {
        this.types = types;
    }

    public List<String> getTypes() {
        return types;
    }

    public void setTypes(List<String> types) {
        this.types = types;
    }
} 