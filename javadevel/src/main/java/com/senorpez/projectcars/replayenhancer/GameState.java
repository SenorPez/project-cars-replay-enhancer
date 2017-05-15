package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum GameState {
    GAME_EXITED(0),
    GAME_FRONT_END(1),
    GAME_INGAME_PLAYING(2),
    GAME_INGAME_PAUSED(3),
    GAME_MAX(4);

    private final Byte stateValue;

    GameState(int stateValue) {
        this.stateValue = (byte) stateValue;
    }

    private static final Map<Byte, GameState> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(GameState.class)
                .stream()
                .collect(Collectors.toMap(gameState -> gameState.stateValue, gameState -> gameState)));
    }

    static GameState valueOf(int stateValue) {
        return lookup.get((byte) stateValue);
    }
}
