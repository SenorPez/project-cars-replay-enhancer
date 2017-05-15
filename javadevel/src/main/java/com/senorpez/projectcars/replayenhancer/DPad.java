package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum DPad {
    BUTTON_1(1, "Up"),
    BUTTON_2(2, "Down"),
    BUTTON_3(4, "Left"),
    BUTTON_4(8, "Right"),
    BUTTON_5(16),
    BUTTON_6(32),
    BUTTON_7(64),
    BUTTON_8(128);

    private final Integer stateValue;
    private final String PCButtonName;
    private final String XBoxButtonName;
    private final String PS4ButtonName;
    
    DPad(Integer stateValue) {
        this.stateValue = stateValue;
        this.PCButtonName = null;
        this.XBoxButtonName = null;
        this.PS4ButtonName = null;
    }
    
    DPad(Integer stateValue, String buttonName) {
        this.stateValue = stateValue;
        this.PCButtonName = buttonName;
        this.XBoxButtonName = buttonName;
        this.PS4ButtonName = buttonName;
    }

    private static final Map<Integer, DPad> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(DPad.class)
                .stream()
                .collect(Collectors.toMap(dPad -> dPad.stateValue, dPad -> dPad)));
    }

    static DPad valueOf(int stateValue) {
        return lookup.get(stateValue);
    }

    Boolean isSet(Short dPad) {
        return (stateValue & dPad) != 0;
    }

    String getPCButtonName() {
        return PCButtonName;
    }

    String getXBoxButtonName() {
        return XBoxButtonName;
    }

    String getPS4ButtonName() {
        return PS4ButtonName;
    }
}
