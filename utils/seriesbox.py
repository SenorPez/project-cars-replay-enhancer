import sys

from tqdm import tqdm

from replayenhancer.RaceData import RaceData

point_structure = [0, 25, 18, 15, 12 ,10, 8, 6, 4, 2, 1]
drivers = dict()

for telemetry in sys.argv[1:]:
    data = RaceData(telemetry)
    with tqdm(desc="Processing {}".format(telemetry)) as progress:
        while True:
            try:
                _ = data.get_data()
                progress.update()
            except StopIteration:
                break

    for entry in data.classification:
        driver_name = entry.driver_name
        position = entry.position
        best_lap = entry.best_lap

        if driver_name not in drivers:
            drivers[driver_name] = 0

        try:
            if point_structure[0] and best_lap == min([entry.best_lap for entry in data.classification if entry.best_lap is not None]):
                drivers[driver_name] += point_structure[0]
            drivers[driver_name] += point_structure[position]
        except IndexError:
            pass

    output = sorted(
        [(driver, points) for driver, points in drivers.items()],
        key=lambda x: -x[1])

    longest_name = max([len(driver) for driver, _ in output])

    for line in output:
        print('{:{width}} {:4d}'.format(*line, width=longest_name))
