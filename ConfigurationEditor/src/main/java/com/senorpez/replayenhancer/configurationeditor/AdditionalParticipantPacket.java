package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleListProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;

import java.nio.ByteBuffer;

public class AdditionalParticipantPacket extends Packet {
    private final SimpleIntegerProperty offset;
    private final SimpleListProperty<SimpleStringProperty> names;

    public AdditionalParticipantPacket(ByteBuffer data) {
        super(data);          
        
        this.offset = new SimpleIntegerProperty(ReadChar(data));

        this.names = new SimpleListProperty<>(FXCollections.observableArrayList());
        for (int i = 0; i < 16 ; i++) {
            this.names.add(new SimpleStringProperty(ReadString(data, 64).split("\u0000", 2)[0]));
        }
    }
    
    public Integer getOffset() {
        return offset.get();
    }

    public ObservableList<SimpleStringProperty> getNames() {
        return names.get();
    }
}