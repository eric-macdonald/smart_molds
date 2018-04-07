#!/Users/eric.w.macdonald/miniconda2/bin/python
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
import sys
import math

locator = 10 
mag4a = []
mag4b = []
mag4c = []
mag4d = []
mag4e = []
timea = datetime.datetime.now() - datetime.timedelta(100)
timeb = datetime.datetime.now() - datetime.timedelta(100)
timec = datetime.datetime.now() - datetime.timedelta(100)

file = open(sys.argv[1], 'r') 
for line in file:
    line = line.split(',')
    oldtimea = timea
    timea = datetime.datetime.strptime(line[0], '%Y-%m-%dT%H:%M:%S.%f')
    if(timea < oldtimea):
        print "backward time"
        print timea
        print oldtimea
    valuea = line[1].rstrip()
    valuea = float(valuea) 
    mag4a.append([timea,  valuea])

file = open(sys.argv[2], 'r') 
for line in file:
    line = line.split(',')
    timeb = datetime.datetime.strptime(line[0], '%Y-%m-%dT%H:%M:%S.%f')
    valueb = line[1].rstrip()
    valueb = float(valueb)
    mag4b.append([timeb,  valueb])

timea, valuea = zip(*mag4a)
timeb, valueb = zip(*mag4b)

fig, ax = plt.subplots()

ax.plot_date(timea, valuea,'g-', label="First Sensor (g)")
ax.plot_date(timeb, valueb,'b-', label="Second Sensor (g)")
#ax.plot_date(timed, valued,'m-', label="Sensor 5")
#ax.plot_date(timee, valuee,'y-', label="Sensor 6")
ax.set_xlabel('time (hour:minutes:seconds)')
ax.set_ylabel('Magnetic Magnitude (g)', color='g')

legend = ax.legend(loc='upper left', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.90')

fig.autofmt_xdate()
xfmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=locator))
plt.show()

fig, ax = plt.subplots()
axes = [ax, ax.twinx() ]
fig.subplots_adjust(right=0.75)

axes[0].plot_date(timea, valuea,'g-')
axes[0].set_xlabel('time (minutes:seconds)')
axes[0].set_ylabel('First Sensor (g)', color='g')
axes[0].tick_params('y', colors='g')
t1, t2 = axes[0].get_xlim()
#axes[0].set_xlim(736598.589500, 736598.591681)

axes[1].plot_date(timeb, valueb,'b-')
axes[1].set_ylabel('Second Sensor (g)', color='b')
axes[1].tick_params('y', colors='b')

#axes[3].plot_date(timed, valued,'m-')
#axes[3].set_ylabel('Magnetic sensor 4 (g)', color='m')
#axes[3].tick_params('y', colors='m')

#axes[4].plot_date(timee, valuee,'y-')
#axes[3].set_ylabel('Magnetic sensor 4 (g)', color='m')
#axes[4].tick_params('y', colors='y')

fig.autofmt_xdate()
xfmt = mdates.DateFormatter('%M:%S')
axes[-1].xaxis.set_major_formatter(xfmt)
axes[-1].xaxis.set_major_locator(mdates.SecondLocator(interval=locator))
plt.show()

