#!/bin/sh
URL=google.com
PNGROOT=/srv/www/speed
PNGFILE=`date +"%d%m%y%k%M"`
RRDFILE=/tmp/curspeed.rrd
RRDTOTAL=/tmp/totalspeed.rrd

/home/user/work/scripts-git/curlstat.py $URL $PNGROOT/$PNGFILE.png $RRDFILE $RRDTOTAL
