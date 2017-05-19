package com.senorpez.projectcars.replayenhancer;

import java.io.DataInputStream;
import java.io.IOException;
import java.util.Iterator;

class PacketFactory implements Iterator<Packet> {
    private final DataInputStream telemetryData;

    public PacketFactory(DataInputStream telemetryData) {
        this.telemetryData = telemetryData;
    }

    @Override
    public boolean hasNext() {
        try {
            return telemetryData.available() > 0;
        } catch (IOException e) {
            return false;
        }
    }

    @Override
    public Packet next() {
        PacketType packetType;
        try {
            packetType = PacketType.valueOf(telemetryData.readShort());
            return packetType.getPacket(telemetryData);
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    static Packet getPacket(DataInputStream telemetryData) {
        try {
            if (telemetryData.available() > 0) {
                PacketType packetType = PacketType.valueOf(telemetryData.readShort());
                return packetType.getPacket(telemetryData);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }
}
