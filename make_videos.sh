#!/bin/bash
#USAGE:
#find -L "`pwd`" -maxdepth 2 -regextype posix-extended -iregex >>>REGEX HERE<<< -exec ./make_videos.sh {} \;

for f in $@
do
	#SNAME=$(sed -r 's/.*(race[[:digit:]]+.*).*\.json/\1/g' <<< "$f")
    SNAME=$(sed -r 's/.*\/(.*).json/\1/g' <<< "$f")
	screen -dmS $SNAME python3 ReplayEnhancer.py $f
done
