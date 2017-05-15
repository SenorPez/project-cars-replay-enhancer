package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum FlagReason {
    FLAG_REASON_NONE(0),
    FLAG_REASON_SOLO_CRASH(1),
    FLAG_REASON_VEHICLE_CRASH(2),
    FLAG_REASON_VEHICLE_OBSTRUCTION(3),
    FLAG_REASON_MAX(4);

    private final Byte stateValue;

    FlagReason(int stateValue) {
        this.stateValue = (byte) stateValue;
    }

    private static final Map<Byte, FlagReason> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(FlagReason.class)
                .stream()
                .collect(Collectors.toMap(flagReason -> flagReason.stateValue, flagReason -> flagReason)));
    }

    static FlagReason valueOf(int stateValue) {
        return lookup.get((byte) stateValue);
    }
}
