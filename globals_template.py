from PIL import ImageFont

sourcevideo = "./assets/race1.mp4"
sourcetelemetry = "./assets/race1/"
outputvideo = "./outputs/race1.mp4"

backdrop = "./assets/Glencairn.jpg"
logo = "./assets/GlencairnLogo.png"
logo_height = 150
logo_width = 150

racestart = 3.5+0.8

font = ImageFont.truetype("/usr/share/fonts/truetype/Roboto/Roboto-Regular.ttf", 15)
headingfont = ImageFont.truetype("/usr/share/fonts/truetype/Roboto/Roboto-Medium.ttf", 20)

margin = 20
columnMargin = 10

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
cachefile = './assets/file.cache'

#Best sectors and laps.
sectorBests = [-1, -1, -1]
personalBests = [[-1, -1, -1] for x in range(64)]
bestLap = -1
personalBestLaps = [-1 for x in range(64)]

elapsedTimes = [-1 for x in range(64)]

pointStructure = [5, 15, 12, 10, 8, 6, 4, 2, 1, 0, 0, 0, 0]
points = [x for x in range(12)]
