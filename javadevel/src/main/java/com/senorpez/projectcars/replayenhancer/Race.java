package com.senorpez.projectcars.replayenhancer;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.annotation.JsonTypeName;
import com.senorpez.projectcars.replayenhancer.TelemetryDataPacket.State;
import org.springframework.hateoas.ResourceSupport;

import java.io.*;
import java.util.*;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;
import java.util.stream.IntStream;

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include = JsonTypeInfo.As.WRAPPER_OBJECT)
@JsonTypeName("race")
class Race extends ResourceSupport {
    @JsonProperty("drivers")
    private final Set<Driver> drivers = new TreeSet<>(Comparator.comparing(Driver::getName));

    private final ByteArrayOutputStream byteStream = new ByteArrayOutputStream();

    @JsonProperty("packetCount")
    private Integer packetCount = 0;

    @JsonProperty("completeRace")
    private final Boolean completeRace;

    @JsonProperty("laps")
    private Short laps = 0;

    @JsonProperty("time")
    private Float time = 0f;

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

        completeRace = (previousState == State.RACING && currentState == State.FINISHED)
                || (previousState == State.FINISHED && currentState == State.FINISHED);

        ObjectInputStream inputStream = new ObjectInputStream(new ByteArrayInputStream(byteStream.toByteArray()));
        PacketFactory newPacketFactory = new PacketFactory(inputStream);

        drivers.addAll(Collections.unmodifiableSet(addDrivers(newPacketFactory)));

        inputStream = new ObjectInputStream(new ByteArrayInputStream(byteStream.toByteArray()));
        packetFactory = new PacketFactory(inputStream);
        while (packetFactory.hasNext()) {
            Packet packet = packetFactory.next();
            if (packet instanceof TelemetryDataPacket) {
                getDrivers().forEach(driver -> driver.addSectorTime((TelemetryDataPacket) packet));
                laps = ((TelemetryDataPacket) packet).getLapsInEvent();
                time = Math.max(time, ((TelemetryDataPacket) packet).getEventTimeRemaining());
            }
        }
    }

    byte[] getByteData() {
        return byteStream.toByteArray();
    }

    Set<Driver> getDrivers() {
        return drivers;
    }

    Integer getPacketCount() {
        return packetCount;
    }

    Boolean isCompleteRace() {
        return completeRace;
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
