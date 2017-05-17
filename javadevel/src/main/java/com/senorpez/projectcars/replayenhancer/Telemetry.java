package com.senorpez.projectcars.replayenhancer;

import java.io.DataInputStream;
import java.io.IOException;
import java.nio.ByteBuffer;
import java.util.ArrayList;
import java.util.List;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.Stream;

class Telemetry {
    private final DataInputStream telemetryData;

    private Telemetry(DataInputStream telemetryData) {
        this.telemetryData = telemetryData;
    }

    private Packet getPacket() {
        try {
            if (telemetryData.available() > 0) {
                byte[] packet = new byte[telemetryData.readShort()];
                telemetryData.read(packet);
                return PacketFactory.createPacket(ByteBuffer.wrap(packet));
            }
        } catch (IOException e) {

        }
        return null;
    }

    private void showCarThings() {
        Packet packet;
        do {
            packet = getPacket();
            if (packet instanceof TelemetryDataPacket) {
                Stream.of(
                        ((TelemetryDataPacket) packet).isHeadlight(),
                        ((TelemetryDataPacket) packet).isEngineActive(),
                        ((TelemetryDataPacket) packet).isEngineWarning(),
                        ((TelemetryDataPacket) packet).isSpeedLimiter(),
                        ((TelemetryDataPacket) packet).isAbs(),
                        ((TelemetryDataPacket) packet).isHandbrake(),
                        ((TelemetryDataPacket) packet).isStability(),
                        ((TelemetryDataPacket) packet).isTractionControl())
                        .map(value -> value ? 1 : 0)
                        .forEach(value -> System.out.printf("%d", value));
                System.out.printf("\n");
            }
        } while (packet != null);
    }

    private void showStateTransitions() {
        List<String> states = new ArrayList<>();

        Packet packet;
        TelemetryDataPacket.State state = TelemetryDataPacket.State.UNDEFINED;
        do {

            packet = getPacket();
            if (packet instanceof TelemetryDataPacket) {
                TelemetryDataPacket.State previousState = state;
                state = ((TelemetryDataPacket) packet).getState();

                if (state != previousState) System.out.println(state.toString());
                if (state == TelemetryDataPacket.State.UNDEFINED) System.out.printf("%s %s %s\n",
                        ((TelemetryDataPacket) packet).getGameState(),
                        ((TelemetryDataPacket) packet).getSessionState(),
                        ((TelemetryDataPacket) packet).getRaceState());
                states.add(state.toString());
            }
        } while (packet != null);

        states.stream()
                .collect(Collectors.groupingBy(Function.identity(), Collectors.counting()))
                .forEach((statename, count) -> System.out.printf("%s: %d\n", statename, count));

    }

    public static void main(String[] args) {
        ClassLoader classLoader = Telemetry.class.getClassLoader();
        Telemetry telemetry = new Telemetry(new DataInputStream(classLoader.getResourceAsStream("race1.replayenhancer")));
        telemetry.showCarThings();
    }
}
