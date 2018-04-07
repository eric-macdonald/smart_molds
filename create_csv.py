#!/Users/eric.w.macdonald/miniconda2/bin/python
import numpy as np
from scipy.signal import lfilter, lfilter_zi, filtfilt, butter
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as ticker
import datetime
import sys
import math

#start = 9000
#starte = 2200
#start = int(sys.argv[2])
#starte = int(sys.argv[3])
#locator = int(sys.argv[4])
#locator = 0.0002 
#locatore = 0.00008 

temperature = []
humidity = []
pressure = []
mag1 = []
mag2 = []
mag3 = []
mag4 = []
mag5x = []
mag5y = []
mag5z = []
mag5 = []
acc1 = []
acc2 = []
acc3 = []
gyro1 = []
gyro2 = []
gyro3 = []

#print "file name" + str(sys.argv[1])
short_name = sys.argv[1]
#print "start " + str(start)
#print "starte" + str(starte) 

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
            mag1.append([time1, magx ])
            if (bob1 == 0):
                mag = line[3].split("u")
                magy = mag[0] 
            else:
                mag = line[3].split("u")
                magy = mag[0]
            mag2.append([time1, magy ])
            if (bob1 == 0):
                mag = line[4].split("u")
                magz = mag[0] 
            else:
                mag = line[4].split("u")
                magz = mag[0]
            mag3.append([time1, magz])
            mag4.append([time1, math.sqrt(float(magz)**2 + float(magy)**2 + float(magx)**2)])
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

for idx, val in enumerate(magx):
    mag5x.append([time1[idx], magx4[idx]])
    mag5y.append([time1[idx], magy4[idx]])
    mag5z.append([time1[idx], magz4[idx]])
    mag5.append([time1[idx], magt4[idx]])

time4, magt = zip(*mag4)

mag5x_name = short_name + "_Xmagt.csv"
mag5y_name = short_name + "_Ymagt.csv"
mag5z_name = short_name + "_Zmagt.csv"
mag5_name = short_name + "_magt.csv"
for idx, val in enumerate(magx):
    mag5x.append([time1[idx], magx4[idx]])
    mag5y.append([time1[idx], magy4[idx]])
    mag5z.append([time1[idx], magz4[idx]])
with open(mag5x_name,'w') as f:
    f.writelines(["%s\n" % item for item in mag5x])
    f.close()
with open(mag5y_name,'w') as f:
    f.writelines(["%s\n" % item for item in mag5y])
    f.close()
with open(mag5z_name,'w') as f:
    f.writelines(["%s\n" % item for item in mag5z])
    f.close()
with open(mag5_name,'w') as f:
    f.writelines(["%s\n" % item for item in mag5])
    f.close()
 

print "printing acc with length"
print len(acc1)
#time20, ac1 = zip(*acc1)
#time21, ac2 = zip(*acc2)
#time22, ac3 = zip(*acc3)

accx_name = short_name + "_accx.csv"
with open(accx_name,'w') as f:
    f.writelines(["%s\n" % item  for item in acc1])
    f.close()

accy_name = short_name + "_accy.csv"
with open(accy_name,'w') as f:
    f.writelines(["%s\n" % item  for item in acc2])
    f.close()

accz_name = short_name + "_accz.csv"
with open(accz_name,'w') as f:
    f.writelines(["%s\n" % item  for item in acc3])
    f.close()

time10, gyr1 = zip(*gyro1)
time11, gyr2 = zip(*gyro2)
time12, gyr3 = zip(*gyro3)

gyro1_name = short_name + "gyro1.csv"
gyro2_name = short_name + "gyro2.csv"
gyro3_name = short_name + "gyro3.csv"

with open(gyro1_name,'w') as f:
    f.writelines(["%s\n" % item  for item in gyro1])
    f.close()

with open(gyro2_name,'w') as f:
    f.writelines(["%s\n" % item  for item in gyro2])
    f.close()

with open(gyro3_name,'w') as f:
    f.writelines(["%s\n" % item  for item in gyro3])
    f.close()

time4, temper = zip(*temperature)
time5, humid = zip(*humidity)
time6, press = zip(*pressure)

temp_name = short_name + "_temp.csv"
with open(temp_name,'w') as f:
    f.writelines(["%s\n" % item  for item in temperature])
    f.close()

humid_name = short_name + "_humid.csv"
with open(humid_name,'w') as f:
    f.writelines(["%s\n" % item  for item in humidity])
    f.close()

press_name = short_name + "_press.csv"
with open(press_name,'w') as f:
    f.writelines(["%s\n" % item  for item in pressure])
    f.close()
