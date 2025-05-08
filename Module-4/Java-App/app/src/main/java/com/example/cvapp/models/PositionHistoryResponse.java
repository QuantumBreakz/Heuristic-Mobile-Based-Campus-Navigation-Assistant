package com.example.cvapp.models;

import java.util.List;

public class PositionHistoryResponse {
    private List<Coordinates> history;

    public PositionHistoryResponse(List<Coordinates> history) {
        this.history = history;
    }

    public List<Coordinates> getHistory() {
        return history;
    }

    public void setHistory(List<Coordinates> history) {
        this.history = history;
    }
} 