#!/usr/bin/env python
import cv2
import urllib2
import numpy as np
import sys
import time
import RPi.GPIO as GPIO
import signal
import atexit
import time, threading
from socket import *

flag_x = 0
flag_y = 0

def loop_fuc():
	#time.sleep(10)
	global flag_x
	global flag_y
	#print ('thread %s is running...',cnt)
	#print ('%s', cnt)
	#print ('thread  ended.')
	HOST = '127.0.0.1'
    PORT = 9999

    s = socket(AF_INET,SOCK_DGRAM)
    s.bind((HOST,PORT))
    print '...waiting for message..'
    while True:
        data,address = s.recvfrom(1024)

        if(data == 'right')
            flag_x = 1
        elif(data == 'left')
            flag_x = -1
        elif(data == 'up')
            flag_y = 1
        elif(data == 'down')
            flag_y = -1
        print data
        print flag_x
        print flag_y
    #s.sendto('this is the UDP server',address)
    s.close()


X=640
Y=320
b0=90
d0=90
freq = 5
c=1
pox=320
poy=240
trackflag = 1

t = threading.Thread(target=loop_fuc, name='LoopThread')
t.start()

atexit.register(GPIO.cleanup)
servopin=21
GPIO.setmode(GPIO.BCM)
GPIO.setup(servopin,GPIO.OUT,initial=False)
p=GPIO.PWM(servopin,50)
p.start(0)
time.sleep(2)
pin=20
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin,GPIO.OUT,initial=False)
q=GPIO.PWM(pin,50)
q.start(0)
time.sleep(2)
def mov(paim,qaim):
        global b0
        global d0
        if paim<b0:
                pa=-10
        else:
                pa=10
        if qaim<d0:
                qa=-10
        else:
                qa=10
        for i in range(b0,int(paim),pa):
                p.ChangeDutyCycle(4+0.4*10*i/180)
                time.sleep(0.2)
                p.ChangeDutyCycle(0)
                time.sleep(0.2)
        for i in range(d0,int(qaim),qa):
                q.ChangeDutyCycle(4+0.4*10*i/180)
                time.sleep(0.2)
                q.ChangeDutyCycle(0)
                time.sleep(0.2)
        b0=int(paim)
        d0=int(qaim)
def gery(x,y,flag):
         sheer = 0
         upper = 0
         if(flag==0):
                print "Steering gear not tracking!"
         else:
                if(x<0 or  x>X or  y<0 or  y>Y ):
                        print "Unable to track for data error!"
                else :
                        if(x<=(X/2)):
                                if(y<=(Y/2) or ):
                                        sheer = 40
                                        upper = -40
                                        mov(120+sheer,150+upper)
                                else:

                                        sheer = 40
                                        upper = 40
                                        mov(120+sheer,150+upper)
                        else:
                                if(y<=(Y/2)):
                                        sheer = -40
                                        upper = -40
                                        mov(120+sheer,150+upper)
                                else:
                                        sheer = -40
                                        upper = 40
                                        mov(120+sheer,150+upper)

face_cascade = cv2.CascadeClassifier('haar-frontface.xml')
#nose_cascade = cv2.CascadeClassifier('haarcascade_mcs_nose.xml')
face_cascade.load('/home/pi/cascades/haar-frontface.xml')
#nose_cascade.load('/home/pi/cascades/haarcascade_mcs_nose.xml')
host = "192.168.1.100:8080"
if len(sys.argv)>1:
    host = sys.argv[1]
hoststr = 'http://' + host + '/?action=stream'
print 'Streaming ' + hoststr

print 'Print Esc to quit'
stream=urllib2.urlopen(hoststr)
bytes=''
while True:
    bytes += stream.read(1024)
    a = bytes.find('\xff\xd8')
    b = bytes.find('\xff\xd9')

    if a!=-1 and b!=-1:

        jpg = bytes[a:b+2]
        bytes= bytes[b+2:]
        i = cv2.imdecode(np.fromstring(jpg, dtype=np.uint8),flags=1)
        gray = cv2.cvtColor(i, cv2.COLOR_BGR2GRAY)
        #cv2.imshow("gray", gray)
        if c % freq == 0:

            localtime = time.asctime( time.localtime(time.time()) )#ticks = time.time()
            print(localtime)
            faces = face_cascade.detectMultiScale(gray, 1.5, 5)
#            noses = nose_cascade.detectMultiScale(gray, 1.1, 5)
            detectflag = 0
            for (x, y, w, h) in faces:
                i = cv2.rectangle(i, (x, y), (x + w, y + h), (0, 255, 0), 2)
                detectflag = 1
                #            roi_gray = gray[y:y+h, x:x+w]
                #for (ex, ey, ew, eh) in noses:
                    #cv2.rectangle(i, (ex, ey), (ex + ew, ey + eh), (255, 255, 0), 2)
                    #detectflag = 2
            if detectflag == 2:
                print("Target position: (%d, %d)" % (x + w / 2, y + h / 2))
                pox = x + w / 2
                poy = y + h / 2
            elif detectflag == 1:
                print("potential target at:(%d, %d)" % (x + w / 2, y + h / 2))
                pox = x + w / 2
                poy = y + h / 2
            else:
                print("Searching target")

        # print i.shape
        #cv2.imshow("xiaorun",i)
        c+=1
        gery(pox,poy,trackflag)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            exit(0)
                                            
