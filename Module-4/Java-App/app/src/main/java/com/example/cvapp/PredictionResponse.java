package com.example.cvapp;

public class PredictionResponse {
    private String predicted_class;
    private double confidence;
    private String status;

    public String getPredicted_class() {
        return predicted_class;
    }

    public double getConfidence() {
        return confidence;
    }

    public String getStatus() {
        return status;
    }

    public void setPredicted_class(String predicted_class) {
        this.predicted_class = predicted_class;
    }

    public void setConfidence(double confidence) {
        this.confidence = confidence;
    }

    public void setStatus(String status) {
        this.status = status;
    }
}
