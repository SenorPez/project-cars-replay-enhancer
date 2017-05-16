package com.senorpez.projectcars.replayenhancer;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;

public class PacketReader {
    public static void main(String[] args) throws IOException {
        try (DataInputStream inputStream = new DataInputStream(getResource())) {
            while (inputStream.available() > 0) {
                Short packetLength = inputStream.readShort();
                byte[] packet = new byte[packetLength];
                inputStream.read(packet);
                Packet data = PacketFactory.createPacket(ByteBuffer.wrap(packet));

                if (data instanceof TelemetryDataPacket) {
                    System.out.println(((TelemetryDataPacket) data).getRaceState().toString());
                }
            }
        }
    }

    private static InputStream getResource() throws IOException {
        ClassLoader classLoader = PacketReader.class.getClassLoader();
        return classLoader.getResourceAsStream("race1.replayenhancer");
    }
}
