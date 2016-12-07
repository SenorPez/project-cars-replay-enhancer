package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleObjectProperty;
import javafx.beans.property.SimpleStringProperty;

public class Car {
    private final SimpleStringProperty carName;
    private final SimpleObjectProperty<CarClass> carClass;

    public Car(String name, CarClass carClass) {
        this.carName = new SimpleStringProperty(name);
        this.carClass = new SimpleObjectProperty<>(carClass);
    }

    public String getCarName() {
        return carName.get();
    }

    public void setCarName(String carName) {
        this.carName.set(carName);
    }

    public SimpleStringProperty carNameProperty() {
        return carName;
    }

    public CarClass getCarClass() {
        return carClass.get();
    }

    public void setCarClass(CarClass carClass) {
        this.carClass.set(carClass);
    }

    public SimpleObjectProperty<CarClass> carClassProperty() {
        return carClass;
    }
}
