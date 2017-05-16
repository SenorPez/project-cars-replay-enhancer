package com.senorpez.projectcars.replayenhancer;

import java.nio.ByteBuffer;
import java.util.List;
import java.util.stream.IntStream;

class AdditionalParticipantPacket extends Packet {
    private final static Short packetType = 2;

    private final Short offset;
    private final List<String> names;

    AdditionalParticipantPacket(ByteBuffer data) throws InvalidPacketException {
        super(data);
        if (!isCorrectPacketType(packetType)) {
            throw new InvalidPacketException();
        }

        this.offset = ReadUnsignedByte(data);
        this.names = IntStream.range(0, 16).mapToObj(value -> ReadString(data)).collect(ImmutableListCollector.toImmutableList());
    }

    @Override
    Short getPacketType() {
        return packetType;
    }

    Short getOffset() {
        return offset;
    }

    List<String> getNames() {
        return names;
    }
}
