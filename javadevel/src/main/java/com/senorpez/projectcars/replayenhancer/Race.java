package com.senorpez.projectcars.replayenhancer;

import com.senorpez.projectcars.replayenhancer.TelemetryDataPacket.State;

import java.io.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

class Race {
    private final Set<Driver> drivers = new TreeSet<>(Comparator.comparing(Driver::getName));

    private final ByteArrayOutputStream byteStream = new ByteArrayOutputStream();
    private Integer packetCount = 0;

    Race(PacketFactory packetFactory) throws IOException {
        Boolean raceStarted = false;
        Boolean raceFinished = false;

        State currentState = State.UNDEFINED;
        State previousState = State.UNDEFINED;

        ObjectOutputStream raceData = new ObjectOutputStream(byteStream);

        while (packetFactory.hasNext() && !raceFinished) {
            Packet packet = packetFactory.next();
            if (packet instanceof TelemetryDataPacket) {
                previousState = currentState;
                currentState = ((TelemetryDataPacket) packet).getState();

                raceStarted = raceStarted || currentState.raceStarted();
                raceFinished = currentState.raceFinished(previousState);
            } else if (packet == null) {
                raceFinished = previousState.raceFinishedTelemetryExhausted();
            }

            if (raceStarted && !raceFinished) {
                raceData.writeObject(packet);
                packetCount++;
            }
        }
        raceData.close();

        ObjectInputStream inputStream = new ObjectInputStream(new ByteArrayInputStream(byteStream.toByteArray()));
        PacketFactory newPacketFactory = new PacketFactory(inputStream);

        drivers.addAll(Collections.unmodifiableSet(addDrivers(newPacketFactory)));
    }

    Set<Driver> getDrivers() {
        return drivers;
    }

    public Integer getPacketCount() {
        return packetCount;
    }

    static private Set<Driver> addDrivers(PacketFactory packetFactory) {
        Byte numParticipants = null;
        Set<Driver> drivers = new TreeSet<>(Comparator.comparing(Driver::getName));

        while (numParticipants == null && packetFactory.hasNext()) {
            Packet packet = packetFactory.next();
            if (packet instanceof TelemetryDataPacket) {
                numParticipants = ((TelemetryDataPacket) packet).getNumParticipants();
            }
        }

        if (numParticipants == null) return drivers;
        Byte packetParticipants = numParticipants;

        while (packetParticipants.equals(numParticipants)
                && drivers.size() < numParticipants
                && packetFactory.hasNext()) {
            Packet packet = packetFactory.next();
            if (packet instanceof TelemetryDataPacket) {
                packetParticipants = ((TelemetryDataPacket) packet).getNumParticipants();
            } else if (packet instanceof ParticipantPacket) {
                AtomicInteger index = new AtomicInteger(0);
                drivers.addAll(((ParticipantPacket) packet).getNames().stream()
                        .filter(name -> !name.isEmpty())
                        .limit(numParticipants)
                        .map(name -> new Driver((byte) index.getAndIncrement(), name))
                        .collect(Collectors.toList()));
            }
        }

        if (drivers.size() < numParticipants) {
            return IntStream.range(0, numParticipants)
                    .mapToObj(index -> new Driver((byte) index, String.format("Driver %d", index)))
                    .collect(Collectors.toSet());
        } else {
            return drivers;
        }
    }
}
