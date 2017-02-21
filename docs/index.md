## The Big Rewrite

After working on the Project CARS Replay Enhancer for almost 9 months, I came to the realization that I needed to rewrite it, almost from scratch, due to an enormous number of failings and dead-ends in the code. In the professional world, this is often referred to as "technical debt," wherein your deficiencies are made manifest.

I'm pretty sure this big rewrite, and the lack of updates while it happened, cost me most of my user base, which is a shame, because the end result is much better.

### Render Size Limitations

One of the first invitational events you might get invited to in a Project CARS career, DLC and success willing, is a three hour McLaren race at Zolder. I captured the telemetry from this race, resulting in almost a quarter-million packets being saved.

Pre-rewrite, I couldn't create this video, however. The memory requirements of doing so, because the architecture required loading the entire dataset into memory at once, could not be satisfied by the home server I used for rendering. I had to actually render it, to make sure it worked, on my gaming PC.

Post-rewrite, I can not only create this video on any machine, but it is no slower (on a per-frame basis, obviously, a three hour race takes longer to render than a three minute race) than any other dataset. The telemetry is streamed "as needed" to the video renderer, cutting the memory requirements down siginficantly.

Based on the new architecture, if you wanted to capture and render a 25 hour race, you could do so. You'd have well over 2 million packets captured, and on my machine it would take over 8 days to render, but it **could** be done.

### Performance Improvements

I stupidly do not have performance profiles from the pre-rewrite architecture. I created them, but didn't save them, because I'm an idiot. But one thing stood out: The video renderer (from the `moviepy` package) was waiting on the Replay Enhancer scripts each frame.

Post-rewrite, I have performance profiles. In every case, be it a three minute or three hour race, the video renderer is the bottleneck. Further performance improvements would have to go into the compositing routines used by the renderer.

### Greater Flexibility

Pre-rewrite, things were a mess. Configuration files were so deeply embedded in the architecture that errors or small changes could break numerous things. There was no way to see the data being created. Outputs were coming out of a wide array of spigots. When things went bad, it was almost impossible to figure out why.

Post-rewrite, everything is far more componentized. The core is actually `RaceData` which actually handles the telemetry data. Moving forward, I plan on moving into its own project, to function as a Python-based package to parse and analyze telemetry data. With the announcement that PCARS2 will support telemetry data, it'll be a good thing to have separate.

Beyond that, title cards are their own classes. The standings overlay are their own classes. The configuration data is just a dictionary of values. Unlike in the pre-rewrite world, you could actually SIMPLY, with a bit of Python code, create your own custom sequences. The main Replay Enhancer script just uses what I think is a sensible default from analyzing a configuration file.

### Show Something

Okay, fine, I'll show you some Python code that'll show you things I find amazingly... refreshing?... about the post-rewrite architecture.

#### Best Lap For Each Driver
```
>>> from replayenhancer.RaceData import RaceData 
>>> data = RaceData('assets/race67') # Open saved telemetry 
>>> while True: data.get_data() # Advance all the way through the data until race end.
>>> {name: driver.best_lap for name, driver in data.drivers.items()}
```

#### Create a simple Results Card
```
>>> from replayenhancer.RaceData import RaceData; from replayenhancer.DefaultCards import RaceResults; from PIL import Image
>>> data = RaceData('assets/race67')
>>> while True: _ = data.get_data()
>>> card = RaceResults(data.classification)
>>> Image.fromarray(card.to_frame()).save('ResultsCard.jpg')
```

### Create a Video of the Standings display for the first 30 seconds
```
>>> from replayenhancer.RaceData import RaceData; from replayenhancer.GTStandings import GTStandings; import moviepy.editor as mpy
>>> data = RaceData('assets/race67')
>>> standings = GTStandings(data, ups=30)
>>> clip = mpy.VideoClip(standings.make_frame, duration=30)
>>> clip.write_videofile('outputs/out.mp4', fps=30)
```
