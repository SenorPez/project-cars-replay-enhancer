# project-cars-replay-enhancer
Project CARS Replay Enhancer: Combines telemetry data with replay video to improve Project CARS replays.

Current release: 0.2.1 
Current edge state: Rough  
Current mood: Nervous  

The Project CARS Replay Enhancer (I'd call it PCRE, [but that's taken](http://www.pcre.org/ "PCRE")) is designed to augment Project CARS replays by combining captured telemetry data with replay video. The current state of the project is quite rough, so a bit of programming and troubleshooting knowledge is required.

The scripts are currently not fast enough for live broadcasting.

## Requirements
* [Python 3.4](https://www.python.org/download/releases/3.4.0/ "Python 3.4.0") or greater
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
* At the end of the race, do not click **Continue** or stop telemetry capture until this **Race Time** numbers post. (Make sure you scroll down to see the later cars!) Despite you being on the results screen, the remaining cars will finish their lap and this is captured by the telemetry.
* Each collection of telemetry packet captures should only contain a single race. Restarting, if that is allowed, is allowed. The parser automatically detects the latest complete (start->finish) race in each collection; if multiple complete races are included in the telemetry, only the last one will be used. (Opened issue #12 to consider removing this limitation.)
    
###Video Capture:
There is no video capture functionality included in the scripts. How you get the video to your local machine is left as an exercise for the reader. For my PS4, I stream the replay to YouTube which then archives it and then can be downloaded using [youtube-dl](https://rg3.github.io/youtube-dl/ "youtube-dl"). Video capture devices such as an Elgato work just fine as well (probably better, actually).
    
See the configuration file for some details on when the video should stop and start, and how to sync the video to the telemetry.
    
###Replay Enhancement:
To run the replay enhancer, run the `replay.py` script with a configuration file.  
Usage is `python replay.py <configfile>;`
    
####Config File:
A sample configuration file is included in the repository as `globals_template.py`. This contains values that are passed between the various scripts. All values must be included; there are no defaults. Additional values can be added as needed.
      
`sourcevideo`: Path to the source video.  
`sourcetelemetry`: Path to the directory of captured telemetry data. Make sure to include the trailing slash!
`outputvideo`: Path to the desired output video. Images are be output using this file name with a .jpg extension.
      
`racestart`: This is used to synchronize the telemetry data with the video. This is the number of seconds between the start of the replay video (after blackframe detection, see below) and the green flag dropping.  
In testing, this number always seems to be **close to** but not exactly 3.5 seconds. One method to find this value is to use the default 3.5 and note how much it needs to be adjusted based on the difference on the timer between 0.00 and the displayed time on a new lap.
      
`font`, `headingfont`: Pillow ImageFont objects defining fonts. These names (font, headingfont) are used by display modules.  
Add new values as needed by new display modules.
      
`margin`: Margin value used by display modules.  
Add new values as needed by new display modules.
      
`headingtext`, `subheadingtext`: Text used by display modules.  
Add new values as needed by new display modules.
      
`carData`, `teamData`: Python lists that map cars and teams to participants, based on their index.  
There is a utility script (`show_participants.py`) that dumps participant name and indexes for ease of creating these lists.
      
> **NOTE:** Due to UDP packet limitations, these aren't included in the data. I typically use a race-ending screenshot to save this data, and manually enter it.
      
`participantData`, `telemetryData`: Empty lists used by the scripts to build information.
      
`threshold`: Used for blackframe detection.  
If the average brightness of a frame is below this, it's considered a blackframe. Default is 1.

> **NOTE:** You generally want the replay controls panel closed. If you want it open, you might have to adjust threshold up.

`gaptime`: Used for blackframe gaps to determine "scenes".  
Blackframes closer than this gaptime (default 1 second) are considered to be a part of the same fade.
      
`skipstart`: Number of "scenes" at the start of the video to skip, not including the first scene. See below.
`skipend`: Number of "scenes" at the end of the video to skip, not including the last scene. See below.
        
Project CARS replays use a fade-through-black when the camera angle changes. This divides the replay into a series of "scenes". In a "perfect" replay, you'd start at perfect black, show the race action, and end at perfect black.

In the real world, this is impossible.

What we do, then, is detect the blackframes that define scenes, and use that to define the extent of our desired replay.
          
> **EXAMPLE:** Our video shows the "replay loading" screen, fades to black, then begins the race. At the end of the race, it fades to black, and restarts the replay, but ends before another fade. In this case, `skipstart` and `skipend` are both 0, as the first and last scenes are automatically* skipped.

> * This is mostly for sanity, due to how Project CARS shows its replays. If you really want those, you can set `skipstart` and `skipend` to -1.

> **EXAMPLE:** Our video shows the "replay loading" screen, fades to black, then begins the race. However, we were drunk, and forgot to stop the replay, however, so it showed a total of 8 scenes (each separated by a fade-through-black) at the end before we stopped it. In this case, `skipstart` is 0 and `skipend` would be 8.
          
Note that if you wanted to, you could use this to create replays of single laps. The telemetry data syncs, but data from before the video start (previous laps, for example) is not available.

`cachefile`: Blackframe detection is **HORRIBLY SLOW**. As a result, once we find the extents of our desired video, we cache it into this file.

> **NOTE:** If you later change something, such as your `skipstart` or `skipend` parameters, you **NEED TO REMOVE** the entry in the cache file. (Or just delete the entire cache.) Since it's **HORRIBLY SLOW**, if the file is seen in the cache data, we just use that cache data.
        
####Output Selection:
Output selection is currently super-hacky. See the bottom of `replay.py` for a few options, and comment and uncomment lines to create what you want. This is definitely something that should be added as an option instead by whatever.
      
####Display Modules:
The various modules add the replay data to the video and are modular in nature. There are a few included right now:
* `make_results`: Creates a results screen.
* `make_series_standings`: Creates a series standing screen.
* `make_standings`: Creates a standings tree during the race.
* `make_timer`: Creates a laptime and lap counter during the race.
* `make_title`: Creates a title screen.
        
Each callable function in the modules can take no arguments; a `t` value, indicating the current video time, is automatically passed by MoviePy. The above modules all include a "base" function (which returns the graphic) and a "mask" version of the function (which returns the alpha values for the graphic).
      
For information on compositing the video and the module output, see the MoviePy documentation, and the compositing sections in `replay.py`
      
##Enhancing the Enhancer?
You're more than welcome to do so! Write new modules, speed up new modules, feel free. If you have any issues or questions please communicate them here!
