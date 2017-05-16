package com.senorpez.projectcars.replayenhancer;

import java.util.ArrayList;
import java.util.List;

class Driver {
    private Byte index;
    private final String name;
    private final List<SectorTime> sectorTimes;

    Driver(Byte index, String name) {
        this.index = index;
        this.name = name;
        this.sectorTimes = new ArrayList<>();
    }

    Byte getIndex() {
        return index;
    }

    String getName() {
        return name;
    }

    public List<SectorTime> getSectorTimes() {
        return sectorTimes;
    }
}
