package com.senorpez.projectcars.replayenhancer;

import com.senorpez.projectcars.replayenhancer.TelemetryDataPacket.State;

import java.io.DataInputStream;
import java.io.IOException;
import java.text.DecimalFormat;
import java.text.NumberFormat;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.function.Function;
import java.util.stream.Collectors;

class Telemetry {
    private static void showStateTransitions(PacketFactory packetFactory) {
        State currentState = State.UNDEFINED;
        List<String> states = new ArrayList<>();

        while (packetFactory.hasNext()) {
            Packet packet = packetFactory.next();
            if (packet instanceof TelemetryDataPacket) {
                State previousState = currentState;
                currentState = ((TelemetryDataPacket) packet).getState();

                if (previousState != currentState) System.out.println(currentState.toString());
                if (currentState == State.UNDEFINED) System.out.printf("%s %s %s\n",
                        ((TelemetryDataPacket) packet).getGameState(),
                        ((TelemetryDataPacket) packet).getSessionState(),
                        ((TelemetryDataPacket) packet).getRaceState());
                states.add(currentState.toString());
            }
        }

        states.stream()
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()))
                .forEach((statename, count) -> System.out.printf("%s: %d\n", statename, count));
    }

    private static List<Race> getAllRaces(PacketFactory packetFactory) {
        List<Race> races = new ArrayList<>();
        Race race;

        while (packetFactory.hasNext()) {
            try {
                race = new Race(packetFactory);
            } catch (IOException e) {
                race = null;
            }
            if (race != null) {
                races.add(race);
            }
        }
        return races;
    }

    public static void main(String[] args) throws IOException {
        ClassLoader classLoader = Telemetry.class.getClassLoader();
        DataInputStream telemetryData = new DataInputStream(classLoader.getResourceAsStream("race1.replayenhancer"));

        Race race = getAllRaces(new PacketFactory(telemetryData))
                .stream()
                .filter(Race::isCompleteRace)
                .findFirst()
                .orElse(null);

        PacketFactory packetFactory = new PacketFactory(race);
        while (packetFactory.hasNext()) {
            Packet packet = packetFactory.next();
            if (packet instanceof TelemetryDataPacket) {
                List<TelemetryDataPacket.ParticipantInfo> participantInfos = ((TelemetryDataPacket) packet).getParticipantInfo().stream()
                        .filter(TelemetryDataPacket.ParticipantInfo::isActive)
                        .collect(Collectors.toList());
                AtomicInteger atomicIndex = new AtomicInteger(0);
                participantInfos
                        .forEach(participantInfo -> {
                            race.getDrivers().stream()
                                    .filter(driver1 -> driver1.getIndex().equals(atomicIndex.byteValue()))
                                    .findFirst()
                                    .orElse(null)
                                    .addSectorTime(
                                            new SectorTime(
                                                    participantInfo.getLastSectorTime(),
                                                    participantInfo.getCurrentSector(),
                                                    participantInfo.isLapInvalidated())
                                    );
                            atomicIndex.getAndIncrement();
                        });
            }
        }
        race.getDrivers()
                .forEach(driver -> {
                    System.out.println(driver.getName());
                    driver.getSectorTimes()
                            .forEach(sectorTime -> System.out.println(sectorTime.getTime()));
                });
    }
}
