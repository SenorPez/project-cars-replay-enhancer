package com.senorpez.projectcars.replayenhancer;

import java.util.EnumSet;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

enum TerrainMaterial {
    TERRAIN_ROAD(0),
    TERRAIN_LOW_GRIP_ROAD(1),
    TERRAIN_BUMPY_ROAD1(2),
    TERRAIN_BUMPY_ROAD2(3),
    TERRAIN_BUMPY_ROAD3(4),
    TERRAIN_MARBLES(5),
    TERRAIN_GRASSY_BERMS(6),
    TERRAIN_GRASS(7),
    TERRAIN_GRAVEL(8),
    TERRAIN_BUMPY_GRAVEL(9),
    TERRAIN_RUMBLE_STRIPS(10),
    TERRAIN_DRAINS(11),
    TERRAIN_TYREWALLS(12),
    TERRAIN_CEMENTWALLS(13),
    TERRAIN_GUARDRAILS(14),
    TERRAIN_SAND(15),
    TERRAIN_BUMPY_SAND(16),
    TERRAIN_DIRT(17),
    TERRAIN_BUMPY_DIRT(18),
    TERRAIN_DIRT_ROAD(19),
    TERRAIN_BUMPY_DIRT_ROAD(20),
    TERRAIN_PAVEMENT(21),
    TERRAIN_DIRT_BANK(22),
    TERRAIN_WOOD(23),
    TERRAIN_DRY_VERGE(24),
    TERRAIN_EXIT_RUMBLE_STRIPS(25),
    TERRAIN_GRASSCRETE(26),
    TERRAIN_LONG_GRASS(27),
    TERRAIN_SLOPE_GRASS(28),
    TERRAIN_COBBLES(29),
    TERRAIN_SAND_ROAD(30),
    TERRAIN_BAKED_CLAY(31),
    TERRAIN_ASTROTURF(32),
    TERRAIN_SNOWHALF(33),
    TERRAIN_SNOWFULL(34),
    TERRAIN_MAX(35);

    private final Byte stateValue;

    TerrainMaterial(int stateValue) {
        this.stateValue = (byte) stateValue;
    }

    private static final Map<Byte, TerrainMaterial> lookup = new HashMap<>();

    static {
        lookup.putAll(EnumSet.allOf(TerrainMaterial.class)
                .stream()
                .collect(Collectors.toMap(terrainMaterial -> terrainMaterial.stateValue, terrainMaterial -> terrainMaterial)));
    }

    static TerrainMaterial valueOf(int stateValue) {
        return lookup.get((byte) stateValue);
    }
}
