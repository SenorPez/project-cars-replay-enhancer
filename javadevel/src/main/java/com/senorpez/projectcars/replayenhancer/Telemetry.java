package com.senorpez.projectcars.replayenhancer;

import com.senorpez.projectcars.replayenhancer.TelemetryDataPacket.State;

import java.io.DataInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
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

    private static void getAllRaces(PacketFactory packetFactory) {
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

        races.forEach(race1 -> {
            System.out.println("-----");
            race1.getDrivers().stream().map(Driver::getName).sorted().forEach(System.out::println);
        });
        System.out.println("-----");
    }

    public static void main(String[] args) throws IOException {
        ClassLoader classLoader = Telemetry.class.getClassLoader();
        DataInputStream telemetryData = new DataInputStream(classLoader.getResourceAsStream("race1.replayenhancer"));

        PacketFactory packetFactory = new PacketFactory(telemetryData);
        getAllRaces(packetFactory);
    }
}
