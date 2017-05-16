package com.senorpez.projectcars.replayenhancer;

class SectorTime {
    private final Float time;
    private final CurrentSector sector;
    private Boolean invalid;

    public SectorTime(Float time, CurrentSector sector, Boolean invalid) {
        this.time = time;
        this.sector = sector;
        this.invalid = invalid;
    }

    public Float getTime() {
        return time;
    }

    public CurrentSector getSector() {
        return sector;
    }

    public Boolean getInvalid() {
        return invalid;
    }

    public void setInvalid(Boolean invalid) {
        this.invalid = invalid;
    }
}
