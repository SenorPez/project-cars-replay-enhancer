package com.senorpez.projectcars.replayenhancer;

import java.nio.ByteBuffer;

class PacketFactory {
    static Packet createPacket(ByteBuffer data) {
        switch(data.remaining()) {
            case 1367:
                try {
                    return new TelemetryDataPacket(data);
                } catch (InvalidPacketException e) {
                    e.printStackTrace();
                }

            case 1347:
                try {
                    return new ParticipantPacket(data);
                } catch (InvalidPacketException e) {
                    e.printStackTrace();
                }

            case 1028:
                try {
                    return new AdditionalParticipantPacket(data);
                } catch (InvalidPacketException e) {
                    e.printStackTrace();
                }

            default:
                System.out.printf("Error: %d\n", data.remaining());
                return null;
        }
    }
}
