package com.example.cvapp.models;

public class DistanceResponse {
    private double distance;
    private String unit;

    public DistanceResponse(double distance, String unit) {
        this.distance = distance;
        this.unit = unit;
    }

    public double getDistance() {
        return distance;
    }

    public void setDistance(double distance) {
        this.distance = distance;
    }

    public String getUnit() {
        return unit;
    }

    public void setUnit(String unit) {
        this.unit = unit;
    }
} 