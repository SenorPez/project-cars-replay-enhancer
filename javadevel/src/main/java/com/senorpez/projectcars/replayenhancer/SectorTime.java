package com.senorpez.projectcars.replayenhancer;

import com.fasterxml.jackson.annotation.JsonProperty;

class SectorTime {
    @JsonProperty("time")
    private final Float time;
    @JsonProperty("sector")
    private final CurrentSector sector;
    private Boolean invalid;

    SectorTime(Float time, CurrentSector sector, Boolean invalid) {
        this.time = time;
        this.sector = sector;
        this.invalid = invalid;
    }

    Float getTime() {
        return time;
    }

    CurrentSector getSector() {
        return sector;
    }

    Boolean getInvalid() {
        return invalid;
    }

    void setInvalid(Boolean invalid) {
        this.invalid = invalid;
    }
}
