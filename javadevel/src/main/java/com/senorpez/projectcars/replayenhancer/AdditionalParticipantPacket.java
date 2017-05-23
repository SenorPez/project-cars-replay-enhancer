package com.senorpez.projectcars.replayenhancer;

import java.io.DataInputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.List;
import java.util.stream.IntStream;

class AdditionalParticipantPacket extends Packet {
    private final static PacketType packetType = PacketType.ADDITIONAL_PARTICIPANT;

    private final Short offset;
    private final List<String> names;

    AdditionalParticipantPacket(DataInputStream data) throws InvalidPacketException, IOException {
        super(data);
        if (!isCorrectPacketType(packetType)) {
            throw new InvalidPacketException();
        }

        this.offset = (short) data.readUnsignedByte();

        byte[] nameBuffer = new byte[64];
        this.names = IntStream.range(0, 16).mapToObj(value -> {
            try {
                data.read(nameBuffer);
            } catch (IOException e) {
                e.printStackTrace();
            }
            return new String(nameBuffer, StandardCharsets.UTF_8).split("\u0000", 2)[0];
        }).collect(ImmutableListCollector.toImmutableList());
    }

    @Override
    PacketType getPacketType() {
        return packetType;
    }

    Short getOffset() {
        return offset;
    }

    List<String> getNames() {
        return names;
    }
}
