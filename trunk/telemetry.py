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

	telemetryData.append(struct.unpack(packString, tele))

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
