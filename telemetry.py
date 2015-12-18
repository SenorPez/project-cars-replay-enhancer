import binascii
import glob
import natsort
import struct

data = list()
for a in natsort.natsorted(glob.glob('./packetdata/pdata*')):
	with open(a, 'rb') as f:
		data.append(f.read())

data = [x for x in data if len(x) == 1367]
telemetryData = list()

for tele in data:
	sBuildVersionNumber = struct.unpack("H", tele[0:2])[0]
	sPacketType = struct.unpack("B", tele[2:3])[0]
	
	sGameSessionState = struct.unpack("B", tele[3:4])[0]

	sViewedParticipantIndex = struct.unpack("b", tele[4:5])[0]
	sNumParticipants = struct.unpack("b", tele[5:6])[0]

	sUnfilteredThrottle = struct.unpack("B", tele[6:7])[0]
	sUnfilteredBrake = struct.unpack("B", tele[7:8])[0]
	sUnfilteredSteering = struct.unpack("b", tele[8:9])[0]
	sUnfilteredClutch = struct.unpack("B", tele[9:10])[0]
	sRaceStateFlags = struct.unpack("B", tele[10:11])[0]

	sLapsInEvent = struct.unpack("B", tele[11:12])[0]

	sBestLapTime = struct.unpack("f", tele[12:16])[0]
	sLastLapTime = struct.unpack("f", tele[16:20])[0]
	sCurrentTime = struct.unpack("f", tele[20:24])[0]
	sSplitTimeAhead = struct.unpack("f", tele[24:28])[0]
	sSplitTimeBehind = struct.unpack("f", tele[28:32])[0]
	sSplitTime = struct.unpack("f", tele[32:36])[0]
	sEventTimeRemaining = struct.unpack("f", tele[36:40])[0]
	sPersonalFastestLapTime = struct.unpack("f", tele[40:44])[0]
	sWorldFastestLapTime = struct.unpack("f", tele[44:48])[0]
	sCurrentSector1Time = struct.unpack("f", tele[48:52])[0]
	sCurrentSector2Time = struct.unpack("f", tele[52:56])[0]
	sCurrentSector3Time = struct.unpack("f", tele[56:60])[0]
	sFastestSector1Time = struct.unpack("f", tele[60:64])[0]
	sFastestSector2Time = struct.unpack("f", tele[64:68])[0]
	sFastestSector3Time = struct.unpack("f", tele[68:72])[0]
	sPersonalFastestSector1Time = struct.unpack("f", tele[72:76])[0]
	sPersonalFastestSector2Time = struct.unpack("f", tele[76:80])[0]
	sPersonalFastestSector3Time = struct.unpack("f", tele[80:84])[0]
	sWorldFastestSector1Time = struct.unpack("f", tele[84:88])[0]
	sWorldFastestSector2Time = struct.unpack("f", tele[88:92])[0]
	sWorldFastestSector3Time = struct.unpack("f", tele[92:96])[0]

	sJoyPad = struct.unpack("H", tele[96:98])[0]

	sHighestFlag = struct.unpack("B", tele[98:99])[0]

	sPitModeSchedule = struct.unpack("B", tele[99:100])[0]

	sOilTempCelsius = struct.unpack("h", tele[100:102])[0]
	sOilPressureKPa = struct.unpack("H", tele[102:104])[0]
	sWaterTempCelsius = struct.unpack("h", tele[104:106])[0]
	sWaterPressureKpa = struct.unpack("H", tele[106:108])[0]
	sFuelPressureKpa = struct.unpack("H", tele[108:110])[0]
	sCarFlags = struct.unpack("B", tele[110:111])[0]
	sFuelCapacity = struct.unpack("B", tele[111:112])[0]
	sBrake = struct.unpack("B", tele[112:113])[0]
	sThrottle = struct.unpack("B", tele[113:114])[0]
	sClutch = struct.unpack("B", tele[114:115])[0]
	sSteering = struct.unpack("b", tele[115:116])[0]
	sFuelLevel = struct.unpack("f", tele[116:120])[0]
	sSpeed = struct.unpack("f", tele[120:124])[0]
	sRpm = struct.unpack("H", tele[124:126])[0]
	sMaxRpm = struct.unpack("H", tele[126:128])[0]
	sGearNumGears = struct.unpack("B", tele[128:129])[0]
	sBoostAmount = struct.unpack("B", tele[129:130])[0]
	sEnforcedPitStopLap = struct.unpack("b", tele[130:131])[0]
	sCrashState = struct.unpack("B", tele[131:132])[0]

	sOdometerKM = struct.unpack("f", tele[132:136])[0]
	sOrientation0 = struct.unpack("f", tele[136:140])[0]
	sOrientation1 = struct.unpack("f", tele[140:144])[0]
	sOrientation2 = struct.unpack("f", tele[144:148])[0]
	sLocalVelocity0 = struct.unpack("f", tele[148:152])[0]
	sLocalVelocity1 = struct.unpack("f", tele[152:156])[0]
	sLocalVelocity2 = struct.unpack("f", tele[156:160])[0]
	sWorldVelocity0 = struct.unpack("f", tele[160:164])[0]
	sWorldVelocity1 = struct.unpack("f", tele[164:168])[0]
	sWorldVelocity2 = struct.unpack("f", tele[168:172])[0]
	sAngularVelocity0 = struct.unpack("f", tele[172:176])[0]
	sAngularVelocity1 = struct.unpack("f", tele[176:180])[0]
	sAngularVelocity2 = struct.unpack("f", tele[180:184])[0]
	sLocalAcceleration0 = struct.unpack("f", tele[184:188])[0]
	sLocalAcceleration1 = struct.unpack("f", tele[188:192])[0]
	sLocalAcceleration2 = struct.unpack("f", tele[192:196])[0]
	sWorldAcceleration0 = struct.unpack("f", tele[196:200])[0]
	sWorldAcceleration1 = struct.unpack("f", tele[200:204])[0]
	sWorldAcceleration2 = struct.unpack("f", tele[204:208])[0]
	sExtentsCentre0 = struct.unpack("f", tele[208:212])[0]
	sExtentsCentre1 = struct.unpack("f", tele[212:216])[0]
	sExtentsCentre2 = struct.unpack("f", tele[216:220])[0]

	sTyreFlag0 = struct.unpack("B", tele[220:221])[0]
	sTyreFlag1 = struct.unpack("B", tele[221:222])[0]
	sTyreFlag2 = struct.unpack("B", tele[222:223])[0]
	sTyreFlag3 = struct.unpack("B", tele[223:224])[0]
	sTerrain0 = struct.unpack("B", tele[224:225])[0]
	sTerrain1 = struct.unpack("B", tele[225:226])[0]
	sTerrain2 = struct.unpack("B", tele[226:227])[0]
	sTerrain3 = struct.unpack("B", tele[227:228])[0]
	sTyreY0 = struct.unpack("f", tele[228:232])[0]
	sTyreY1 = struct.unpack("f", tele[232:236])[0]
	sTyreY2 = struct.unpack("f", tele[236:240])[0]
	sTyreY3 = struct.unpack("f", tele[240:244])[0]
	sTyreRPS0 = struct.unpack("f", tele[244:248])[0]
	sTyreRPS1 = struct.unpack("f", tele[248:252])[0]
	sTyreRPS2 = struct.unpack("f", tele[252:256])[0]
	sTyreRPS3 = struct.unpack("f", tele[256:260])[0]
	sTyreSlipSpeed0 = struct.unpack("f", tele[260:264])[0]
	sTyreSlipSpeed1 = struct.unpack("f", tele[264:268])[0]
	sTyreSlipSpeed2 = struct.unpack("f", tele[268:272])[0]
	sTyreSlipSpeed3 = struct.unpack("f", tele[272:276])[0]
	sTyreTemp0 = struct.unpack("B", tele[276:277])[0]
	sTyreTemp1 = struct.unpack("B", tele[277:278])[0]
	sTyreTemp2 = struct.unpack("B", tele[278:279])[0]
	sTyreTemp3 = struct.unpack("B", tele[279:280])[0]
	sTyreGrip0 = struct.unpack("B", tele[280:281])[0]
	sTyreGrip1 = struct.unpack("B", tele[281:282])[0]
	sTyreGrip2 = struct.unpack("B", tele[282:283])[0]
	sTyreGrip3 = struct.unpack("B", tele[283:284])[0]
	sTyreHeightAboveGround0 = struct.unpack("f", tele[284:288])[0]
	sTyreHeightAboveGround1 = struct.unpack("f", tele[288:292])[0]
	sTyreHeightAboveGround2 = struct.unpack("f", tele[292:296])[0]
	sTyreHeightAboveGround3 = struct.unpack("f", tele[296:300])[0]
	sTyreLateralStiffness0 = struct.unpack("f", tele[300:304])[0]
	sTyreLateralStiffness1 = struct.unpack("f", tele[304:308])[0]
	sTyreLateralStiffness2 = struct.unpack("f", tele[308:312])[0]
	sTyreLateralStiffness3 = struct.unpack("f", tele[312:316])[0]
	sTyreWear0 = struct.unpack("B", tele[316:317])[0]
	sTyreWear1 = struct.unpack("B", tele[317:318])[0]
	sTyreWear2 = struct.unpack("B", tele[318:319])[0]
	sTyreWear3 = struct.unpack("B", tele[319:320])[0]
	sBrakeDamage0  = struct.unpack("B", tele[320:321])[0]
	sBrakeDamage1 = struct.unpack("B", tele[321:322])[0]
	sBrakeDamage2 = struct.unpack("B", tele[322:323])[0]
	sBrakeDamage3 = struct.unpack("B", tele[323:324])[0]
	sSuspensionDamage0 = struct.unpack("B", tele[324:325])[0]
	sSuspensionDamage1 = struct.unpack("B", tele[325:326])[0]
	sSuspensionDamage2 = struct.unpack("B", tele[326:327])[0]
	sSuspensionDamage3 = struct.unpack("B", tele[327:328])[0]
	sBrakeTempCelsius0 = struct.unpack("h", tele[328:330])[0]
	sBrakeTempCelsius1 = struct.unpack("h", tele[330:332])[0]
	sBrakeTempCelsius2 = struct.unpack("h", tele[332:334])[0]
	sBrakeTempCelsius3 = struct.unpack("h", tele[334:336])[0]
	sTyreTreadTemp0 = struct.unpack("H", tele[336:338])[0]
	sTyreTreadTemp1 = struct.unpack("H", tele[338:340])[0]
	sTyreTreadTemp2 = struct.unpack("H", tele[340:342])[0]
	sTyreTreadTemp3 = struct.unpack("H", tele[342:344])[0]
	sTyreLayerTemp0 = struct.unpack("H", tele[344:346])[0]
	sTyreLayerTemp1 = struct.unpack("H", tele[346:348])[0]
	sTyreLayerTemp2 = struct.unpack("H", tele[348:350])[0]
	sTyreLayerTemp3 = struct.unpack("H", tele[350:352])[0]
	sTyreCarcassTemp0 = struct.unpack("H", tele[352:354])[0]
	sTyreCarcassTemp1 = struct.unpack("H", tele[354:356])[0]
	sTyreCarcassTemp2 = struct.unpack("H", tele[356:358])[0]
	sTyreCarcassTemp3 = struct.unpack("H", tele[358:360])[0]
	sTyreRimTemp0 = struct.unpack("H", tele[360:362])[0]
	sTyreRimTemp1 = struct.unpack("H", tele[362:364])[0]
	sTyreRimTemp2 = struct.unpack("H", tele[364:366])[0]
	sTyreRimTemp3 = struct.unpack("H", tele[366:368])[0]
	sTyreInternalAirTemp0 = struct.unpack("H", tele[368:370])[0]
	sTyreInternalAirTemp1 = struct.unpack("H", tele[370:372])[0]
	sTyreInternalAirTemp2 = struct.unpack("H", tele[372:374])[0]
	sTyreInternalAirTemp3 = struct.unpack("H", tele[374:376])[0]
	sWheelLocalPositionY0 = struct.unpack("f", tele[376:380])[0]
	sWheelLocalPositionY1 = struct.unpack("f", tele[380:384])[0]
	sWheelLocalPositionY2 = struct.unpack("f", tele[384:388])[0]
	sWheelLocalPositionY3 = struct.unpack("f", tele[388:392])[0]
	sRideHeight0 = struct.unpack("f", tele[392:396])[0]
	sRideHeight1 = struct.unpack("f", tele[396:400])[0]
	sRideHeight2 = struct.unpack("f", tele[400:404])[0]
	sRideHeight3 = struct.unpack("f", tele[404:408])[0]
	sSuspensionTravel0 = struct.unpack("f", tele[408:412])[0]
	sSuspensionTravel1 = struct.unpack("f", tele[412:416])[0]
	sSuspensionTravel2 = struct.unpack("f", tele[416:420])[0]
	sSuspensionTravel3 = struct.unpack("f", tele[420:424])[0]
	sSuspensionVelocity0 = struct.unpack("f", tele[424:428])[0]
	sSuspensionVelocity1 = struct.unpack("f", tele[428:432])[0]
	sSuspensionVelocity2 = struct.unpack("f", tele[432:436])[0]
	sSuspensionVelocity3 = struct.unpack("f", tele[436:440])[0]
	sAirPressure0 = struct.unpack("H", tele[440:442])[0]
	sAirPressure1 = struct.unpack("H", tele[442:444])[0]
	sAirPressure2 = struct.unpack("H", tele[444:446])[0]
	sAirPressure3 = struct.unpack("H", tele[446:448])[0]

	sEngineSpeed = struct.unpack("f", tele[448:452])[0]
	sEngineTorque = struct.unpack("f", tele[452:456])[0]

	sAeroDamage = struct.unpack("B", tele[456:457])[0]
	sEngineDamage = struct.unpack("B", tele[457:458])[0]

	sAmbientTemperature = struct.unpack("b", tele[458:459])[0]
	sTrackTemperature = struct.unpack("b", tele[459:460])[0]
	sRainDensity = struct.unpack("B", tele[460:461])[0]
	sWindSpeed = struct.unpack("b", tele[461:462])[0]
	sWindDirectionX = struct.unpack("b", tele[462:463])[0]
	sWindDirectionY = struct.unpack("b", tele[463:464])[0]

	sParticipantInfo = list()
	for participant in range(56):
		offset = participant*16+464
		pTele = tele[offset:offset+16]

		sWorldPosition0 = struct.unpack("h", pTele[0:2])[0]
		sWorldPosition1 = struct.unpack("h", pTele[2:4])[0]
		sWorldPosition2 = struct.unpack("h", pTele[4:6])[0]
		sCurrentLapDistance = struct.unpack("H", pTele[6:8])[0]
		sRacePosition = struct.unpack("B", pTele[8:9])[0]
		sLapsCompleted = struct.unpack("B", pTele[9:10])[0]
		sCurrentLap = struct.unpack("B", pTele[10:11])[0]
		sSector = struct.unpack("B", pTele[11:12])[0]
		sLastSectorTime = struct.unpack("f", pTele[12:16])[0]

		sParticipantInfo.append((sWorldPosition0, sWorldPosition1, sWorldPosition2, sCurrentLapDistance, sRacePosition, sLapsCompleted, sCurrentLap, sSector, sLastSectorTime))

	sTrackLength = struct.unpack("f", tele[1360:1364])[0]
	sWings0 = struct.unpack("B", tele[1364:1365])[0]
	sWings1 = struct.unpack("B", tele[1365:1366])[0]
	sDPad = struct.unpack("B", tele[1366:1368])[0]

	telemetryData.append((sBuildVersionNumber, sPacketType,
		sGameSessionState,
		sViewedParticipantIndex, sNumParticipants,
		sUnfilteredThrottle, sUnfilteredBrake, sUnfilteredSteering, sUnfilteredClutch, sRaceStateFlags,
		sLapsInEvent, 
		sBestLapTime, sLastLapTime, sCurrentTime, sSplitTimeAhead, sSplitTimeBehind, sSplitTime, sEventTimeRemaining, sPersonalFastestLapTime, sWorldFastestLapTime, sCurrentSector1Time, sCurrentSector2Time, sCurrentSector3Time, sFastestSector1Time, sFastestSector2Time, sFastestSector3Time, sPersonalFastestSector1Time, sPersonalFastestSector2Time, sPersonalFastestSector3Time, sWorldFastestSector1Time, sWorldFastestSector2Time, sWorldFastestSector3Time,
		sJoyPad,
		sHighestFlag,
		sPitModeSchedule,
		sOilTempCelsius, sOilPressureKPa, sWaterTempCelsius, sWaterPressureKpa, sFuelPressureKpa, sCarFlags, sFuelCapacity, sBrake, sThrottle, sClutch, sSteering, sFuelLevel, sSpeed, sRpm, sMaxRpm, sGearNumGears, sBoostAmount, sEnforcedPitStopLap, sCrashState,
		sOdometerKM, sOrientation0, sOrientation1, sOrientation2, sLocalVelocity0, sLocalVelocity1, sLocalVelocity2, sWorldVelocity0, sWorldVelocity1, sWorldVelocity2, sAngularVelocity0, sAngularVelocity1, sAngularVelocity2, sLocalAcceleration0, sLocalAcceleration1, sLocalAcceleration2, sWorldAcceleration0, sWorldAcceleration1, sWorldAcceleration2, sExtentsCentre0, sExtentsCentre1, sExtentsCentre2,
		sTyreFlag0, sTyreFlag1, sTyreFlag2, sTyreFlag3, sTerrain0, sTerrain1, sTerrain2, sTerrain3, sTyreY0, sTyreY1, sTyreY2, sTyreY3, sTyreRPS0, sTyreRPS1, sTyreRPS2, sTyreRPS3, sTyreSlipSpeed0, sTyreSlipSpeed1, sTyreSlipSpeed2, sTyreSlipSpeed3, sTyreTemp0, sTyreTemp1, sTyreTemp2, sTyreTemp3, sTyreGrip0, sTyreGrip1, sTyreGrip2, sTyreGrip3, sTyreHeightAboveGround0, sTyreHeightAboveGround1, sTyreHeightAboveGround2, sTyreHeightAboveGround3, sTyreLateralStiffness0, sTyreLateralStiffness1, sTyreLateralStiffness2, sTyreLateralStiffness3, sTyreWear0, sTyreWear1, sTyreWear2, sTyreWear3, sBrakeDamage0, sBrakeDamage1, sBrakeDamage2, sBrakeDamage3, sSuspensionDamage0, sSuspensionDamage1, sSuspensionDamage2, sSuspensionDamage3, sBrakeTempCelsius0, sBrakeTempCelsius1, sBrakeTempCelsius2, sBrakeTempCelsius3, sTyreTreadTemp0, sTyreTreadTemp1, sTyreTreadTemp2, sTyreTreadTemp3, sTyreLayerTemp0, sTyreLayerTemp1, sTyreLayerTemp2, sTyreLayerTemp3, sTyreCarcassTemp0, sTyreCarcassTemp1, sTyreCarcassTemp2, sTyreCarcassTemp3, sTyreRimTemp0, sTyreRimTemp1, sTyreRimTemp2, sTyreRimTemp3, sTyreInternalAirTemp0, sTyreInternalAirTemp1, sTyreInternalAirTemp2, sTyreInternalAirTemp3, sWheelLocalPositionY0, sWheelLocalPositionY1, sWheelLocalPositionY2, sWheelLocalPositionY3, sRideHeight0, sRideHeight1, sRideHeight2, sRideHeight3, sSuspensionTravel0, sSuspensionTravel1, sSuspensionTravel2, sSuspensionTravel3, sSuspensionVelocity0, sSuspensionVelocity1, sSuspensionVelocity2, sSuspensionVelocity3, sAirPressure0, sAirPressure1, sAirPressure2, sAirPressure3,
		sEngineSpeed, sEngineTorque,
		sAeroDamage, sEngineDamage,
		sAmbientTemperature, sTrackTemperature, sRainDensity, sWindSpeed, sWindDirectionX, sWindDirectionY,
		sParticipantInfo,
		sTrackLength, sWings0, sWings1, sDPad))

	
	# Participant infor starts at 464.
	#base = tele[464:464+16]
	#datapoint = (binascii.hexlify(base[0:2]), binascii.hexlify(base[2:4]), binascii.hexlify(base[4:6]), binascii.hexlify(base[6:8]), binascii.hexlify(base[8:9]), binascii.hexlify(base[9:10]), binascii.hexlify(base[10:11]), binascii.hexlify(base[11:14]), binascii.hexlify(base[14:16]))
	#datapoint = (struct.unpack('4s', binascii.hexlify(base[0:2]))[0], struct.unpack('4s', binascii.hexlify(base[4:6]))[0])
	#datapoint = (struct.unpack('h', base[0:2])[0], struct.unpack('h', base[2:4])[0], struct.unpack('h', base[4:6])[0], binascii.hexlify(base[6:8]))
	
	#participant.append(datapoint)
	#base = tele[464:]
	#datapoint = list()
	#for i in range(56):
		#offset = 16*i
		#datapoint.append(binascii.hexlify(base[offset+8:offset+9]))

	#participant.append(datapoint)

#with open('party.csv', 'w') as f:
	#for l in participant: f.write(",".join(str(x) for x in l)+"\n")

with open('tele.csv', 'w') as f:
	for p in telemetryData:
		for x in p:
			if isinstance(x, list):
				for y in x:
					#f.write(",".join(str(binascii.hexlify(z)) for z in y)+",")
					f.write(",".join(str(z) for z in y)+",")
			else:
				#f.write(str(binascii.hexlify(x))+",")
				f.write(str(x)+",")
		f.write("\n")
