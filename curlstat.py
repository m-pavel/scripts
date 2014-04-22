#!/usr/bin/env python
import urllib2, sys, time
import rrdtool
import sys

url = sys.argv[1]
output = sys.argv[2] if len(sys.argv) >= 3 else "default.png"
rrd_file = "/tmp/spped.rrd"
 
def chunk_report(bytes_so_far, chunk_size, total_size, time_start, time_prev, time_curr):
    percent = float(bytes_so_far) / total_size
    percent = round(percent*100, 2)
    av_speed = float(bytes_so_far) / 1024 / (time_curr - time_start)
    react_speed = chunk_size / 1024 / (time_curr - time_prev)
    print '{0} and {1} and {2}'.format(av_speed, react_speed, percent)
#    rrdtool.update(rrd_file, 'N:%s:%s:%s:%s' % (av_speed, react_speed, percent, bytes_so_far))
    rrdtool.update(rrd_file, 'N:%s:%s' % (av_speed, bytes_so_far))

def chunk_read(response, chunk_size=8192, report_hook=None):
    total_size = response.info().getheader('Content-Length').strip()
    total_size = int(total_size)
    bytes_so_far = 0
    starttime = time.time()
    chunktime = starttime
    while True:
	prevchunktime = chunktime
	chunk = response.read(chunk_size)
	chunktime = time.time()
	bytes_so_far += len(chunk)
	if not chunk:
	    break
	if report_hook:
	    report_hook(bytes_so_far, chunk_size, total_size, starttime, prevchunktime, chunktime)

    return bytes_so_far

if __name__ == '__main__':

    data_sources=[  'DS:speed_av:GAUGE:10:U:U',
#		    'DS:speed_react:GAUGE:10:U:U',
#		    'DS:percent:GAUGE:10:U:U',
		    'DS:amount:COUNTER:10:U:U',
		    'RRA:AVERAGE:0.5:10:1000' ,
		    'RRA:AVERAGE:0.5:5:1000' ,
		    'RRA:AVERAGE:0.5:1:1000',
		    'RRA:LAST:0.5:2:1000']
    rrdstart = int(time.time()) 
    rrdtool.create(rrd_file, '--step', '1', '--start', str(rrdstart), data_sources)
    response = urllib2.urlopen(url);
    chunk_read(response, 2048, report_hook=chunk_report)
    rrdend = int(time.time())
    print (rrdend - rrdstart)
    ret = rrdtool.graph( output, "--start", str(rrdstart-10) , "--end", str(rrdend+10),
"--vertical-label=KB/s",
'--watermark=stat',
"-w 800",
"DEF:m1_num="+rrd_file+":speed_av:AVERAGE",
"DEF:m2_num="+rrd_file+":amount:AVERAGE",
"DEF:m3_num="+rrd_file+":speed_av:LAST",
#"LINE1:m1_num#0000FF:speed_av\\r",
"LINE2:m2_num#00FF00:amount\\r",
#"LINE3:m3_num#FF0000:last\\r",
#"GPRINT:m1_num:AVERAGE:Avg speed\: %6.0lf ",
#"GPRINT:m1_num:MAX:Max speed\: %6.0lf \\r")
"GPRINT:m3_num:AVERAGE:Avg\: %6.0lf ",
"GPRINT:m3_num:MAX:Max\: %6.0lf \\r")

print ret