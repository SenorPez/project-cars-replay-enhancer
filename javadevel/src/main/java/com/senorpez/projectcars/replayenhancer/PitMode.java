package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum PitMode {
    PIT_MODE_NONE(0),
    PIT_MODE_DRIVING_INTO_PITS(1),
    PIT_MODE_IN_PIT(2),
    PIT_MODE_DRIVING_OUT_OF_PITS(3),
    PIT_MODE_IN_GARAGE(4),
    PIT_MODE_MAX(5);

    private final Byte stateValue;

    PitMode(int stateValue) {
        this.stateValue = (byte) stateValue;
    }

    private static final Map<Byte, PitMode> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(PitMode.class)
                .stream()
                .collect(Collectors.toMap(pitMode -> pitMode.stateValue, pitMode -> pitMode)));
    }

    static PitMode valueOf(int stateValue) {
        return lookup.get((byte) stateValue);
    }
}
