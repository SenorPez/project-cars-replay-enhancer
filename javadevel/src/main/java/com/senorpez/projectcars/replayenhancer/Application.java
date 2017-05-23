package com.senorpez.projectcars.replayenhancer;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

import java.io.DataInputStream;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

@SpringBootApplication
public class Application {
    private static final ClassLoader classLoader = Application.class.getClassLoader();
    private static final DataInputStream telemetryData = new DataInputStream(classLoader.getResourceAsStream("race1.replayenhancer"));
    static final List<Race> RACES = getAllRaces(new PacketFactory(telemetryData));

    public static void main(String[] args) {
        SpringApplication.run(Application.class, args);
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
}
