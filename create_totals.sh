#!/bin/sh
rrdfile=$1
rrdtool create $rrdfile --step 1 \
        DS:speed_av:GAUGE:10:U:U	 \
	RRA:AVERAGE:0.5:10:1000 	\
	RRA:AVERAGE:0.5:5:1000 	\
	RRA:AVERAGE:0.5:1:1000 	\
	RRA:LAST:0.5:2:1000
