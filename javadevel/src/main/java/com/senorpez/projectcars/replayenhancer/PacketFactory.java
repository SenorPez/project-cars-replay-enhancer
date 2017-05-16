package com.senorpez.projectcars.replayenhancer;

import java.nio.ByteBuffer;

class PacketFactory {
    static Packet createPacket(ByteBuffer data) {
        switch(data.remaining()) {
            case 1367:
                return new TelemetryDataPacket(data);

            case 1347:
                return new ParticipantPacket(data);

            case 1028:
                return new AdditionalParticipantPacket(data);

            default:
                System.out.printf("Error: %d\n", data.remaining());
                return null;
        }
    }
}
