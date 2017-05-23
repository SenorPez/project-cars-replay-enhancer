package com.senorpez.projectcars.replayenhancer;

import java.io.DataInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.stream.IntStream;

class ParticipantPacket extends Packet {
    private final static PacketType packetType = PacketType.PARTICIPANT;

    private final String carName;
    private final String carClass;
    private final String trackLocation;
    private final String trackVariation;
    private final List<String> names;
    private final List<Float> fastestLapTimes;

    ParticipantPacket(DataInputStream data) throws InvalidPacketException, IOException {
        super(data);
        if (!isCorrectPacketType(packetType)) {
            throw new InvalidPacketException();
        }

        byte[] nameBuffer = new byte[64];

        data.read(nameBuffer);
        this.carName = new String(nameBuffer, StandardCharsets.UTF_8).split("\u0000", 2)[0];
        data.read(nameBuffer);
        this.carClass = new String(nameBuffer, StandardCharsets.UTF_8).split("\u0000", 2)[0];
        data.read(nameBuffer);
        this.trackLocation = new String(nameBuffer, StandardCharsets.UTF_8).split("\u0000", 2)[0];
        data.read(nameBuffer);
        this.trackVariation = new String(nameBuffer, StandardCharsets.UTF_8).split("\u0000", 2)[0];

        this.names = IntStream.range(0, 16).mapToObj(value -> {
            try {
                data.read(nameBuffer);
            } catch (IOException e) {
                e.printStackTrace();
            }
            return new String(nameBuffer, StandardCharsets.UTF_8).split("\u0000", 2)[0];
        }).collect(ImmutableListCollector.toImmutableList());
        this.fastestLapTimes = IntStream.range(0, 16).mapToObj((IntFunctionThrows<Float>) value -> data.readFloat()).collect(ImmutableListCollector.toImmutableList());
    }

    @Override
    PacketType getPacketType() {
        return packetType;
    }

    String getCarName() {
        return carName;
    }

    String getCarClass() {
        return carClass;
    }

    String getTrackLocation() {
        return trackLocation;
    }

    String getTrackVariation() {
        return trackVariation;
    }

    List<String> getNames() {
        return names;
    }

    List<Float> getFastestLapTimes() {
        return fastestLapTimes;
    }
}
