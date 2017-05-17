package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum SessionState {
    SESSION_INVALID,
    SESSION_PRACTICE,
    SESSION_TEST,
    SESSION_QUALIFY,
    SESSION_FORMATION_LAP,
    SESSION_RACE,
    SESSION_TIME_ATTACK,
    SESSION_MAX;

    private static final Map<Integer, SessionState> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(SessionState.class)
                .stream()
                .collect(Collectors.toMap(Enum::ordinal, sessionState -> sessionState)));
    }

    static SessionState valueOf(int stateValue) {
        return lookup.get(stateValue);
    }
}
