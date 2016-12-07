import sys

from ReplayEnhancer import ReplayEnhancer


def update_drivers(replay, car_class):
    classification = replay.race_data.class_classification(car_class)

    for data in classification:
        try:
            drivers[data[1]].append(drivers[data[1]][-1]+data[-2])
        except KeyError:
            drivers[data[1]] = [data[-2]]

races = sys.argv[1:]
drivers = dict()

for race in races:
    replay = ReplayEnhancer(race)

    if len(replay.car_classes):
        [
            update_drivers(replay, car_class)
            for car_class in replay.car_classes
        ]
    else:
        update_drivers(replay, None)

print(sorted(drivers.items()))
