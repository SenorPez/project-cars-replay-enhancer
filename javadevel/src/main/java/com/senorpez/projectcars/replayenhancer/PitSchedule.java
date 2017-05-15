package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum PitSchedule {
    PIT_SCHEDULE_NONE(0),
    PIT_SCHEDULE_STANDARD(1),
    PIT_SCHEDULE_DRIVE_THROUGH(2),
    PIT_SCHEDULE_STOP_GO(3),
    PIT_SCHEDULE_MAX(4);

    private final Byte stateValue;

    PitSchedule(int stateValue) {
        this.stateValue = (byte) stateValue;
    }

    private static final Map<Byte, PitSchedule> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(PitSchedule.class)
                .stream()
                .collect(Collectors.toMap(pitSchedule -> pitSchedule.stateValue, pitSchedule -> pitSchedule)));
    }

    static PitSchedule valueOf(int stateValue) {
        return lookup.get((byte) stateValue);
    }
}
