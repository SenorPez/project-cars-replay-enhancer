package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum CurrentSector {
    SECTOR_INVALID(0),
    SECTOR_START(1),
    SECTOR_SECTOR1(2),
    SECTOR_SECTOR2(3),
    SECTOR_FINISH(4),
    SECTOR_STOP(5),
    SECTOR_MAX(6);

    private final Byte stateValue;

    CurrentSector(int stateValue) {
        this.stateValue = (byte) stateValue;
    }

    private static final Map<Byte, CurrentSector> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(CurrentSector.class)
                .stream()
                .collect(Collectors.toMap(currentSector -> currentSector.stateValue, currentSector -> currentSector)));
    }

    static CurrentSector valueOf(int stateValue) {
        return lookup.get((byte) stateValue);
    }
}
