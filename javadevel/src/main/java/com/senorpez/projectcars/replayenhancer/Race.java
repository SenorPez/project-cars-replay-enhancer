package com.senorpez.projectcars.replayenhancer;

import com.senorpez.projectcars.replayenhancer.TelemetryDataPacket.State;

import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

class Race {
    private final List<Packet> racePackets;
    private Byte numParticipants;

    Race(PacketFactory packetFactory) {
        Boolean raceStarted = false;
        Boolean raceFinished = false;
        State currentState = State.UNDEFINED;
        State previousState = State.UNDEFINED;
        racePackets = new ArrayList<>();
        numParticipants = null;

        while (packetFactory.hasNext() && !raceFinished) {
            Packet packet = packetFactory.next();
            if (packet instanceof TelemetryDataPacket) {
                numParticipants = ((TelemetryDataPacket) packet).getNumParticipants();

                previousState = currentState;
                currentState = ((TelemetryDataPacket) packet).getState();

                raceStarted = raceStarted || currentState.raceStarted();
                raceFinished = currentState.raceFinished(previousState);
            } else if (packet == null) {
                raceFinished = previousState.raceFinishedTelemetryExhausted();
            }

            if (raceStarted && !raceFinished) {
                racePackets.add(packet);
            }
        }
    }

    Set<Driver> getDrivers() {
        Iterator<Packet> packetIterator = racePackets.iterator();
        Set<Driver> drivers = new HashSet<>();
        Byte packetParticipants;

        if (numParticipants == null) {
            while (numParticipants == null && packetIterator.hasNext()) {
                Packet packet = packetIterator.next();
                if (packet instanceof TelemetryDataPacket) {
                    numParticipants = ((TelemetryDataPacket) packet).getNumParticipants();
                }
            }
        }
        packetParticipants = numParticipants;

        while (packetIterator.hasNext()
                && packetParticipants.equals(numParticipants)
                && drivers.size() < numParticipants) {
            Packet packet = packetIterator.next();
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
