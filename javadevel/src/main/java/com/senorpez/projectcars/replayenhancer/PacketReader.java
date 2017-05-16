package com.senorpez.projectcars.replayenhancer;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.nio.ByteBuffer;
import java.util.Comparator;
import java.util.List;
import java.util.Set;
import java.util.TreeSet;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

public class PacketReader {
    public static void main(String[] args) throws IOException {
        Set<Driver> drivers = new TreeSet<>(Comparator.comparing(Driver::getName));
        Byte numParticipants = null;
        try (DataInputStream inputStream = new DataInputStream(getResource())) {
            while (inputStream.available() > 0) {
                Short packetLength = inputStream.readShort();
                byte[] packet = new byte[packetLength];
                inputStream.read(packet);
                Packet data = PacketFactory.createPacket(ByteBuffer.wrap(packet));

                if (data instanceof TelemetryDataPacket) {
                    TelemetryDataPacket telemetryDataPacket = (TelemetryDataPacket) data;

                    if (telemetryDataPacket.getRaceState() == RaceState.RACESTATE_RACING) {
                        numParticipants = telemetryDataPacket.getNumParticipants() > 0 ? telemetryDataPacket.getNumParticipants() : null;
                    } else if (telemetryDataPacket.getRaceState() == RaceState.RACESTATE_NOT_STARTED) {
                        numParticipants = null;
                        drivers.clear();
                    }
                } else if (data instanceof ParticipantPacket && numParticipants != null) {
                    drivers.addAll(readNames(((ParticipantPacket) data).getNames()));
                } else if (data instanceof AdditionalParticipantPacket && numParticipants != null) {
                    drivers.addAll(readNames(((AdditionalParticipantPacket) data).getNames(), ((AdditionalParticipantPacket) data).getOffset()));
                }
            }
        }
        drivers.forEach(driver -> System.out.printf("%d: %s\n", driver.getIndex(), driver.getName()));
    }

    private static InputStream getResource() throws IOException {
        ClassLoader classLoader = PacketReader.class.getClassLoader();
        return classLoader.getResourceAsStream("race1.replayenhancer");
    }

    private static List<Driver> readNames(List<String> names) {
        return readNames(names, (short) 0);
    }

    private static List<Driver> readNames(List<String> names, Short offset) {
        AtomicInteger index = new AtomicInteger(offset);
        return names.stream()
                .filter(name -> name.length() > 0)
                .map(name -> new Driver((byte) index.getAndIncrement(), name))
                .collect(Collectors.toList());
    }
}
