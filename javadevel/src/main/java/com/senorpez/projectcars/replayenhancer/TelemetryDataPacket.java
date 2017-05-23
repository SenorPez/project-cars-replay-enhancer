package com.senorpez.projectcars.replayenhancer;

import java.io.DataInputStream;
import java.io.IOException;
import java.io.Serializable;
import java.nio.ByteBuffer;
import java.nio.ByteOrder;
import java.util.Arrays;
import java.util.List;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class TelemetryDataPacket extends Packet {
    enum State {
        /*
        State transition graph:
        LOADING -> PRE_RACE_PAUSED
        PRE_RACE_PAUSED -> PRE_RACE
        PRE_RACE -> RACING
        RACING -> LOADING
               -> FINISHED
         */
        LOADING {  /* Not sure on this. Could be Restarting? */
            @Override
            public Boolean raceFinished(final State previousState) {
                return previousState == State.RACING;
            }
        },
        PRE_RACE_PAUSED,
        PRE_RACE {
            @Override
            public Boolean raceStarted() {
                return true;
            }
        },
        RACING,
        FINISHED {
            @Override
            public Boolean raceFinished(final State previousState) {
                return false;
            }

            @Override
            public Boolean raceFinishedTelemetryExhausted() {
                return true;
            }
        },
        UNDEFINED {
            @Override
            public Boolean raceFinishedTelemetryExhausted() {
                return true;
            }
        };

        public Boolean raceStarted() {
            return false;
        }

        public Boolean raceFinished(final State previousState) {
            return previousState == State.FINISHED;
        }

        public Boolean raceFinishedTelemetryExhausted() {
            return false;
        }
    }

    class ParticipantInfo implements Serializable {
        private final List<Short> worldPosition;
        private final Integer currentLapDistance;
        private final Short racePosition;
        private final Short lapsCompleted;
        private final Short currentLap;
        private final Short sector;
        private final Float lastSectorTime;

        ParticipantInfo(DataInputStream data) throws IOException {
            this.worldPosition = IntStream.range(0, 3).mapToObj((IntFunctionThrows<Short>) value -> data.readShort()).collect(ImmutableListCollector.toImmutableList());
            this.currentLapDistance = data.readUnsignedShort();
            this.racePosition = (short) data.readUnsignedByte();
            this.lapsCompleted = (short) data.readUnsignedByte();
            this.currentLap = (short) data.readUnsignedByte();
            this.sector = (short) data.readUnsignedByte();
            this.lastSectorTime = getLittleFloat(data);
        }

        List<Float> getWorldPosition() {
            return Stream
                    .of(
                            worldPosition.get(0) + ((sector >>> 6) / 4.0f),
                            (float) worldPosition.get(1),
                            worldPosition.get(2) + (((48 & sector) >>> 4) / 4.0f))
                    .collect(ImmutableListCollector.toImmutableList());
        }

        Integer getCurrentLapDistance() {
            return currentLapDistance;
        }

        Short getRacePosition() {
            Integer mask = 127; /* 0111 1111 */
            return Integer.valueOf(mask & racePosition).shortValue();
        }

        Boolean isActive() {
            Integer mask = 128; /* 1000 0000 */
            return (mask & racePosition) != 0;
        }

        Short getLapsCompleted() {
            Integer mask = 127; /* 0111 1111 */
            return Integer.valueOf(mask * lapsCompleted).shortValue();
        }

        Boolean isLapInvalidated() {
            Integer mask = 128; /* 1000 0000 */
            return (mask & lapsCompleted) != 0;
        }

        Short getCurrentLap() {
            return currentLap;
        }

        CurrentSector getCurrentSector() {
            Integer mask = 7; /* 0000 0111 */
            return CurrentSector.valueOf(mask & sector);
        }

        Boolean isSameClass() {
            Integer mask = 8; /* 0000 1000 */
            return (mask & sector) != 0;
        }

        Float getLastSectorTime() {
            return lastSectorTime;
        }
    }

    private final static PacketType packetType = PacketType.TELEMETRY;

    private final Short gameSessionState;

    private final Byte viewedParticipantIndex;
    private final Byte numParticipants;

    private final Short unfilteredThrottle;
    private final Short unfilteredBrake;
    private final Byte unfilteredSteering;
    private final Short unfilteredClutch;
    private final Short raceStateFlags;

    private final Short lapsInEvent;

    private final Float bestLapTime;
    private final Float lastLapTime;
    private final Float currentTime;
    private final Float splitTimeAhead;
    private final Float splitTimeBehind;
    private final Float splitTime;
    private final Float eventTimeRemaining;
    private final Float personalFastestLapTime;
    private final Float worldFastestLapTime;
    private final Float currentSector1Time;
    private final Float currentSector2Time;
    private final Float currentSector3Time;
    private final Float fastestSector1Time;
    private final Float fastestSector2Time;
    private final Float fastestSector3Time;
    private final Float personalFastestSector1Time;
    private final Float personalFastestSector2Time;
    private final Float personalFastestSector3Time;
    private final Float worldFastestSector1Time;
    private final Float worldFastestSector2Time;
    private final Float worldFastestSector3Time;

    private final Integer joyPad;

    private final Short highestFlag;

    private final Short pitModeSchedule;

    private final Short oilTemp;
    private final Integer oilPressure;
    private final Short waterTemp;
    private final Integer waterPressure;
    private final Integer fuelPressure;
    private final Short carFlags;
    private final Short fuelCapacity;
    private final Short brake;
    private final Short throttle;
    private final Short clutch;
    private final Byte steering;
    private final Float fuelLevel;
    private final Float speed;
    private final Integer rpm;
    private final Integer maxRpm;
    private final Short gearNumGears;
    private final Short boostAmount;
    private final Byte enforcedPitStopLap;
    private final Short crashState;

    private final Float odometer;
    private final List<Float> orientation;
    private final List<Float> localVelocity;
    private final List<Float> worldVelocity;
    private final List<Float> angularVelocity;
    private final List<Float> localAcceleration;
    private final List<Float> worldAcceleration;
    private final List<Float> extentsCentre;

    private final List<Short> tyreFlags;
    private final List<Short> terrain;
    private final List<Float> tyreY;
    private final List<Float> tyreRps;
    private final List<Float> tyreSlipSpeed;
    private final List<Short> tyreTemp;
    private final List<Short> tyreGrip;
    private final List<Float> tyreHeightAboveGround;
    private final List<Float> tyreLateralStiffness;
    private final List<Short> tyreWear;
    private final List<Short> brakeDamage;
    private final List<Short> suspensionDamage;
    private final List<Short> brakeTemp;
    private final List<Integer> tyreTreadTemp;
    private final List<Integer> tyreLayerTemp;
    private final List<Integer> tyreCarcassTemp;
    private final List<Integer> tyreRimTemp;
    private final List<Integer> tyreInternalAirTemp;
    private final List<Float> wheelLocalPositionY;
    private final List<Float> rideHeight;
    private final List<Float> suspensionTravel;
    private final List<Float> suspensionVelocity;
    private final List<Integer> airPressure;

    private final Float engineSpeed;
    private final Float engineTorque;

    private final Short aeroDamage;
    private final Short engineDamage;

    private final Byte ambientTemperature;
    private final Byte trackTemperature;
    private final Short rainDensity;
    private final Byte windSpeed;
    private final Byte windDirectionX;
    private final Byte windDirectionY;

    private final List<ParticipantInfo> participantInfo;

    private final Float trackLength;
    private final List<Short> wings;
    private final Short dPad;

    TelemetryDataPacket(DataInputStream data) throws IOException, InvalidPacketException {
        super(data);
        if (!isCorrectPacketType(packetType)) {
            throw new InvalidPacketException();
        }

        this.gameSessionState = (short) data.readUnsignedByte();

        this.viewedParticipantIndex = data.readByte();
        this.numParticipants = data.readByte();

        this.unfilteredThrottle = (short) data.readUnsignedByte();
        this.unfilteredBrake = (short) data.readUnsignedByte();
        this.unfilteredSteering = data.readByte();
        this.unfilteredClutch = (short) data.readUnsignedByte();
        this.raceStateFlags = (short) data.readUnsignedByte();

        this.lapsInEvent = (short) data.readUnsignedByte();

        this.bestLapTime = getLittleFloat(data);
        this.lastLapTime = getLittleFloat(data);
        this.currentTime = getLittleFloat(data);
        this.splitTimeAhead = getLittleFloat(data);
        this.splitTimeBehind = getLittleFloat(data);
        this.splitTime = getLittleFloat(data);
        this.eventTimeRemaining = getLittleFloat(data);
        this.personalFastestLapTime = getLittleFloat(data);
        this.worldFastestLapTime = getLittleFloat(data);
        this.currentSector1Time = getLittleFloat(data);
        this.currentSector2Time = getLittleFloat(data);
        this.currentSector3Time = getLittleFloat(data);
        this.fastestSector1Time = getLittleFloat(data);
        this.fastestSector2Time = getLittleFloat(data);
        this.fastestSector3Time = getLittleFloat(data);
        this.personalFastestSector1Time = getLittleFloat(data);
        this.personalFastestSector2Time = getLittleFloat(data);
        this.personalFastestSector3Time = getLittleFloat(data);
        this.worldFastestSector1Time = getLittleFloat(data);
        this.worldFastestSector2Time = getLittleFloat(data);
        this.worldFastestSector3Time = getLittleFloat(data);

        this.joyPad = data.readUnsignedShort();

        this.highestFlag = (short) data.readUnsignedByte();

        this.pitModeSchedule = (short) data.readUnsignedByte();

        this.oilTemp = data.readShort();
        this.oilPressure = data.readUnsignedShort();
        this.waterTemp = data.readShort();
        this.waterPressure = data.readUnsignedShort();
        this.fuelPressure = data.readUnsignedShort();
        this.carFlags = (short) data.readUnsignedByte();
        this.fuelCapacity = (short) data.readUnsignedByte();
        this.brake = (short) data.readUnsignedByte();
        this.throttle = (short) data.readUnsignedByte();
        this.clutch = (short) data.readUnsignedByte();
        this.steering = data.readByte();
        this.fuelLevel = getLittleFloat(data);
        this.speed = getLittleFloat(data);
        this.rpm = data.readUnsignedShort();
        this.maxRpm = data.readUnsignedShort();
        this.gearNumGears = (short) data.readUnsignedByte();
        this.boostAmount = (short) data.readUnsignedByte();
        this.enforcedPitStopLap = data.readByte();
        this.crashState = (short) data.readUnsignedByte();

        this.odometer = getLittleFloat(data);
        this.orientation = IntStream.range(0, 3).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.localVelocity = IntStream.range(0, 3).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.worldVelocity = IntStream.range(0, 3).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.angularVelocity = IntStream.range(0, 3).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.localAcceleration = IntStream.range(0, 3).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.worldAcceleration = IntStream.range(0, 3).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.extentsCentre = IntStream.range(0, 3).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());

        this.tyreFlags = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Short>) value -> (short) data.readUnsignedByte()).collect(ImmutableListCollector.toImmutableList());
        this.terrain = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Short>) value -> (short) data.readUnsignedByte()).collect(ImmutableListCollector.toImmutableList());
        this.tyreY = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreRps = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreSlipSpeed = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreTemp = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Short>) value -> (short) data.readUnsignedByte()).collect(ImmutableListCollector.toImmutableList());
        this.tyreGrip = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Short>) value -> (short) data.readUnsignedByte()).collect(ImmutableListCollector.toImmutableList());
        this.tyreHeightAboveGround = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreLateralStiffness = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreWear = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Short>) value -> (short) data.readUnsignedByte()).collect(ImmutableListCollector.toImmutableList());
        this.brakeDamage = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Short>) value -> (short) data.readUnsignedByte()).collect(ImmutableListCollector.toImmutableList());
        this.suspensionDamage = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Short>) value -> (short) data.readUnsignedByte()).collect(ImmutableListCollector.toImmutableList());
        this.brakeTemp = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Short>) value -> data.readShort()).collect(ImmutableListCollector.toImmutableList());
        this.tyreTreadTemp = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Integer>) value -> data.readUnsignedShort()).collect(ImmutableListCollector.toImmutableList());
        this.tyreLayerTemp = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Integer>) value -> data.readUnsignedShort()).collect(ImmutableListCollector.toImmutableList());
        this.tyreCarcassTemp = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Integer>) value -> data.readUnsignedShort()).collect(ImmutableListCollector.toImmutableList());
        this.tyreRimTemp = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Integer>) value -> data.readUnsignedShort()).collect(ImmutableListCollector.toImmutableList());
        this.tyreInternalAirTemp = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Integer>) value -> data.readUnsignedShort()).collect(ImmutableListCollector.toImmutableList());
        this.wheelLocalPositionY = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.rideHeight = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.suspensionTravel = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.suspensionVelocity = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Float>) value -> getLittleFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.airPressure = IntStream.range(0, 4).mapToObj((IntFunctionThrows<Integer>) value -> data.readUnsignedShort()).collect(ImmutableListCollector.toImmutableList());

        this.engineSpeed = getLittleFloat(data);
        this.engineTorque = getLittleFloat(data);

        this.aeroDamage = (short) data.readUnsignedByte();
        this.engineDamage = (short) data.readUnsignedByte();

        this.ambientTemperature = data.readByte();
        this.trackTemperature = data.readByte();
        this.rainDensity = (short) data.readUnsignedByte();
        this.windSpeed = data.readByte();
        this.windDirectionX = data.readByte();
        this.windDirectionY = data.readByte();

        this.participantInfo = IntStream.range(0, 56).mapToObj((IntFunctionThrows<ParticipantInfo>) value -> new ParticipantInfo(data)).collect(ImmutableListCollector.toImmutableList());

        this.trackLength = getLittleFloat(data);
        this.wings = IntStream.range(0, 2).mapToObj((IntFunctionThrows<Short>) value -> (short) data.readUnsignedByte()).collect(ImmutableListCollector.toImmutableList());
        this.dPad = (short) data.readUnsignedByte();
    }

    @Override
    PacketType getPacketType() {
        return packetType;
    }

    GameState getGameState() {
        Integer mask = 15; /* 0000 1111 */
        return GameState.valueOf(mask & gameSessionState);
    }

    SessionState getSessionState() {
        return SessionState.valueOf(gameSessionState >>> 4);
    }

    RaceState getRaceState() {
        Integer mask = 7; /* 0000 0111 */
        return RaceState.valueOf(mask & raceStateFlags);
    }

    Boolean isLapInvalidated() {
        Integer mask = 8; /* 0000 1000 */
        return (mask & raceStateFlags) != 0;
    }

    Boolean isAntiLockActive() {
        Integer mask = 16; /* 0001 0000 */
        return (mask & raceStateFlags) != 0;
    }

    Boolean isBoostActive() {
        Integer mask = 32; /* 0010 0000 */
        return (mask & raceStateFlags) != 0;
    }

    Byte getViewedParticipantIndex() {
        return viewedParticipantIndex;
    }

    Byte getNumParticipants() {
        return numParticipants;
    }

    Float getUnfilteredThrottle() {
        return unfilteredThrottle / 255.0f;
    }

    Float getUnfilteredBrake() {
        return unfilteredBrake / 255.0f;
    }

    Float getUnfilteredSteering() {
        return unfilteredSteering / 127.0f;
    }

    Float getUnfilteredClutch() {
        return unfilteredClutch / 255.0f;
    }

    Float getTrackLength() {
        return trackLength;
    }

    Short getLapsInEvent() {
        return lapsInEvent;
    }

    Float getBestLapTime() {
        return bestLapTime;
    }

    Float getLastLapTime() {
        return lastLapTime;
    }

    Float getCurrentTime() {
        return currentTime;
    }

    Float getSplitTimeAhead() {
        return splitTimeAhead;
    }

    Float getSplitTimeBehind() {
        return splitTimeBehind;
    }

    Float getSplitTime() {
        return splitTime;
    }

    Float getEventTimeRemaining() {
        return eventTimeRemaining;
    }

    Float getPersonalFastestLapTime() {
        return personalFastestLapTime;
    }

    Float getWorldFastestLapTime() {
        return worldFastestLapTime;
    }

    Float getCurrentSector1Time() {
        return currentSector1Time;
    }

    Float getCurrentSector2Time() {
        return currentSector2Time;
    }

    Float getCurrentSector3Time() {
        return currentSector3Time;
    }

    Float getFastestSector1Time() {
        return fastestSector1Time;
    }

    Float getFastestSector2Time() {
        return fastestSector2Time;
    }

    Float getFastestSector3Time() {
        return fastestSector3Time;
    }

    Float getPersonalFastestSector1Time() {
        return personalFastestSector1Time;
    }

    Float getPersonalFastestSector2Time() {
        return personalFastestSector2Time;
    }

    Float getPersonalFastestSector3Time() {
        return personalFastestSector3Time;
    }

    Float getWorldFastestSector1Time() {
        return worldFastestSector1Time;
    }

    Float getWorldFastestSector2Time() {
        return worldFastestSector2Time;
    }

    Float getWorldFastestSector3Time() {
        return worldFastestSector3Time;
    }

    FlagColour getHighestFlagColor() {
        Integer mask = 15; /* 0000 1111 */
        return FlagColour.valueOf(mask & highestFlag);
    }

    FlagReason getHighestFlagReason() {
        return FlagReason.valueOf(highestFlag >>> 4);
    }

    PitMode getPitMode() {
        Integer mask = 15; /* 0000 1111 */
        return PitMode.valueOf(mask & pitModeSchedule);
    }

    PitSchedule getPitSchedule() {
        return PitSchedule.valueOf(pitModeSchedule >>> 4);
    }

    Boolean isHeadlight() {
        return CarFlags.CAR_HEADLIGHT.isSet(carFlags);
    }

    Boolean isEngineActive() {
        return CarFlags.CAR_ENGINE_ACTIVE.isSet(carFlags);
    }

    Boolean isEngineWarning() {
        return CarFlags.CAR_ENGINE_WARNING.isSet(carFlags);
    }

    Boolean isSpeedLimiter() {
        return CarFlags.CAR_SPEED_LIMITER.isSet(carFlags);
    }

    Boolean isAbs() {
        return CarFlags.CAR_ABS.isSet(carFlags);
    }

    Boolean isHandbrake() {
        return CarFlags.CAR_HANDBRAKE.isSet(carFlags);
    }

    Boolean isStability() {
        return CarFlags.CAR_STABILITY.isSet(carFlags);
    }

    Boolean isTractionControl() {
        return CarFlags.CAR_TRACTION_CONTROL.isSet(carFlags);
    }

    Short getOilTemp() {
        return oilTemp;
    }

    Integer getOilPressure() {
        return oilPressure;
    }

    Short getWaterTemp() {
        return waterTemp;
    }

    Integer getWaterPressure() {
        return waterPressure;
    }

    Integer getFuelPressure() {
        return fuelPressure;
    }

    Short getFuelCapacity() {
        return fuelCapacity;
    }

    Float getBrake() {
        return brake / 255.0f;
    }

    Float getFuelLevel() {
        return fuelLevel;
    }

    Float getSpeed() {
        return speed;
    }

    Integer getRpm() {
        return rpm;
    }

    Integer getMaxRpm() {
        return maxRpm;
    }

    Float getThrottle() {
        return throttle / 255.0f;
    }

    Float getClutch() {
        return clutch / 255.0f;
    }

    Float getSteering() {
        return steering / 127.0f;
    }

    Short getGear() {
        Integer mask = 15; /* 0000 1111 */
        return Integer.valueOf(mask * gearNumGears).shortValue();
    }

    Short getNumGears() {
        return Integer.valueOf(gearNumGears >>> 4).shortValue();
    }

    Float getOdometer() {
        return odometer;
    }

    Short getBoostAmount() {
        return boostAmount;
    }

    List<Float> getOrientation() {
        return orientation;
    }

    List<Float> getLocalVelocity() {
        return localVelocity;
    }

    List<Float> getWorldVelocity() {
        return worldVelocity;
    }

    List<Float> getAngularVelocity() {
        return angularVelocity;
    }

    List<Float> getLocalAcceleration() {
        return localAcceleration;
    }

    List<Float> getWorldAcceleration() {
        return worldAcceleration;
    }

    List<Float> getExtentsCentre() {
        return extentsCentre;
    }

    List<Boolean> isTyreAttached() {
        return tyreFlags.stream().map(TyreFlags.TYRE_ATTACHED::isSet).collect(ImmutableListCollector.toImmutableList());
    }

    List<Boolean> isTyreInflated() {
        return tyreFlags.stream().map(TyreFlags.TYRE_INFLATED::isSet).collect(ImmutableListCollector.toImmutableList());
    }

    List<Boolean> isTyreIsOnGround() {
        return tyreFlags.stream().map(TyreFlags.TYRE_IS_ON_GROUND::isSet).collect(ImmutableListCollector.toImmutableList());
    }

    List<TerrainMaterial> getTerrain() {
        return terrain.stream().map(TerrainMaterial::valueOf).collect(ImmutableListCollector.toImmutableList());
    }

    List<Float> getTyreY() {
        return tyreY;
    }

    List<Float> getTyreRps() {
        return tyreRps;
    }

    List<Float> getTyreSlipSpeed() {
        return tyreSlipSpeed;
    }

    List<Short> getTyreTemp() {
        return tyreTemp;
    }

    List<Float> getTyreGrip() {
        return tyreGrip.stream().map(tyreGrip -> tyreGrip / 255.0f).collect(ImmutableListCollector.toImmutableList());
    }

    List<Float> getTyreHeightAboveGround() {
        return tyreHeightAboveGround;
    }

    List<Float> getTyreLateralStiffness() {
        return tyreLateralStiffness;
    }

    List<Float> getTyreWear() {
        return tyreWear.stream().map(tyreWear -> tyreWear / 255.0f).collect(ImmutableListCollector.toImmutableList());
    }

    List<Float> getBrakeDamage() {
        return brakeDamage.stream().map(brakeDamage -> brakeDamage / 255.0f).collect(ImmutableListCollector.toImmutableList());
    }

    List<Float> getSuspensionDamage() {
        return suspensionDamage.stream().map(suspensionDamage -> suspensionDamage / 255.0f).collect(ImmutableListCollector.toImmutableList());
    }

    List<Short> getBrakeTemp() {
        return brakeTemp;
    }

    List<Integer> getTyreTreadTemp() {
        return tyreTreadTemp;
    }

    List<Integer> getTyreLayerTemp() {
        return tyreLayerTemp;
    }

    List<Integer> getTyreCarcassTemp() {
        return tyreCarcassTemp;
    }

    List<Integer> getTyreRimTemp() {
        return tyreRimTemp;
    }

    List<Integer> getTyreInternalAirTemp() {
        return tyreInternalAirTemp;
    }

    List<Float> getWheelLocalPositionY() {
        return wheelLocalPositionY;
    }

    List<Float> getRideHeight() {
        return rideHeight;
    }

    List<Float> getSuspensionTravel() {
        return suspensionTravel;
    }

    List<Float> getSuspensionVelocity() {
        return suspensionVelocity;
    }

    List<Integer> getAirPressure() {
        return airPressure;
    }

    Float getEngineSpeed() {
        return engineSpeed;
    }

    Float getEngineTorque() {
        return engineTorque;
    }

    List<Short> getWings() {
        return wings;
    }

    Byte getEnforcedPitStopLap() {
        return enforcedPitStopLap;
    }

    CrashDamageState getCrashState() {
        Integer mask = 15; /* 0000 1111 */
        return CrashDamageState.valueOf(mask & crashState);
    }

    Float getAeroDamage() {
        return aeroDamage / 255.0f;
    }

    Float getEngineDamage() {
        return engineDamage / 255.0f;
    }

    Byte getAmbientTemperature() {
        return ambientTemperature;
    }

    Byte getTrackTemperature() {
        return trackTemperature;
    }

    Short getRainDensity() {
        return rainDensity;
    }

    Byte getWindSpeed() {
        return windSpeed;
    }

    Byte getWindDirectionX() {
        return windDirectionX;
    }

    Byte getWindDirectionY() {
        return windDirectionY;
    }

    Boolean isJoyPadButton1() {
        return JoyPad.BUTTON_1.isSet(joyPad);
    }

    Boolean isJoyPadButton2() {
        return JoyPad.BUTTON_2.isSet(joyPad);
    }

    Boolean isJoyPadButton3() {
        return JoyPad.BUTTON_3.isSet(joyPad);
    }

    Boolean isJoyPadButton4() {
        return JoyPad.BUTTON_4.isSet(joyPad);
    }

    Boolean isJoyPadButton5() {
        return JoyPad.BUTTON_5.isSet(joyPad);
    }

    Boolean isJoyPadButton6() {
        return JoyPad.BUTTON_6.isSet(joyPad);
    }

    Boolean isJoyPadButton7() {
        return JoyPad.BUTTON_7.isSet(joyPad);
    }

    Boolean isJoyPadButton8() {
        return JoyPad.BUTTON_8.isSet(joyPad);
    }

    Boolean isJoyPadButton9() {
        return JoyPad.BUTTON_9.isSet(joyPad);
    }

    Boolean isJoyPadButton10() {
        return JoyPad.BUTTON_10.isSet(joyPad);
    }

    Boolean isJoyPadButton11() {
        return JoyPad.BUTTON_11.isSet(joyPad);
    }

    Boolean isJoyPadButton12() {
        return JoyPad.BUTTON_12.isSet(joyPad);
    }

    Boolean isJoyPadButton13() {
        return JoyPad.BUTTON_13.isSet(joyPad);
    }

    Boolean isJoyPadButton14() {
        return JoyPad.BUTTON_14.isSet(joyPad);
    }

    Boolean isJoyPadButton15() {
        return JoyPad.BUTTON_15.isSet(joyPad);
    }

    Boolean isJoyPadButton16() {
        return JoyPad.BUTTON_16.isSet(joyPad);
    }

    Boolean isDPadButton1() {
        return DPad.BUTTON_1.isSet((int) (dPad >>> 4));
    }

    Boolean isDPadButton2() {
        return DPad.BUTTON_2.isSet((int) (dPad >>> 4));
    }

    Boolean isDPadButton3() {
        return DPad.BUTTON_3.isSet((int) (dPad >>> 4));
    }

    Boolean isDPadButton4() {
        return DPad.BUTTON_4.isSet((int) (dPad >>> 4));
    }

    Boolean isDPadButton5() {
        return DPad.BUTTON_5.isSet((int) (crashState >>> 4));
    }

    Boolean isDPadButton6() {
        return DPad.BUTTON_6.isSet((int) (crashState >>> 4));
    }

    Boolean isDPadButton7() {
        return DPad.BUTTON_7.isSet((int) (crashState >>> 4));
    }

    Boolean isDPadButton8() {
        return DPad.BUTTON_8.isSet((int) (crashState >>> 4));
    }

    List<ParticipantInfo> getParticipantInfo() {
        return participantInfo;
    }

    State getState() {
        if (getRaceState() == RaceState.RACE_NOT_STARTED) {
            if (getGameState() == GameState.GAME_INGAME_PAUSED) {
                return State.PRE_RACE_PAUSED;
            } else if (getGameState() == GameState.GAME_INGAME_PLAYING) {
                return State.PRE_RACE;
            }
        } else if (getRaceState() == RaceState.RACE_RACING) {
            return State.RACING;
        } else if (getRaceState() == RaceState.RACE_FINISHED) {
            return State.FINISHED;
        } else if (getGameState() == GameState.GAME_MAX
                && getSessionState() == SessionState.SESSION_INVALID
                && getRaceState() == RaceState.RACE_INVALID) {
            return State.LOADING;
        }
        System.out.printf("%s %s %s\n",
                getGameState(),
                getSessionState(),
                getRaceState());
        return State.UNDEFINED;
    }

    private static Float getLittleFloat(DataInputStream data) throws IOException {
        byte[] bytes = new byte[4];
        data.readFully(bytes);
        int asInt = (bytes[0] & 0xFF)
                | ((bytes[1] & 0xFF) << 8)
                | ((bytes[2] & 0xFF) << 16)
                | ((bytes[3] & 0xFF) << 24);
        return Float.intBitsToFloat(asInt);
    }
}
