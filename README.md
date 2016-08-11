# Project CARS Replay Enhancer [![Build Status](https://travis-ci.org/SenorPez/project-cars-replay-enhancer.svg?branch=0.4-rewrite)](https://travis-ci.org/SenorPez/project-cars-replay-enhancer) [![codecov](https://codecov.io/gh/SenorPez/project-cars-replay-enhancer/branch/0.4-rewrite/graph/badge.svg)](https://codecov.io/gh/SenorPez/project-cars-replay-enhancer)

Combines telemetry data with replay video to improve Project CARS replays.

Current release: 0.4  
Current edge state: Very Rough  
Current mood: Frustrated  

The Project CARS Replay Enhancer (I'd call it PCRE, [but that's taken](http://www.pcre.org/ "PCRE")) is intended to augment Project CARS replays by combining captured telemetry data with replay video. The project is currently in a rough state, being rewritten from the ground-up to be more stable, better tested, and faster.

The scripts are currently not fast enough for live broadcasting.

## Requirements
* [Python 3.3](https://www.python.org/download/releases/3.4.0/ "Python 3.3.0") or greater
* [MoviePy](http://zulko.github.io/moviepy/ "MoviePy")
* [natsort](https://pypi.python.org/pypi/natsort "natsort")
* [NumPy](http://www.numpy.org/ "NumPy")
* [Pillow](https://pypi.python.org/pypi/Pillow "Pillow")

## Usage
###Telemetry Capture:
Telemetry packet capture is performed by running the `packetgrab.py` script on the network. This captures UDP packets broadcast by Project CARS (make sure you've enabled UDP broadcast) and store them to a subdirectory for future processing.

> **NOTE:** As most internet video runs at 30 frames per second, you want to set your UDP broadcast rate to at least 30 packets per second, otherwise there may be noticeable "phasing" between video and data displays.

####Telemetry Capture Best Practices:
There are a few things to do to optimize the telemetry data used by the Project CARS Replay Enhancer.

* Telemetry capture should be started before entering the race. The preferred time for this would be at the menu before clicking the **Drive** button on the menu.
* At the end of the race, do not click **Continue** or stop telemetry capture until all the **Race Time** numbers post. (Make sure you scroll down to see the later cars!) Despite you being on the results screen, the remaining cars will finish their lap and this is captured by the telemetry.
* Each collection of telemetry packet captures should only contain a single race. Restarting, if that is allowed, is allowed. The parser automatically detects the latest complete (start->finish) race in each collection; if multiple complete races are included in the telemetry, only the last one will be used.
    
###Video Capture:
There is no video capture functionality included in the scripts. How you get the video to your local machine is left as an exercise for the reader. For my PS4, I stream the replay to YouTube which then archives it and then can be downloaded using [youtube-dl](https://rg3.github.io/youtube-dl/ "youtube-dl"). Video capture devices such as an Elgato work just fine as well (probably better, actually).
    
###Getting Started:
> **NOTE:** Depending on your install environment, you may need to substitute `python3` for `python` in the following commands, to force usage of Python 3.3+. This is most typical on a Linux system, where Python 2.x is the default.

To create a new configuration file, run the Project CARS Replay Enhancer with no command line arguments: `python ReplayEnhancer.py`.

To edit an existing configuration file, or use an existing configuration file as the defaults for a new configuration file, run the Project CARS Replay Enhancer with the `-c` option and the name of the configuration file: `python ReplayEnhancer.py -c config_file.json`

Once the configuration file is completed, the Project CARS Replay Enhancer creates a low-quality, shortened video. This video can be used to confirm the title, results, standings, and--if enabled--champion screens, as well as the video trimming.

To adjust the video trimming, run the Project CARS Replay Enhancer with the `-t` option and the name of the configuration file: `python ReplayEnhancer.py -t config_file.json`. The trimming parameters are adjusted and another low-quality, shortened video is created to confirm the trimming.

> **NOTE:** If you have previously set a telemetry synchronization value (see below), it will be reset to 0.0 if either the detection parameters or start trimming parameters are changed.

To adjust the telemetry synchronization, run the Project CARS Replay Enhancer with the `-r` option and the name of the configuration file: `python ReplayEnhancer.py -r config_file.json`. To determine the telemetry synchronization value, view the time on the timer when the subject car crosses the start-finish line to begin Lap #2.
* If the timer shows Lap 2 has already begun, the telemetry needs to start later. Add the amount of time on the timer to the telemetry synchronization value. (This is the typical scenario.)
* If the timer shows Lap 1 is still in progress, the telemetry needs to start sooner. Subtract the difference between the time on the timer and the time of Lap 1 (obtainable from the standings display) from the telemetry synchronization value.
After adjusting the telemetry synchronization, another low-quality, shortened video is created to confirm the synchronization.

Once the configuration is complete, create the full-length, full-quality video by providing the Project CARS Replay Enhancer with the configuration file, and no options: `python ReplayEnhancer.py config_file.json`.
      
##Enhancing the Enhancer?
You're more than welcome to do so! Write new modules, speed up new modules, feel free. If you have any issues or questions please communicate them here! I'm always looking for help.
