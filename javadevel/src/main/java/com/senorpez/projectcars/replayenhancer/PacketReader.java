package com.senorpez.projectcars.replayenhancer;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;

public class PacketReader {
    public static void main(String[] args) throws IOException {
        List<String> sectors = new ArrayList<>();
        List<String> combined_state = new ArrayList<>();
        try (DataInputStream inputStream = new DataInputStream(getResource())) {
            while (inputStream.available() > 0) {
                Short packetLength = inputStream.readShort();
                byte[] packet = new byte[packetLength];
                inputStream.read(packet);
                Packet data = PacketFactory.createPacket(ByteBuffer.wrap(packet));

                if (data instanceof TelemetryDataPacket) {
                    TelemetryDataPacket teleData = (TelemetryDataPacket) data;
                    sectors.add(teleData.getParticipantInfo().get(0).getCurrentSector().toString());
                    combined_state.add(
                            teleData.getGameState().toString() + " "
                                    + teleData.getSessionState().toString() + " "
                                    + teleData.getRaceState().toString());
                }
            }
        }

        System.out.println(sectors.stream().collect(Collectors.groupingBy(Function.identity(), Collectors.counting())));
        combined_state.stream()
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()))
                .forEach((state, count) -> System.out.printf("%s: %d\n", state, count));
    }

    private static InputStream getResource() throws IOException {
        ClassLoader classLoader = PacketReader.class.getClassLoader();
        return classLoader.getResourceAsStream("race1.replayenhancer");
    }
}
