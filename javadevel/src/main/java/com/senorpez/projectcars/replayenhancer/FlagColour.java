package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum FlagColour {
    FLAG_COLOUR_NONE(0),
    FLAG_COLOUR_GREEN(1),
    FLAG_COLOUR_BLUE(2),
    FLAG_COLOUR_WHITE(3),
    FLAG_COLOUR_YELLOW(4),
    FLAG_COLOUR_DOUBLE_YELLOW(5),
    FLAG_COLOUR_BLACK(6),
    FLAG_COLOUR_CHEQUERED(7),
    FLAG_COLOUR_MAX(8);

    private final Byte stateValue;

    FlagColour(int stateValue) {
        this.stateValue = (byte) stateValue;
    }

    private static final Map<Byte, FlagColour> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(FlagColour.class)
                .stream()
                .collect(Collectors.toMap(flagColour -> flagColour.stateValue, flagColour -> flagColour)));
    }

    static FlagColour valueOf(int stateValue) {
        return lookup.get((byte) stateValue);
    }
}
