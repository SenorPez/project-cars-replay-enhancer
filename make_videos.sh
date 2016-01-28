#!/bin/bash
for f in $@
do
	SNAME=$(sed -r 's/.*(race[[:digit:]]+.*)_.*/\1/g' <<< "$f")
	screen -dmS $SNAME python3 replay.py $f
done
