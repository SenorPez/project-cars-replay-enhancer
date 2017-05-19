package com.senorpez.projectcars.replayenhancer;

import com.senorpez.projectcars.replayenhancer.TelemetryDataPacket.State;

import java.io.DataInputStream;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;

class Telemetry {
    private final DataInputStream telemetryData;

    private Telemetry(DataInputStream telemetryData) {
        this.telemetryData = telemetryData;
    }

    private void showStateTransitions(PacketFactory packetFactory) {
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

    public static void main(String[] args) {
        ClassLoader classLoader = Telemetry.class.getClassLoader();
        Telemetry telemetry = new Telemetry(new DataInputStream(classLoader.getResourceAsStream("race1.replayenhancer")));
        PacketFactory packetFactory = new PacketFactory(telemetry.telemetryData);
//        telemetry.showStateTransitions(new PacketFactory(telemetry.telemetryData));
        System.out.println("-----");
        Race race = new Race(packetFactory);
        race.getDrivers().stream().map(Driver::getName).sorted().forEach(System.out::println);
        System.out.println("-----");
        race = new Race(packetFactory);
        race.getDrivers().stream().map(Driver::getName).sorted().forEach(System.out::println);
        System.out.println("-----");
        race = new Race(packetFactory);
        race.getDrivers().stream().map(Driver::getName).sorted().forEach(System.out::println);
        System.out.println("-----");
        race = new Race(packetFactory);
        race.getDrivers().stream().map(Driver::getName).sorted().forEach(System.out::println);
        System.out.println("-----");
        race = new Race(packetFactory);
        race.getDrivers().stream().map(Driver::getName).sorted().forEach(System.out::println);
        System.out.println("-----");
        race = new Race(packetFactory);
        race.getDrivers().stream().map(Driver::getName).sorted().forEach(System.out::println);
        System.out.println("-----");
    }
}
