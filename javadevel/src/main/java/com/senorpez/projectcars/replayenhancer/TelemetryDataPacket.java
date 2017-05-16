package com.senorpez.projectcars.replayenhancer;

import java.nio.ByteBuffer;
import java.util.List;
import java.util.stream.IntStream;
import java.util.stream.Stream;

class TelemetryDataPacket extends Packet {
    class ParticipantInfo {
        private final List<Short> worldPosition;
        private final Integer currentLapDistance;
        private final Short racePosition;
        private final Short lapsCompleted;
        private final Short currentLap;
        private final Short sector;
        private final Float lastSectorTime;

        ParticipantInfo(ByteBuffer data) {
            this.worldPosition = IntStream.range(0, 3).mapToObj(value -> ReadSignedShort(data)).collect(ImmutableListCollector.toImmutableList());
            this.currentLapDistance = ReadUnsignedShort(data);
            this.racePosition = ReadUnsignedByte(data);
            this.lapsCompleted = ReadUnsignedByte(data);
            this.currentLap = ReadUnsignedByte(data);
            this.sector = ReadUnsignedByte(data);
            this.lastSectorTime = ReadFloat(data);
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

    private final static Short packetType = 0;

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

    TelemetryDataPacket(ByteBuffer data) throws InvalidPacketException {
        super(data);
        if (!isCorrectPacketType(packetType)) {
            throw new InvalidPacketException();
        }

        this.gameSessionState = ReadUnsignedByte(data);

        this.viewedParticipantIndex = ReadSignedByte(data);
        this.numParticipants = ReadSignedByte(data);

        this.unfilteredThrottle = ReadUnsignedByte(data);
        this.unfilteredBrake = ReadUnsignedByte(data);
        this.unfilteredSteering = ReadSignedByte(data);
        this.unfilteredClutch = ReadUnsignedByte(data);
        this.raceStateFlags = ReadUnsignedByte(data);

        this.lapsInEvent = ReadUnsignedByte(data);

        this.bestLapTime = ReadFloat(data);
        this.lastLapTime = ReadFloat(data);
        this.currentTime = ReadFloat(data);
        this.splitTimeAhead = ReadFloat(data);
        this.splitTimeBehind = ReadFloat(data);
        this.splitTime = ReadFloat(data);
        this.eventTimeRemaining = ReadFloat(data);
        this.personalFastestLapTime = ReadFloat(data);
        this.worldFastestLapTime = ReadFloat(data);
        this.currentSector1Time = ReadFloat(data);
        this.currentSector2Time = ReadFloat(data);
        this.currentSector3Time = ReadFloat(data);
        this.fastestSector1Time = ReadFloat(data);
        this.fastestSector2Time = ReadFloat(data);
        this.fastestSector3Time = ReadFloat(data);
        this.personalFastestSector1Time = ReadFloat(data);
        this.personalFastestSector2Time = ReadFloat(data);
        this.personalFastestSector3Time = ReadFloat(data);
        this.worldFastestSector1Time = ReadFloat(data);
        this.worldFastestSector2Time = ReadFloat(data);
        this.worldFastestSector3Time = ReadFloat(data);

        this.joyPad = ReadUnsignedShort(data);

        this.highestFlag = ReadUnsignedByte(data);

        this.pitModeSchedule = ReadUnsignedByte(data);

        this.oilTemp = ReadSignedShort(data);
        this.oilPressure = ReadUnsignedShort(data);
        this.waterTemp = ReadSignedShort(data);
        this.waterPressure = ReadUnsignedShort(data);
        this.fuelPressure = ReadUnsignedShort(data);
        this.carFlags = ReadUnsignedByte(data);
        this.fuelCapacity = ReadUnsignedByte(data);
        this.brake = ReadUnsignedByte(data);
        this.throttle = ReadUnsignedByte(data);
        this.clutch = ReadUnsignedByte(data);
        this.steering = ReadSignedByte(data);
        this.fuelLevel = ReadFloat(data);
        this.speed = ReadFloat(data);
        this.rpm = ReadUnsignedShort(data);
        this.maxRpm = ReadUnsignedShort(data);
        this.gearNumGears = ReadUnsignedByte(data);
        this.boostAmount = ReadUnsignedByte(data);
        this.enforcedPitStopLap = ReadSignedByte(data);
        this.crashState = ReadUnsignedByte(data);

        this.odometer = ReadFloat(data);
        this.orientation = IntStream.range(0, 3).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.localVelocity = IntStream.range(0, 3).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.worldVelocity = IntStream.range(0, 3).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.angularVelocity = IntStream.range(0, 3).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.localAcceleration = IntStream.range(0, 3).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.worldAcceleration = IntStream.range(0, 3).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.extentsCentre = IntStream.range(0, 3).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());

        this.tyreFlags = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedByte(data)).collect(ImmutableListCollector.toImmutableList());
        this.terrain = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedByte(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreY = IntStream.range(0, 4).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreRps = IntStream.range(0, 4).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreSlipSpeed = IntStream.range(0, 4).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreTemp = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedByte(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreGrip = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedByte(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreHeightAboveGround = IntStream.range(0, 4).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreLateralStiffness = IntStream.range(0, 4).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreWear = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedByte(data)).collect(ImmutableListCollector.toImmutableList());
        this.brakeDamage = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedByte(data)).collect(ImmutableListCollector.toImmutableList());
        this.suspensionDamage = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedByte(data)).collect(ImmutableListCollector.toImmutableList());
        this.brakeTemp = IntStream.range(0, 4).mapToObj(value -> ReadSignedShort(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreTreadTemp = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedShort(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreLayerTemp = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedShort(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreCarcassTemp = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedShort(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreRimTemp = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedShort(data)).collect(ImmutableListCollector.toImmutableList());
        this.tyreInternalAirTemp = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedShort(data)).collect(ImmutableListCollector.toImmutableList());
        this.wheelLocalPositionY = IntStream.range(0, 4).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.rideHeight = IntStream.range(0, 4).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.suspensionTravel = IntStream.range(0, 4).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.suspensionVelocity = IntStream.range(0, 4).mapToObj(value -> ReadFloat(data)).collect(ImmutableListCollector.toImmutableList());
        this.airPressure = IntStream.range(0, 4).mapToObj(value -> ReadUnsignedShort(data)).collect(ImmutableListCollector.toImmutableList());

        this.engineSpeed = ReadFloat(data);
        this.engineTorque = ReadFloat(data);

        this.aeroDamage = ReadUnsignedByte(data);
        this.engineDamage = ReadUnsignedByte(data);

        this.ambientTemperature = ReadSignedByte(data);
        this.trackTemperature = ReadSignedByte(data);
        this.rainDensity = ReadUnsignedByte(data);
        this.windSpeed = ReadSignedByte(data);
        this.windDirectionX = ReadSignedByte(data);
        this.windDirectionY = ReadSignedByte(data);

        this.participantInfo = IntStream.range(0, 56).mapToObj(value -> new ParticipantInfo(data)).collect(ImmutableListCollector.toImmutableList());

        this.trackLength = ReadFloat(data);
        this.wings = IntStream.range(0, 2).mapToObj(value -> ReadUnsignedByte(data)).collect(ImmutableListCollector.toImmutableList());
        this.dPad = ReadUnsignedByte(data);
    }

    @Override
    Short getPacketType() {
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
}
