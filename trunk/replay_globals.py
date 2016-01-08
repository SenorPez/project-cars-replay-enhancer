from PIL import ImageFont

racestart = 3.5

font = ImageFont.truetype("/usr/share/fonts/truetype/Roboto/Roboto-Regular.ttf", 15)
headingfont = ImageFont.truetype("/usr/share/fonts/truetype/Roboto/Roboto-Medium.ttf", 20)

margin = 20

headingtext = "Kart One UK Nationals"
subheadingtext = "Round 1 of 3 - Glencairn East"
carData = ["125cc Shifter Kart" for x in range(12)]
teamData = ["Dark NiTRO" for x in range(12)]

participantData = list()
telemetryData = list()
