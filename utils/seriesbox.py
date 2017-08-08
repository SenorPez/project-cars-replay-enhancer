import sys

from tqdm import tqdm

from replayenhancer.RaceData import RaceData

point_structure = [0, 25, 18, 15, 12 ,10, 8, 6, 4, 2, 1]
#point_structure = [ 2, 34, 28, 25, 22, 20, 18, 16, 14, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1 ]
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
        key=lambda x: (-x[1], x[0]))

    longest_name = max([len(driver) for driver, _ in output])

    position = 0
    last_points = None;
    for (number, line) in enumerate(output, 1):
        if last_points is None or last_points != line[1]:
            position = number
        last_points = line[1]

        print('{:2d} {:2d} {:{width}} {:4d}'.format(number, position, *line, width=longest_name))
