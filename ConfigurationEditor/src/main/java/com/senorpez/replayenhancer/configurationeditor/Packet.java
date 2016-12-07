package com.senorpez.replayenhancer.configurationeditor;

import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleListProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;

import java.io.UnsupportedEncodingException;
import java.nio.ByteBuffer;
import java.nio.charset.StandardCharsets;
import java.util.logging.Level;
import java.util.logging.Logger;

public abstract class Packet {

    private final SimpleIntegerProperty buildVersionNumber;
    private final SimpleIntegerProperty packetType;    

    protected Packet(ByteBuffer data) {
        this.buildVersionNumber = new SimpleIntegerProperty(ReadShort(data));
        this.packetType = new SimpleIntegerProperty(ReadChar(data));
    }
    
    private static Integer toInt(byte[] bytes) {
        int returnValue = 0;
        for (byte chunk : bytes) {
            returnValue <<= 8;
            returnValue |= (int)chunk & 0xFF;
        }
        return returnValue;
    }
     
    protected static Short ReadShort(ByteBuffer data) {
        byte[] readBytes = new byte[2];
        data.get(readBytes);
        return toInt(readBytes).shortValue();
    }
    
    protected static Integer ReadChar(ByteBuffer data) {
        byte[] readBytes = new byte[1];
        data.get(readBytes);
        return toInt(readBytes);
    }
    
    protected static Integer ReadByte(ByteBuffer data) {
        return ReadChar(data);
    }
    
    protected static Float ReadFloat(ByteBuffer data) {
        byte[] readBytes = new byte[4];
        data.get(readBytes);
        return ByteBuffer.wrap(readBytes).getFloat();
    }
    
    protected static String ReadString(ByteBuffer data, Integer length) {
        byte[] readBytes = new byte[length];
        data.get(readBytes);
        return new String(readBytes, StandardCharsets.UTF_8);
    }
    
    public Integer getBuildVersionNumber() {
        return buildVersionNumber.get();
    }
    
    public Integer getPacketType() {
        return packetType.get();
    }
}
