from PIL import ImageFont

sourcevideo = "./demo/demo.mp4"
sourcetelemetry = "demo/demotelemetry/"
outputvideo = "./demo/demo-output.mp4"

backdrop = "./demo/Ruapuna.jpg"
logo = "./demo/Ruapuna.png"
logo_height = 150
logo_width = 150

racestart = 3.5+0.8

font = ImageFont.truetype("./demo/Roboto-Regular.ttf", 15)
headingfont = ImageFont.truetype("./demo/Roboto-Medium.ttf", 20)

margin = 20
columnMargin = 10

headingtext = "Ruapuna Scion Spectacular"
subheadingtext = "Ruapuna Club"
carData = ["Scion FR-S" for x in range(21)]
teamData = [None for x in range(21)]

participantData = list()
telemetryData = list()

#Video analysis variables
threshold = 1
gaptime = 1
skipstart = 0
skipend = 0
cachefile = './demo/file.cache'

#Best sectors and laps.
sectorBests = [-1, -1, -1]
personalBests = [[-1, -1, -1] for x in range(64)]
bestLap = -1
personalBestLaps = [-1 for x in range(64)]

elapsedTimes = [-1 for x in range(64)]

pointStructure = [0, 15, 12, 10, 8, 6, 4, 2, 1, 0, 0, 0, 0]
points = [0 for x in range(21)]
