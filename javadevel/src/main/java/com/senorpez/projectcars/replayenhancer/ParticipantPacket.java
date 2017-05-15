package com.senorpez.projectcars.replayenhancer;

import java.nio.ByteBuffer;
import java.util.List;
import java.util.stream.IntStream;

class ParticipantPacket extends Packet {
    private final static Short packetType = 1;

    private final String carName;
    private final String carClass;
    private final String trackLocation;
    private final String trackVariation;
    private final List<String> names;
    private final List<Float> fastestLapTimes;

    ParticipantPacket(ByteBuffer data) {
        super(data);

        this.carName = ReadString(data);
        this.carClass = ReadString(data);
        this.trackLocation = ReadString(data);
        this.trackVariation = ReadString(data);

        this.names = IntStream.range(0, 16).mapToObj(value -> ReadString(data)).collect(ImmutableListCollector.toImmutableList());
        this.fastestLapTimes = IntStream.range(0, 16).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
    }

    @Override
    Short getPacketType() {
        return getPacketType(packetType);
    }

    @Override
    Short getCount() {
        return getCount(packetType);
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
