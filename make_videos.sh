#!/bin/bash
for f in $@
do
	SNAME=$(sed -r 's/.*(race[[:digit:]]+.*).*\.json/\1/g' <<< "$f")
	screen -dmS $SNAME python3 ReplayEnhancer.py $f
done
