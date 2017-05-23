package com.senorpez.projectcars.replayenhancer;

import java.io.*;
import java.lang.reflect.InvocationTargetException;
import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum PacketType {
    TELEMETRY(1367, TelemetryDataPacket.class),
    PARTICIPANT(1347, ParticipantPacket.class),
    ADDITIONAL_PARTICIPANT(1028, AdditionalParticipantPacket.class);

    private final Short packetLength;
    private final Class<? extends Packet> clazz;

    PacketType(int packetLength, Class<? extends Packet> clazz) {
        this.packetLength = (short) packetLength;
        this.clazz = clazz;
    }

    private static final Map<Short, PacketType> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(PacketType.class)
                .stream()
                .collect(Collectors.toMap(packetType -> packetType.packetLength, packetType -> packetType)));
    }

    static PacketType valueOf(Short packetLength) {
        return lookup.get(packetLength);
    }

    static PacketType valueOf(Integer packetTypeNumeric) {
        return PacketType.values()[packetTypeNumeric];
    }

    Packet getPacket(DataInputStream telemetryData) {
        try {
            if (telemetryData.available() > 0) {
                return clazz.getDeclaredConstructor(DataInputStream.class).newInstance(telemetryData);
            }
        } catch (IOException | NoSuchMethodException | InvocationTargetException | IllegalAccessException | InstantiationException e) {
            e.printStackTrace();
        }
        return null;
    }

    static Packet getPacket(ObjectInputStream telemetryData) {
        try {
            if (telemetryData.available() > 0) {
                return (Packet) telemetryData.readObject();
            }
        } catch (IOException | ClassNotFoundException e) {
            e.printStackTrace();
        }
        return null;
    }

    public Short getPacketLength() {
        return packetLength;
    }
}