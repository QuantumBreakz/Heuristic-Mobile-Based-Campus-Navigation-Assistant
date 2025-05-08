package com.example.cvapp.models;

import java.util.List;

public class PositionResponse {
    private Coordinates currentPosition;
    private List<Coordinates> history;

    public PositionResponse(Coordinates currentPosition, List<Coordinates> history) {
        this.currentPosition = currentPosition;
        this.history = history;
    }

    public Coordinates getCurrentPosition() {
        return currentPosition;
    }

    public void setCurrentPosition(Coordinates currentPosition) {
        this.currentPosition = currentPosition;
    }

    public List<Coordinates> getHistory() {
        return history;
    }

    public void setHistory(List<Coordinates> history) {
        this.history = history;
    }
} 