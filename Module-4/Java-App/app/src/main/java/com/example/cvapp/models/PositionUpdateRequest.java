package com.example.cvapp.models;

import java.util.Map;

public class PositionUpdateRequest {
    private Map<String, Double> distances;
    private Map<String, Double> confidences;

    public PositionUpdateRequest(Map<String, Double> distances, Map<String, Double> confidences) {
        this.distances = distances;
        this.confidences = confidences;
    }

    public Map<String, Double> getDistances() {
        return distances;
    }

    public void setDistances(Map<String, Double> distances) {
        this.distances = distances;
    }

    public Map<String, Double> getConfidences() {
        return confidences;
    }

    public void setConfidences(Map<String, Double> confidences) {
        this.confidences = confidences;
    }
} 