package com.example.cvapp.models;

public class CalibrationRequest {
    private double knownDistance;
    private String image;

    public CalibrationRequest(double knownDistance, String image) {
        this.knownDistance = knownDistance;
        this.image = image;
    }

    public double getKnownDistance() {
        return knownDistance;
    }

    public void setKnownDistance(double knownDistance) {
        this.knownDistance = knownDistance;
    }

    public String getImage() {
        return image;
    }

    public void setImage(String image) {
        this.image = image;
    }
} 