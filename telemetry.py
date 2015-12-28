import binascii
import glob
import natsort
import string
import struct
import sys

if len(sys.argv) == 1:
	print "Usage: 'python "+sys.argv[0]+" <packetdirectory>'";

else:
	data = list()
	for a in natsort.natsorted(glob.glob('./'+sys.argv[1]+'pdata*')):
		with open(a, 'rb') as f:
			data.append(f.read())

	telemetryData = list()

	for tele in data:
		if len(tele) == 1367:
			packString  = "HB"
			packString += "B"
			packString += "bb"
			packString += "BBbBB"
			packString += "B"
			packString += "21f"
			packString += "H"
			packString += "B"
			packString += "B"
			packString += "hHhHHBBBBBbffHHBBbB"
			packString += "22f"
			packString += "8B12f8B8f12B4h20H16f4H"
			packString += "2f"
			packString += "2B"
			packString += "bbBbbb"

			for participant in range(56):
				packString += "hhhHBBBBf"
			
			packString += "fBBB"

		elif len(tele) == 1028:
			packString  = "HBB"

			for participant in range(16):
				packString += "64s"

		elif len(tele) == 1347:
			packString  = "HB64s64s64s64s64s"

			for participant in range(16):
				packString += "64s"

		telemetryData.append(struct.unpack(packString, tele))

	with open('./'+sys.argv[1]+'tele.csv', 'w') as f:
		for p in telemetryData:
			f.write(",".join(string.strip(str(x), '\x00') for x in p)+"\n")
