package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleIntegerProperty;

public class PointStructureItem {
    private final SimpleIntegerProperty points;
    private final SimpleIntegerProperty finishPosition;

    public PointStructureItem(int finishPosition, Integer points) {
        this.finishPosition = new SimpleIntegerProperty(finishPosition);
        this.points = new SimpleIntegerProperty(points);
    }

    public int getPoints() {
        return points.get();
    }

    public void setPoints(int points) {
        this.points.set(points);
    }

    public SimpleIntegerProperty pointsProperty() {
        return points;
    }

    public int getFinishPosition() {
        return finishPosition.get();
    }

    public void setFinishPosition(int finishPosition) {
        this.finishPosition.set(finishPosition);
    }

    public SimpleIntegerProperty finishPositionProperty() {
        return finishPosition;
    }
}
