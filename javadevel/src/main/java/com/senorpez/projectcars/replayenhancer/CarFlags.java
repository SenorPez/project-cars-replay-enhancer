package com.senorpez.projectcars.replayenhancer;

enum CarFlags {
    CAR_HEADLIGHT(1),
    CAR_ENGINE_ACTIVE(1 << 1),
    CAR_ENGINE_WARNING(1 << 2),
    CAR_SPEED_LIMITER(1 << 3),
    CAR_ABS(1 << 4),
    CAR_HANDBRAKE(1 << 5),
    CAR_STABILITY(1 << 6),
    CAR_TRACTION_CONTROL(1 << 7);

    private final Byte stateValue;

    CarFlags(int stateValue) {
        this.stateValue = (byte) stateValue;
    }

    Boolean isSet(Short carFlags) {
        return (stateValue & carFlags) != 0;
    }
}
