package com.senorpez.projectcars.replayenhancer;

import java.io.DataInputStream;
import java.io.FileInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;

public class PacketReader {
    public static void main(String[] args) throws IOException {
        try (DataInputStream inputStream = new DataInputStream(new FileInputStream("race1.replayenhancer"))) {
            while (true) {
                Short packetLength = inputStream.readShort();
                byte[] packet = new byte[packetLength];
                inputStream.read(packet);
                PacketFactory.createPacket(ByteBuffer.wrap(packet));
            }
        }
    }
}
