from glob import glob
from natsort import natsorted
from struct import unpack

def process_telemetry(folder):
	with open(folder+'tele.csv', 'w') as csvfile:
		for a in natsorted(glob(folder+'pdata*')):
			with open(a, 'rb') as packFile:
				packData = packFile.read()
				if len(packData) == 1367:
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

				elif len(packData) == 1028:
					packString  = "HBB"

					for participant in range(16):
						packString += "64s"

				elif len(packData) == 1347:
					packString  = "HB64s64s64s64s"

					for participant in range(16):
						packString += "64s"

					packString += "64x"

				unpackData = unpack(packString, packData)
				csvfile.write(",".join(str(x, encoding='utf-8').replace('\x00', '') if isinstance(x, bytes) else str(x).replace('\x00', '') for x in unpack(packString, packData)+(a,))+"\n")
