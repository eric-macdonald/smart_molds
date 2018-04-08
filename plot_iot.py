#!/Users/eric.w.macdonald/miniconda2/bin/python
import numpy as np
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
import sys
import math

start = int(sys.argv[2])
starte = int(sys.argv[3])
locator = int(sys.argv[4])

temperature = []
humidity = []
pressure = []
mag1 = []
mag2 = []
mag3 = []
mag4 = []
acc1 = []
acc2 = []
acc3 = []
gyro1 = []
gyro2 = []
gyro3 = []

print "file name" + str(sys.argv[1])
short_name = sys.argv[1]
print "start " + str(start)
print "starte" + str(starte) 

file = open(sys.argv[1], 'r') 
bob1 = 0
bob2 = 0
for line in file:
    line = line.split()
    if(len(line)> 2):
        if(line[1]=="TMP"):
            time1 = datetime.datetime.strptime(line[0], '%Y-%m-%dT%H:%M:%S.%f')
            temp = line[2].split("d")
            temperature.append([time1, temp[0]])
        if(line[1]=="PRES"):
            time1 = datetime.datetime.strptime(line[0], '%Y-%m-%dT%H:%M:%S.%f')
            pres = line[2].split("P")
            pres = float(pres[0])/100
            pressure.append([time1, pres])
        if(line[1]=="HUM"):
            time1 = datetime.datetime.strptime(line[0], '%Y-%m-%dT%H:%M:%S.%f')
            humd = line[2].split("%")
            humidity.append([time1, humd[0]])
        if(line[1]=="MAG"):
            time1 = datetime.datetime.strptime(line[0], '%Y-%m-%dT%H:%M:%S.%f')
            if (bob1 == 0):
                mag = line[2].split("u")
                magx = mag[0] 
            else:
                mag = line[2].split("u")
                magx = mag[0]
#                magx = 0.01 * float(mag[0]) + 0.99 * float(magx) 
            mag1.append([time1, magx ])
            if (bob1 == 0):
                mag = line[3].split("u")
                magy = mag[0] 
            else:
                mag = line[3].split("u")
                magy = mag[0]
#                magy = 0.01 * float(mag[0]) + 0.99 * float(magy) 
            mag2.append([time1, magy ])
            if (bob1 == 0):
                mag = line[4].split("u")
                magz = mag[0] 
            else:
                mag = line[4].split("u")
                magz = mag[0]
#                magz = 0.01 * float(mag[0]) + 0.99 * float(magz) 
            mag3.append([time1, magz])
#            mag4.append([time1, math.sqrt(float(magz)**2 + float(magy)**2 + float(magx)**2)])
            bob1 = bob1 + 1

        if(line[1]=="ACC"):
            time1 = datetime.datetime.strptime(line[0], '%Y-%m-%dT%H:%M:%S.%f')
            acc = line[2].split("g")
            acc1.append([time1, acc[0]])
            acc = line[3].split("g")
            acc2.append([time1, acc[0]])
            acc = line[4].split("g")
            acc3.append([time1, acc[0]])
        if(line[1]=="GYR"):
            time1 = datetime.datetime.strptime(line[0], '%Y-%m-%dT%H:%M:%S.%f')
            if (bob2 == 0):
                gyro = line[2].split("d")
                gyrox = gyro[0] 
            else:
                gyro = line[2].split("d")
                gyro = line[2].split("d")
                gyrox = 0.01 * float(gyro[0]) + 0.99 * float(gyrox) 
            gyro1.append([time1, gyrox])
            if (bob2 == 0):
                gyro = line[3].split("d")
                gyroy = gyro[0] 
            else:
                gyro = line[3].split("d")
                gyroy = 0.01 * float(gyro[0]) + 0.99 * float(gyroy) 
            gyro2.append([time1, gyroy])
            if (bob2 == 0):
                gyro = line[4].split("d")
                gyroz = gyro[0] 
            else:
                gyro = line[4].split("d")
                gyroz = 0.01 * float(gyro[0]) + 0.99 * float(gyroz) 
            gyro3.append([time1, gyroz])
            bob2 = bob2 + 1

time1, magx = zip(*mag1)
time2, magy = zip(*mag2)
time3, magz = zip(*mag3)

for idx, val in enumerate(magx):
    mag4.append([time1[idx], math.sqrt(float(magz[idx])**2 + float(magy[idx])**2 + float(magx[idx])**2)])

time4, magt = zip(*mag4)

b, a = butter(3, 0.05)
magx = list(magx)
magx2 = [float(i) for i in magx]
magx3=np.asarray(magx2, dtype=float) 
magy = list(magy)
magy2 = [float(i) for i in magy]
magy3=np.asarray(magy2, dtype=float) 
magz = list(magz)
magz2 = [float(i) for i in magz]
magz3=np.asarray(magz2, dtype=float) 

magt = list(magz)
magt2 = [float(i) for i in magz]
magt3=np.asarray(magt2, dtype=float) 

magx4 = filtfilt(b, a, magx3)
magy4 = filtfilt(b, a, magy3)
magz4 = filtfilt(b, a, magz3)
magt4 = filtfilt(b, a, magt3)

fig, ax = plt.subplots()
axes = [ax, ax.twinx(), ax.twinx()]
fig.subplots_adjust(right=0.75)
axes[-1].spines['right'].set_position(('axes', 1.2))

axes[0].plot_date(time1[start:], magz4[start:],'g-')
axes[0].set_xlabel('time (hours:minutes:seconds)')
axes[0].set_ylabel('Magnetic Flux X Axis (uT)', color='g')
axes[0].tick_params('y', colors='g')

axes[1].plot_date(time2[start:], magy4[start:],'b-')
axes[1].set_ylabel('Magnetic Flux Y Axis (uT)', color='b')
axes[1].tick_params('y', colors='b')

axes[2].plot_date(time3[start:], magx4[start:],'r-')
axes[2].set_ylabel('Magnetic Flux Z Axis (uT)', color='r')
axes[2].tick_params('y', colors='r')

fig.autofmt_xdate()
xfmt = mdates.DateFormatter('%H:%M:%S')
axes[-1].xaxis.set_major_formatter(xfmt)
axes[-1].xaxis.set_major_locator(mdates.SecondLocator(interval=locator))
plt.show()

fig, ax = plt.subplots()
ax.plot_date(time1[start:], magt4[start:],'g-')
ax.set_xlabel('time (hour:minutes:seconds)')
ax.set_ylabel('Magnetic Flux Magnitude (uT)', color='g')
fig.autofmt_xdate()
xfmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=locator))
plt.show()

mag4_name = short_name + "magT.csv"
with open(mag4_name,'w') as f:
    f.writelines(["%s\n" % item for item in magt4])
    f.close()
print "end"

time10, gyr1 = zip(*gyro1)
time11, gyr2 = zip(*gyro2)
time12, gyr3 = zip(*gyro3)

fig, ax = plt.subplots()
axes = [ax, ax.twinx(), ax.twinx()]
fig.subplots_adjust(right=0.75)
axes[-1].spines['right'].set_position(('axes', 1.2))

axes[0].plot_date(time11[start:], gyr1[start:],'g-')
axes[0].set_xlabel('time (hour:minutes:seconds)')
axes[0].set_ylabel('Rotation - X Axis (degrees)', color='g')
axes[0].tick_params('y', colors='g')

axes[1].plot_date(time11[start:], gyr2[start:],'b-')
axes[1].set_ylabel('Rotation - Y Axis (degrees)', color='b')
axes[1].tick_params('y', colors='b')

axes[2].plot_date(time12[start:], gyr3[start:],'r-')
axes[2].set_ylabel('Rotation - Z Axis (degrees)', color='r')
axes[2].tick_params('y', colors='r')

fig.autofmt_xdate()
xfmt = mdates.DateFormatter('%H:%M:%S')
axes[-1].xaxis.set_major_formatter(xfmt)
axes[-1].xaxis.set_major_locator(mdates.SecondLocator(interval=locator))
plt.show()

gyro1_name = short_name + "gyro1.csv"

with open(gyro1_name,'w') as f:
    f.writelines(["%s\n" % item  for item in gyro1])
    f.close()

gyro2_name = short_name + "gyro2.csv"
with open(gyro2_name,'w') as f:
    f.writelines(["%s\n" % item  for item in gyro2])
    f.close()

gyro3_name = short_name + "gyro3.csv"
with open(gyro3_name,'w') as f:
    f.writelines(["%s\n" % item  for item in gyro3])
    f.close()


time20, ac1 = zip(*acc1)
time21, ac2 = zip(*acc2)
time22, ac3 = zip(*acc3)

fig, ax = plt.subplots()

ax.plot_date(time20[start:], ac1[start:],'g-', label="Z Axis")
ax.plot_date(time21[start:], ac2[start:],'b-', label="Y Axis")
ax.plot_date(time22[start:], ac3[start:],'r-', label="X Axis")
ax.set_xlabel('time (hour:minutes:seconds)')
ax.set_ylabel('Acceleration (g)', color='g') 

legend = ax.legend(loc='upper left', shadow=True)
frame = legend.get_frame()
frame.set_facecolor('0.90')

fig.autofmt_xdate()
xfmt = mdates.DateFormatter('%H:%M:%S')
ax.xaxis.set_major_formatter(xfmt)
ax.xaxis.set_major_locator(mdates.SecondLocator(interval=locator))
plt.show()


time4, temper = zip(*temperature)
time5, humid = zip(*humidity)
time6, press = zip(*pressure)

b, a = butter(3, 0.05)
temper = list(temper)
temper2 = [float(i) for i in temper]
temper3=np.asarray(temper2, dtype=float)
humid = list(humid)
humid2 = [float(i) for i in humid]
humid3=np.asarray(humid2, dtype=float)
press = list(press)
press2 = [float(i) for i in press]
press3=np.asarray(press2, dtype=float)


temper4 = filtfilt(b, a, temper3)
humid4 = filtfilt(b, a, humid3)
press4 = filtfilt(b, a, press3)

fig, ax = plt.subplots()
axes = [ax, ax.twinx(), ax.twinx()]
fig.subplots_adjust(right=0.75)
axes[-1].spines['right'].set_position(('axes', 1.2))

axes[0].plot_date(time4[starte:], temper4[starte:],'g-')
axes[0].set_xlabel('time (hour:minute:seconds)')
axes[0].set_ylabel('Temperature', color='g')
axes[0].tick_params('y', colors='g')

axes[1].plot_date(time5[starte:], humid4[starte:],'b-')
axes[1].set_ylabel('Humidity', color='b')
axes[1].tick_params('y', colors='b')

axes[2].plot_date(time6[starte:], press4[starte:],'r-')
axes[2].set_ylabel('Pressure (kPa)', color='r')
axes[2].tick_params('y', colors='r')

fig.autofmt_xdate()
xfmt = mdates.DateFormatter('%H:%M:%S')
axes[-1].xaxis.set_major_formatter(xfmt)
axes[-1].xaxis.set_major_locator(mdates.SecondLocator(interval=locator))
plt.show()


temp_name = short_name + "temp.csv"
with open(temp_name,'w') as f:
    f.writelines(["%s\n" % item  for item in temperature])
    f.close()

humid_name = short_name + "humid.csv"
with open(humid_name,'w') as f:
    f.writelines(["%s\n" % item  for item in humidity])
    f.close()

press_name = short_name + "press.csv"
with open(press_name,'w') as f:
    f.writelines(["%s\n" % item  for item in pressure])
    f.close()
