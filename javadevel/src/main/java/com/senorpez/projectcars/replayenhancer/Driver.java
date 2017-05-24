package com.senorpez.projectcars.replayenhancer;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import com.fasterxml.jackson.annotation.JsonTypeName;

import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;

@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, include = JsonTypeInfo.As.WRAPPER_OBJECT)
@JsonTypeName("driver")
class Driver {
    private Byte index;
    @JsonProperty("name")
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

    List<SectorTime> getSectorTimes() {
        return sectorTimes;
    }

    void addSectorTime(TelemetryDataPacket packet) {
        TelemetryDataPacket.ParticipantInfo participantInfo = packet.getParticipantInfo().get(index);
        SectorTime sectorTime = new SectorTime(
                participantInfo.getLastSectorTime(),
                participantInfo.getCurrentSector(),
                participantInfo.isLapInvalidated());

        if (sectorTime.getTime() == -123.0) {
            return;
        }

        if (sectorTimes.size() == 0) {
            sectorTimes.add(sectorTime);
            return;
        }

        SectorTime previousSectorTime = sectorTimes.get(sectorTimes.size() - 1);
        if (!previousSectorTime.getTime().equals(sectorTime.getTime())
                || !previousSectorTime.getSector().equals(sectorTime.getSector())) {
            sectorTimes.add(sectorTime);
        }
    }

    @JsonProperty("bestLap")
    private Float getBestLap() {
        // TODO: 5/24/2017 Check against lap validity.
        return getLapTimes().size() > 0 ? Collections.min(getLapTimes()) : null;
    }

    private Float getBestSector(CurrentSector sector) {
        // TODO: 5/24/2017 Check against lap validity.
        List<Float> times = sectorTimes.stream()
                .filter(sectorTime -> sectorTime.getSector() == sector)
                .map(SectorTime::getTime)
                .collect(Collectors.toList());
        return times.size() > 0 ? Collections.min(times) : null;
    }

    @JsonProperty("bestSector1")
    private Float getBestSector1() {
        return getBestSector(CurrentSector.SECTOR_SECTOR1);
    }

    @JsonProperty("bestSector2")
    private Float getBestSector2() {
        return getBestSector(CurrentSector.SECTOR_SECTOR2);
    }

    @JsonProperty("bestSector3")
    private Float getBestSector3() {
        return getBestSector(CurrentSector.SECTOR_START);
    }

    @JsonProperty("lapsComplete")
    private Integer getLapsComplete() {
        return getLapTimes().size();
    }

    @JsonProperty("lapTimes")
    private List<Float> getLapTimes() {
        if (sectorTimes.size() == 0) {
            return new ArrayList<>();
        }

        List<SectorTime> times = sectorTimes;
        while (times.get(0).getSector() != CurrentSector.SECTOR_SECTOR1) {
            times.remove(0);
        }

        Integer partitionSize = 3;
        List<List<SectorTime>> partitions = new ArrayList<>();
        for (int i = 0; i < times.size(); i += partitionSize) {
            List<SectorTime> chunk = times.subList(i, Math.min(i + partitionSize, times.size()));
            if (chunk.size() == partitionSize) partitions.add(chunk);
        }

        return partitions.stream()
                .map(sectorTimes -> sectorTimes.stream()
                        .map(SectorTime::getTime)
                        .reduce((sectorTime, sectorTime1) -> sectorTime + sectorTime1)
                        .orElse(0f))
                .collect(Collectors.toList());
    }

    @JsonProperty("raceTime")
    private Float getRaceTime() {
        return getLapTimes().size() > 0
                ? getLapTimes().stream().reduce((lapTime, lapTime2) -> lapTime + lapTime2).orElse(0f)
                : null;
    }
}
