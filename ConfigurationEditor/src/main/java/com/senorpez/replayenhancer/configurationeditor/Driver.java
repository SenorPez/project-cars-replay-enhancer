package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.scene.paint.Color;

public class Driver {
    private final SimpleStringProperty team;
    private final SimpleStringProperty shortName;
    private final SimpleStringProperty displayName;
    private final SimpleStringProperty name;
    private final SimpleObjectProperty<Car> car;
    private final SimpleIntegerProperty seriesPoints;

    public Driver(String name) {
        this.name = new SimpleStringProperty(name);
        this.displayName = new SimpleStringProperty(name);

        String[] nameChunks = name.split(" ");
        if (nameChunks.length == 1) {
            this.shortName = new SimpleStringProperty(name);
        } else {
            String firstName = nameChunks[0];
            String lastName = nameChunks[nameChunks.length - 1];
            this.shortName = new SimpleStringProperty(firstName.charAt(0) + ". " + lastName);
        }

        this.car = new SimpleObjectProperty<>(new Car("", new CarClass("", Color.rgb(255, 0, 0))));
        this.team = new SimpleStringProperty("");
        this.seriesPoints = new SimpleIntegerProperty(0);
    }

    public Driver(String name, String displayName, String shortName, Car car) {
        this.name = new SimpleStringProperty(name);
        this.displayName = new SimpleStringProperty(displayName);
        this.shortName = new SimpleStringProperty(shortName);
        this.car = new SimpleObjectProperty<>(car);
        this.team = new SimpleStringProperty("");
        this.seriesPoints = new SimpleIntegerProperty(0);
    }

    public Driver(String name, String displayName, String shortName, Car car, String team, Integer points) {
        this.name = new SimpleStringProperty(name);
        this.displayName = new SimpleStringProperty(displayName);
        this.shortName = new SimpleStringProperty(shortName);
        this.car = new SimpleObjectProperty<>(car);
        this.team = new SimpleStringProperty(team);
        this.seriesPoints = new SimpleIntegerProperty(points);
    }

    public String getTeam() {
        return team.get();
    }

    public void setTeam(String team) {
        this.team.set(team);
    }

    public SimpleStringProperty teamProperty() {
        return team;
    }

    public String getShortName() {
        return shortName.get();
    }

    public void setShortName(String shortName) {
        this.shortName.set(shortName);
    }

    public SimpleStringProperty shortNameProperty() {
        return shortName;
    }

    public String getDisplayName() {
        return displayName.get();
    }

    public void setDisplayName(String displayName) {
        this.displayName.set(displayName);
    }

    public SimpleStringProperty displayNameProperty() {
        return displayName;
    }

    public String getName() {
        return name.get();
    }

    public void setName(String name) {
        this.name.set(name);
    }

    public SimpleStringProperty nameProperty() {
        return name;
    }

    public Car getCar() {
        return car.get();
    }

    public void setCar(Car car) {
        this.car.set(car);
    }

    public SimpleObjectProperty<Car> carProperty() {
        return car;
    }

    public int getSeriesPoints() {
        return seriesPoints.get();
    }

    public void setSeriesPoints(int seriesPoints) {
        this.seriesPoints.set(seriesPoints);
    }

    public SimpleIntegerProperty seriesPointsProperty() {
        return seriesPoints;
    }
}
