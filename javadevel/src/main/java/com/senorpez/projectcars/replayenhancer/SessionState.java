package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum SessionState {
    SESSION_INVALID(0),
    SESSION_PRACTICE(1),
    SESSION_TEST(2),
    SESSION_QUALIFY(3),
    SESSION_FORMATION_LAP(4),
    SESSION_RACE(5),
    SESSION_TIME_ATTACK(6),
    SESSION_MAX(7);

    private final Byte stateValue;

    SessionState(int stateValue) {
        this.stateValue = (byte) stateValue;
    }

    private static final Map<Byte, SessionState> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(SessionState.class)
                .stream()
                .collect(Collectors.toMap(sessionState -> sessionState.stateValue, sessionState -> sessionState)));
    }

    static SessionState valueOf(int stateValue) {
        return lookup.get((byte) stateValue);
    }
}
