from PIL import ImageFont

sourcevideo = "race1.mp4"
sourcetelemetry = "./race1/"
outputvideo = "race1-output.mp4"

racestart = 3.5+0.8

font = ImageFont.truetype("/usr/share/fonts/truetype/Roboto/Roboto-Regular.ttf", 15)
headingfont = ImageFont.truetype("/usr/share/fonts/truetype/Roboto/Roboto-Medium.ttf", 20)

margin = 20

headingtext = "Kart One UK Nationals"
subheadingtext = "Round 1 of 3 - Sprint Race - Glencairn East"
carData = ["125cc Shifter Kart" for x in range(12)]
teamData = ["DarkNitro", "DarkNitro", "Rodrigues Racing", "Rodrigues Racing", "Greased Lightning", "Greased Lightning", "Galileo", "Galileo", "Barracuda", "Barracuda", "Victory Motorsports", "Victory Motorsports"]

participantData = list()
telemetryData = list()

#Video analysis variables
threshold = 1
gaptime = 1
skipstart = 0
skipend = 0
cachefile = 'file.cache'
