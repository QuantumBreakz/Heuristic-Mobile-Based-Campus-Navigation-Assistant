package com.example.cvapp.models;

public class VisualizationConfig {
    private int[] figureSize;
    private Integer dpi;
    private Integer markerSize;
    private Float historyLineWidth;
    private Integer updateInterval;
    private Boolean showGrid;
    private Boolean showLegend;
    private Boolean showConfidence;

    public VisualizationConfig(int[] figureSize, Integer dpi, Integer markerSize,
                             Float historyLineWidth, Integer updateInterval,
                             Boolean showGrid, Boolean showLegend, Boolean showConfidence) {
        this.figureSize = figureSize;
        this.dpi = dpi;
        this.markerSize = markerSize;
        this.historyLineWidth = historyLineWidth;
        this.updateInterval = updateInterval;
        this.showGrid = showGrid;
        this.showLegend = showLegend;
        this.showConfidence = showConfidence;
    }

    public int[] getFigureSize() {
        return figureSize;
    }

    public void setFigureSize(int[] figureSize) {
        this.figureSize = figureSize;
    }

    public Integer getDpi() {
        return dpi;
    }

    public void setDpi(Integer dpi) {
        this.dpi = dpi;
    }

    public Integer getMarkerSize() {
        return markerSize;
    }

    public void setMarkerSize(Integer markerSize) {
        this.markerSize = markerSize;
    }

    public Float getHistoryLineWidth() {
        return historyLineWidth;
    }

    public void setHistoryLineWidth(Float historyLineWidth) {
        this.historyLineWidth = historyLineWidth;
    }

    public Integer getUpdateInterval() {
        return updateInterval;
    }

    public void setUpdateInterval(Integer updateInterval) {
        this.updateInterval = updateInterval;
    }

    public Boolean getShowGrid() {
        return showGrid;
    }

    public void setShowGrid(Boolean showGrid) {
        this.showGrid = showGrid;
    }

    public Boolean getShowLegend() {
        return showLegend;
    }

    public void setShowLegend(Boolean showLegend) {
        this.showLegend = showLegend;
    }

    public Boolean getShowConfidence() {
        return showConfidence;
    }

    public void setShowConfidence(Boolean showConfidence) {
        this.showConfidence = showConfidence;
    }
} 