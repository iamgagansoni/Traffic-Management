#here we are synchronising timing of greenlight on the basis of number of vehicles
import cv2
import time
import numpy as np
import Car_Detection.car_detection as det 
import os
def dete():
    car,truck,bicycle,bus,motorbike,vehicle=det.detect()
    #print(car,truck,bicycle,bus,motorbike)
    carw,bicyclew=5,5             #Adding Weights for each vehicle type
    truckw=8
    busw=10
    motorbikew=4
    li=[car,truck,bicycle,bus,motorbike]
    li1=[carw,truckw,bicyclew,busw,motorbikew]
    os.system('cls')
    print("Total Vehicle Detected",vehicle)
    return li,li1


def greensig(li,li1,j,route):
    timer=0
    for i in range(len(li)):
        if i==0 or i==2 or i==4:                    #Setting timer for green Light
            timer+=li[i]*li1[i]
            timer//=1.5
        else:
            timer+=li[i]*li1[i]
    timer=int(timer)
    if timer<10:
        timer=15
    while timer>=0:
        mins,secs=divmod(timer,60)
        t='{:02d}:{:02d}'.format(mins,secs)         
        print(t,end='\r')
        time.sleep(1)                                           #Timer Countdown
        timer-=1
        if timer == 10:
            try:
                print("Clicking picture of ",route[j+1])
                li,li1=dete()
                return li,li1
            except:
                pass
        

k=1

while k:
    route=["route_1","route_2","route_3","route_4"]
    for i in range(len(route)):
        if i==0:
            print("Clicking picture of ",route[i])
            li,li1=dete()
        li,li1=greensig(li,li1,i,route)                                                        #Function Calling
    k=int(input("Press 0 to exit \nPress 1 to continue\t"))