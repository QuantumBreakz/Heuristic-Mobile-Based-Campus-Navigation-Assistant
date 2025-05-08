package com.example.cvapp.models;

public class CalibrationResponse {
    private String message;
    private double focalLength;

    public CalibrationResponse(String message, double focalLength) {
        this.message = message;
        this.focalLength = focalLength;
    }

    public String getMessage() {
        return message;
    }

    public void setMessage(String message) {
        this.message = message;
    }

    public double getFocalLength() {
        return focalLength;
    }

    public void setFocalLength(double focalLength) {
        this.focalLength = focalLength;
    }
} 