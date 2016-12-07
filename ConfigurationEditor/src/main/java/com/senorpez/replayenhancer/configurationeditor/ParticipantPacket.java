package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleFloatProperty;
import javafx.beans.property.SimpleListProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;

import java.nio.ByteBuffer;
import java.util.ArrayList;

public class ParticipantPacket extends Packet {
    private final SimpleStringProperty carName;
    private final SimpleStringProperty carClass;
    private final SimpleStringProperty trackLocation;
    private final SimpleStringProperty trackVariation;
        
    private final SimpleListProperty<SimpleStringProperty> names;
    private final SimpleListProperty<SimpleFloatProperty> fastestLapTimes;

    public ParticipantPacket(ByteBuffer data) {
        super(data);
      
        this.carName = new SimpleStringProperty(ReadString(data, 64).trim());
        this.carClass = new SimpleStringProperty(ReadString(data, 64).trim());
        this.trackLocation = new SimpleStringProperty(ReadString(data, 64).trim());
        this.trackVariation = new SimpleStringProperty(ReadString(data, 64).trim());
        

        this.names = new SimpleListProperty<>(FXCollections.observableArrayList());
        for (int i = 0; i < 16 ; i++) {
            this.names.add(new SimpleStringProperty(ReadString(data, 64).split("\u0000", 2)[0]));
        }

        this.fastestLapTimes = new SimpleListProperty<>(FXCollections.observableList(new ArrayList<>()));
        for (int i = 0; i < 16; i++) {
            this.fastestLapTimes.add(new SimpleFloatProperty(ReadFloat(data)));
        }
    }
    
    public String getCarName() {
        return carName.get();
    }
    
    public String getCarClass() {
        return carClass.get();
    }
    
    public String getTrackLocation() {
        return trackLocation.get();
    }
    
    public String getTrackVariation() {
        return trackVariation.get();
    }

    public ObservableList<SimpleStringProperty> getNames() {
        return names.get();
    }

    public ObservableList<SimpleFloatProperty> getFastestLapTimes() {
        return fastestLapTimes.get();
    }
}
