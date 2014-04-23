#!/bin/sh

PNGROOT=/srv/www/speed
PNGFILE=`date +"%d%m%y"`
RRDTOTAL=/tmp/totalspeed.rrd

rrdtool graph $PNGROOT/$PNGFILE.png --vertical-label='KB/s' -w 800 --start -1d \
    DEF:m1_num=$RRDTOTAL:speed_av:AVERAGE \
    LINE1:m1_num#0000FF:"speed_av" \
    VDEF:m1min=m1_num,MINIMUM \
    VDEF:m1max=m1_num,MAXIMUM \
    VDEF:m1avg=m1_num,AVERAGE \
    GPRINT:m1min:"%6.2lf" \
    GPRINT:m1max:"%6.2lf"  \
    GPRINT:m1avg:"%6.2lf \\r"

