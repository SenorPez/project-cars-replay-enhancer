package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum JoyPad {
    BUTTON_1(1),
    BUTTON_2(2),
    BUTTON_3(4),
    BUTTON_4(8),
    BUTTON_5(16, "Start", "Start", "Option"),
    BUTTON_6(32, "Back", "Back", null),
    BUTTON_7(64, "L3", "L3", "L3"),
    BUTTON_8(128, "R3", "R3", "R3"),
    BUTTON_9(256, "LB", "LB", "LB"),
    BUTTON_10(512, "RB", "RB", "RB"),
    BUTTON_11(1024),
    BUTTON_12(2048),
    BUTTON_13(4096, "A", "A", "Cross"),
    BUTTON_14(8192, "B", "B", "Circle"),
    BUTTON_15(16384, "X", "X", "Square"),
    BUTTON_16(32768, "Y", "Y", "Triangle");

    private final Integer stateValue;
    private final String PCButtonName;
    private final String XBoxButtonName;
    private final String PS4ButtonName;

    JoyPad(Integer stateValue) {
        this.stateValue = stateValue;
        this.PCButtonName = null;
        this.XBoxButtonName = null;
        this.PS4ButtonName = null;
    }

    JoyPad(Integer stateValue, String PCButtonName, String XBoxButtonName, String PS4ButtonName) {
        this.stateValue = stateValue;
        this.PCButtonName = PCButtonName;
        this.XBoxButtonName = XBoxButtonName;
        this.PS4ButtonName = PS4ButtonName;
    }

    private static final Map<Integer, JoyPad> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(JoyPad.class)
                .stream()
                .collect(Collectors.toMap(joypad -> joypad.stateValue, joypad -> joypad)));
    }

    static JoyPad valueOf(int stateValue) {
        return lookup.get(stateValue);
    }

    Boolean isSet(Integer joyPad) {
        return (stateValue & joyPad) != 0;
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
