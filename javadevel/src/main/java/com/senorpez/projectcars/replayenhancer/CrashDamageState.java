package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum CrashDamageState {
    CRASH_DAMAGE_NONE(0),
    CRASH_DAMAGE_OFFTRACK(1),
    CRASH_DAMAGE_LARGE_PROP(2),
    CRASH_DAMAGE_SPINNING(3),
    CRASH_DAMAGE_ROLLING(4),
    CRASH_DAMAGE_MAX(5);

    private final Byte stateValue;

    CrashDamageState(int stateValue) {
        this.stateValue = (byte) stateValue;
    }
    
    private static final Map<Byte, CrashDamageState> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(CrashDamageState.class)
                .stream()
                .collect(Collectors.toMap(crashDamageState -> crashDamageState.stateValue, crashDamageState -> crashDamageState)));
    }

    static CrashDamageState valueOf(int stateValue) {
        return lookup.get((byte) stateValue);
    }
}
