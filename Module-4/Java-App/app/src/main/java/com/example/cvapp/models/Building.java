package com.example.cvapp.models;

public class Building {
    private String name;
    private Coordinates coordinates;
    private String type;

    public Building(String name, Coordinates coordinates, String type) {
        this.name = name;
        this.coordinates = coordinates;
        this.type = type;
    }

    public String getName() {
        return name;
    }

    public void setName(String name) {
        this.name = name;
    }

    public Coordinates getCoordinates() {
        return coordinates;
    }

    public void setCoordinates(Coordinates coordinates) {
        this.coordinates = coordinates;
    }

    public String getType() {
        return type;
    }

    public void setType(String type) {
        this.type = type;
    }
} 