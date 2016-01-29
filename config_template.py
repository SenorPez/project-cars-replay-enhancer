'''
Module-specific variables should go here.
'''
#make_title
#make_standings
#make_timer
#make_results
#make_series_standings

from PIL import ImageFont
font = ImageFont.truetype("./demo/Roboto-Regular.ttf", 15)
headingfont = ImageFont.truetype("./demo/Roboto-Medium.ttf", 20)
headingcolor = (255, 0, 0)

#make_title
#make_results
#make_series_standings

backdrop = "./demo/Ruapuna.jpg"
logo = "./demo/Ruapuna.png"
serieslogo = "./demo/Ruapuna.png"
logo_height = 150
logo_width = 150

showChampion = False

headingtext = "Ruapuna Scion Spectacular"
subheadingtext = "Ruapuna Club"

margin = 20
columnMargin = 10

'''
These variables can be set by the create_config script.
'''
sourcevideo = "./demo/demo.mp4"
sourcetelemetry = "demo/demotelemetry/"
outputvideo = "./demo/demo-output.mp4"

carData = ["Scion FR-S" for x in range(21)]
teamData = [None for x in range(21)]
pointStructure = [0, 15, 12, 10, 8, 6, 4, 2, 1, 0, 0, 0, 0]
points = [0 for x in range(21)]

'''
These variables can be set by the create_video script.
'''

threshold = 1
gaptime = 1
skipstart = 0
skipend = 0
cachefile = './demo/file.cache'

'''
These variables can be set by the create_racestart script.
'''

racestart = 3.5+0.8

'''
These variables should not be edited.
'''

participantData = list()
telemetryData = list()
configVersion = 2

sectorBests = [-1, -1, -1]
personalBests = [[-1, -1, -1] for x in range(64)]
bestLap = -1
personalBestLaps = [-1 for x in range(64)]
elapsedTimes = [-1 for x in range(64)]
