import json
import sys

config1 = json.load(open(sys.argv[1]))
config2 = json.load(open(sys.argv[2]))

expected_diffs = {
    'output_video',
    'source_telemetry',
    'source_video',
    'subheading_text',
    'sync_racestart',
    'video_skipend',
    'video_skipstart'}

expected_participant_diffs = {
    'points'}

for key in sorted(config1.keys() | config2.keys()):
    try:
        if key == 'participant_config' and config1[key] != config2[key]:
            participant_config1 = config1[key]
            participant_config2 = config2[key]

            common_drivers = sorted(participant_config1.keys() & participant_config2.keys())
            missing_drivers = sorted(participant_config1.keys() ^ participant_config2.keys())

            for driver in common_drivers:
                for driver_key in participant_config1[driver].keys():
                    if participant_config1[driver][driver_key] != participant_config2[driver][driver_key]:
                        if driver_key in expected_participant_diffs:
                            print("  ->EDIFF: {} {}".format(driver, driver_key))
                        else:
                            print("--->DIFF : {} {}".format(driver, driver_key))

            for driver in missing_drivers:
                print("--->NODRV: {}".format(driver))
                
        elif config1[key] == config2[key]:
            print("    EQUAL: {}".format(key))
        else:
            if key in expected_diffs:
                print("  ->EDIFF: {}".format(key))
            else:
                print("--->DIFF : {}".format(key))
    except KeyError:
        print("--->NOKEY: {}".format(key))
