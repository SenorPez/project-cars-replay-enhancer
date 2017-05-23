package com.senorpez.projectcars.replayenhancer;

import java.io.*;
import java.util.Iterator;

class PacketFactory implements Iterator<Packet> {
    private final InputStream telemetryData;

    PacketFactory(DataInputStream telemetryData) {
        this.telemetryData = telemetryData;
    }

    PacketFactory(ObjectInputStream telemetryData) {
        this.telemetryData = telemetryData;
    }

    PacketFactory(Race race) throws IOException {
        this.telemetryData = new ObjectInputStream(new ByteArrayInputStream(race.getByteData()));
    }

    private Packet nextPacket = null;

    @Override
    public boolean hasNext() {
        if (telemetryData instanceof DataInputStream) {
            try {
                return telemetryData.available() > 0;
            } catch (IOException e) {
                return false;
            }
        } else if (telemetryData instanceof ObjectInputStream) {
            try {
                nextPacket = (Packet) ((ObjectInputStream) telemetryData).readObject();
                return true;
            } catch (IOException | ClassNotFoundException e) {
                nextPacket = null;
                return false;
            }
        }
        return false;
    }

    @Override
    public Packet next() {
        PacketType packetType;

        if (telemetryData instanceof DataInputStream) {
            try {
                packetType = PacketType.valueOf(((DataInputStream) telemetryData).readShort());
                return packetType.getPacket(((DataInputStream) telemetryData));
            } catch (IOException e) {
                e.printStackTrace();
            }
        } else if (telemetryData instanceof ObjectInputStream) {
            return nextPacket;
        }
        return null;
    }
}
