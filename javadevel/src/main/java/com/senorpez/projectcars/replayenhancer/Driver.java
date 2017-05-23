package com.senorpez.projectcars.replayenhancer;

import com.fasterxml.jackson.annotation.JsonProperty;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Map;
import java.util.concurrent.atomic.AtomicInteger;
import java.util.stream.Collectors;

class Driver {
    private Byte index;
    @JsonProperty("name")
    private final String name;
    @JsonProperty("sectorTimes")
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

    List<SectorTime> getSectorTimes() {
        return sectorTimes;
    }

    void addSectorTime(SectorTime sectorTime) {
        if (sectorTime.getTime() == -123.0) {
            return;
        }

        if (sectorTimes.size() == 0) {
            sectorTimes.add(sectorTime);
            return;
        }

        SectorTime previousSectorTime = sectorTimes.get(sectorTimes.size()-1);

        if (!previousSectorTime.getTime().equals(sectorTime.getTime())
                || !previousSectorTime.getSector().equals(sectorTime.getSector())) {
            sectorTimes.add(sectorTime);
        }
    }
}
