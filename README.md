# Project CARS Replay Enhancer [![Build Status](https://travis-ci.org/SenorPez/project-cars-replay-enhancer.svg?branch=0.5-devel)](https://travis-ci.org/SenorPez/project-cars-replay-enhancer) [![codecov](https://codecov.io/gh/SenorPez/project-cars-replay-enhancer/branch/0.5-devel/graph/badge.svg)](https://codecov.io/gh/SenorPez/project-cars-replay-enhancer)

Combines telemetry data with replay video to improve Project CARS replays.

Current release: 0.6  
Current edge state: Close to Smooth  
Current mood: Excited

The Project CARS Replay Enhancer (I'd call it PCRE, [but that's taken](http://www.pcre.org/ "PCRE")) is intended to augment Project CARS replays by combining captured telemetry data with replay video. The project is currently in a rough state, being rewritten from the ground-up to be more stable, better tested, and faster.

The scripts are currently not fast enough for live broadcasting.

## Requirements
* [Python 3.3](https://www.python.org/download/releases/3.3.0/ "Python 3.3.0") or greater
* [moviepy](http://zulko.github.io/moviepy/ "moviepy")
* [natsort](https://pypi.python.org/pypi/natsort "natsort")
* [Pillow](https://pypi.python.org/pypi/Pillow "Pillow")
* [tqdm](https://pypi.python.org/pypi/tqdm "tqdm")

##Installation
### Short Version:
The Project CARS Replay Enhancer can be installed with `pip`: `pip install replayenhancer`.

### Longer Version:
Depending on your environment:
* You may need to use `sudo` or `sudo -H` to install the packages. For example: `sudo -H pip install replayenhancer`.
* You may need to explicitly call pip using your python installation. For example: `python -m pip install replayenhancer` or `python3 -m pip install replayenhancer`.
* You may need to manually install dependencies for some of the packages required by the replayenhancer. The following packages are required:
    * GCC (`gcc`)
    * Python development libraries (`python35-devel` or similar)
    * ZLIB development libraries (`zlib-devel` or similar)
    * JPEG development libraries (`libjpeg-turbo-devel` or similar)
    
For a complete list of commands to get the Project CARS Replay Enhancer running from a newly-created [Amazon EC2 Instance](https://aws.amazon.com/ec2/), see [Commands From Scratch](https://github.com/SenorPez/project-cars-replay-enhancer/wiki/Commands-From-Scratch).

## Usage
### Telemetry Capture:
Telemetry packet capture is performed by running the command `packetcapture` on the network. This captures UDP packets broadcast by Project CARS (make sure you've enabled UDP broadcast) and store them to a subdirectory for future processing.

> **NOTE:** As most internet video runs at 30 frames per second, you want to set your UDP broadcast rate to at least 30 packets per second, otherwise there may be noticeable "phasing" between video and data displays.

#### Telemetry Capture Best Practices:
There are a few things to do to optimize the telemetry data used by the Project CARS Replay Enhancer.

* Telemetry capture should be started before entering the race. The preferred time for this would be at the menu before clicking the **Drive** button on the menu.
* At the end of the race, do not click **Continue** or stop telemetry capture until all the **Race Time** numbers post. (Make sure you scroll down to see the later cars!) Despite you being on the results screen, the remaining cars will finish their lap and this is captured by the telemetry.
* Each collection of telemetry packet captures should only contain a single race. Restarting, if that is allowed, is allowed. The parser automatically detects the latest complete (start->finish) race in each collection; if multiple complete races are included in the telemetry, only the last one will be used.
    
### Video Capture:
There is no video capture functionality included in the scripts. How you get the video to your local machine is left as an exercise for the reader. For my PS4, I stream the replay to YouTube which then archives it and then can be downloaded using [youtube-dl](https://rg3.github.io/youtube-dl/ "youtube-dl"). Video capture devices such as an Elgato work just fine as well (probably better, actually).
    
### Configuration Files:
Project CARS Replay Enhancer configuration files are JSON files, and can be created by using the [Project CARS Replay Enhancer UI](https://github.com/SenorPez/project-cars-replay-enhancer-ui) or by creating them by hand. See [Configuration File Format](https://github.com/SenorPez/project-cars-replay-enhancer/wiki/Configuration-File-Format) for details on recognized fields.

### Telemetry Synchronization:
For best results, the telemetry data feed must be synchronized to the video feed; there is no way to automatically perform this. To aid with this synchronization, run the Project CARS Replay Enhancer is the `-s` option and the desired configuration file. For example, `replayenhancer -s config.json`.

A low-quality video that encompasses only the first lap of the race is created, along with a timer overlay. To determine the telemetry synchronization, compare the time on this overlay with the lap time of a car as it crosses the start-finish line. These two times should be identical; if they are not, the syncronization needs to be adjusted.
* If the value on the timer is greater than the lap time (this is the typical scenario), add the difference between the timer and the lap time to the telemetry synchronization value.
* If the value on the timer is less than the lap time, subtract the difference between the timer and the lap time from the telemetry synchronization value.
After adjusting the telemetry synchronization, another low-quality, shortened video is created to confirm the synchronization.

For an illustrated tutorial of telemetry synchronization, see [Determining Telemetry Synchronization Value](https://github.com/SenorPez/project-cars-replay-enhancer/wiki/Determining-Telemetry-Synchronization-Value).

### Creating a Replay
To create the full, enhanced replay, provide the Project Cars Replay Enhancer with a valid configuration file. For example, `replayenhancer config.json`.
      
## Enhancing the Enhancer?
You're more than welcome to do so! Write new modules, speed up new modules, feel free. If you have any issues or questions please communicate them here! I'm always looking for help.
