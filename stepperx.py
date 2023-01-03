import RPi.GPIO as GPIO
import time
import tkinter as tk
from picamera import PiCamera
from time import sleep

#First Line
root=tk.Tk()
margin= 0.23
#Window Geometry
root.title("Stepper Motor User Interface")
root.geometry('600x400')
root.configure(bg="ghost white")

#X-Steps Widgets
xsteps_label=tk.Label(root,bg="ivory2", text="Number of Steps in x-direction: ")
xsteps_inp=tk.Entry(root)
xsteps_label.grid(row=0,column=0,padx=5,pady=5,sticky=tk.W)
xsteps_inp.grid(row=0,column=1,sticky=tk.E)

#Y-Steps Widgets
ysteps_label=tk.Label(root,bg="lavender blush", text="Number of Steps in y-direction: ")
ysteps_inp=tk.Entry(root)
ysteps_label.grid(row=1,column=0,sticky=tk.W)
ysteps_inp.grid(row=1,column=1,sticky=tk.E)

#Z-Steps Widgets
zsteps_label=tk.Label(root,bg="AntiqueWhite1", text="Number of Steps in z-direction: ")
zsteps_inp=tk.Entry(root)
zsteps_label.grid(row=2,column=0,sticky=tk.W)
zsteps_inp.grid(row=2,column=1,sticky=tk.E)

#Camera Setup
camera=PiCamera()

#GPIO Setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
axisx = [4,17,27,22]
axisy = [10,9,11,7]
axisz = [15,18,23,24]

for pin in axisx + axisy + axisz:
   GPIO.setup(pin,GPIO.OUT)
   GPIO.output(pin,0)

seq = [ [1,0,0,0],
        [1,1,0,0],
        [0,1,0,0],
        [0,1,1,0],
        [0,0,1,0],
        [0,0,1,1],
        [0,0,0,1],
        [1,0,0,1] ]

#LED Brightness
GPIO.setup(21,GPIO.OUT)
led=GPIO.PWM(21,1500)
led.start(0)

#Steps Button for x
def xenter_button():
    xsteps=int(xsteps_inp.get())
    if xsteps < 0:
        seq.reverse()
        for i in range(-xsteps):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(axisx[pin], seq[halfstep][pin])
                    time.sleep(0.001)
        seq.reverse()
    else:
        for i in range(xsteps):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(axisx[pin], seq[halfstep][pin])
                    time.sleep(0.001)
xstep_button=tk.Button(root, text="Enter Steps", command=xenter_button)
xstep_button.grid(row=0,column=2,padx=5,pady=5, sticky=tk.W)

#Steps Button for y
def yenter_button():
    ysteps=int(ysteps_inp.get())
    if ysteps < 0:
        seq.reverse()
        for i in range(-ysteps):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(axisy[pin], seq[halfstep][pin])
                    time.sleep(0.001)
        seq.reverse()
    else:
        for i in range(ysteps):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(axisy[pin], seq[halfstep][pin])
                    time.sleep(0.001)
ystep_button=tk.Button(root, text="Enter Steps", command=yenter_button)
ystep_button.grid(row=1,column=2,padx=5,pady=5, sticky=tk.W)

#Steps Button for z
def zenter_button():
    zsteps=int(zsteps_inp.get())
    if zsteps < 0:
        seq.reverse()
        for i in range(-zsteps):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(axisz[pin], seq[halfstep][pin])
                    time.sleep(0.001)
        seq.reverse()
    else:
        for i in range(zsteps):
            for halfstep in range(8):
                for pin in range(4):
                    GPIO.output(axisz[pin], seq[halfstep][pin])
                    time.sleep(0.001)
zstep_button=tk.Button(root, text="Enter Steps", command=zenter_button)
zstep_button.grid(row=2,column=2,padx=5,pady=5, sticky=tk.W)                   

#Name of Picture file
picname_label=tk.Label(root,bg="lightblue1", text="Name of Picture File: ")
picname_label.grid(row=4,column=0,sticky=tk.W+tk.E)
picname_var=tk.StringVar()
picname_inp=tk.Entry(root,textvariable=picname_var)
picname_inp.grid(row=4,column=1,sticky=tk.W+tk.E)

#Camera Button
def capture_button():
    picname=picname_inp.get()
    camera.resolution=(4056,3040)
    camera.start_preview()
    #camera.start_preview(fullscreen=False,window=(100,20,640,480))
    sleep(4)
    camera.capture(picname_inp.get()+".jpg")
    camera.stop_preview()

picam_button=tk.Button(root, text="Capture Image", command=capture_button)
picam_button.grid(row=4,column=2,padx=5,pady=5,sticky=tk.W)

#Unlimited Start Preview Button
preview_label=tk.Label(root,bg="lightblue1",text="Unlimited Preview")
preview_label.grid(row=5,column=0,sticky=tk.W+tk.E)
def unlimitedpreview_button():
    camera.start_preview(fullscreen=False,window=(100,100,1000,1000))

startpreview_button=tk.Button(root, text ="Start Preview",command=unlimitedpreview_button)
startpreview_button.grid(row=5,column=1,padx=5,pady=5,sticky=tk.W+tk.E)

#Unlimited Stop Preview Button
def stoppreview_button():
    camera.stop_preview()
stoppreview_button=tk.Button(root, text="Stop Preview", command=stoppreview_button)
stoppreview_button.grid(row=5,column=2,padx=5,pady=5,sticky=tk.W+tk.E)

#Instructions
left_label=tk.Label(root,bg="ivory2", text="For LEFT enter:\n NEGATIVE X value")
left_label.grid(row=6,column=0,padx=5,pady=5,sticky=tk.W+tk.E)

right_label=tk.Label(root,bg="ivory2", text="For RIGHT enter:\n POSTIVE X value")
right_label.grid(row=6,column=1,sticky=tk.W+tk.E)

up_label=tk.Label(root,bg="lavender blush", text="For UP enter:\n NEGATIVE Y value")
up_label.grid(row=7,column=0,padx=5,pady=5,sticky=tk.W+tk.E)

down_label=tk.Label(root,bg="lavender blush", text="For DOWN enter:\n POSITIVE Y value")
down_label.grid(row=7,column=1,sticky=tk.W+tk.E)

closer_label=tk.Label(root,bg="AntiqueWhite1",text="For CLOSER enter:\n NEGATIVE Z value")
closer_label.grid(row=8,column=0,padx=5,pady=5,sticky=tk.W+tk.E)

away_label=tk.Label(root,bg="AntiqueWhite1", text="For AWAY enter:\n POSITVE Z value")
away_label.grid(row=8,column=1,sticky=tk.W+tk.E)

#LED Brightness Slider
horizontal =tk.Scale(root,from_=0,to=100,resolution=1,orient=tk.HORIZONTAL)
horizontal.grid(row=9,column=0)

def enter_button():
    led.ChangeDutyCycle(horizontal.get())

brightness_button=tk.Button(root,text="Enter Brightness",command=enter_button)
brightness_button.grid(row=9,column=1)

root.mainloop()
 
