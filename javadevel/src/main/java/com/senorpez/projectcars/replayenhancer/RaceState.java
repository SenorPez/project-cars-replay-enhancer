package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum RaceState {
    RACESTATE_INVALID(0),
    RACESTATE_NOT_STARTED(1),
    RACESTATE_RACING(2),
    RACESTATE_FINISHED(3),
    RACESTATE_DISQUALIFIED(4),
    RACESTATE_RETIRED(5),
    RACESTATE_DNF(6),
    RACESTATE_MAX(7);

    private final Byte stateValue;

    RaceState(int stateValue) {
        this.stateValue = (byte) stateValue;
    }

    private static final Map<Byte, RaceState> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(RaceState.class)
                .stream()
                .collect(Collectors.toMap(raceState -> raceState.stateValue, raceState -> raceState)));
    }

    static RaceState valueOf(int stateValue) {
        return lookup.get((byte) stateValue);
    }
}
