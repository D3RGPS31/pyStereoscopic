#!/usr/bin/python
"""
    Author: D3RGPS31@gmail.com
    Date: 2015/09/11
    Description: Stereoscopic camera(s). Minimum of 1 camera, maximum of 2.
    Input: ~/.pyCulus.json
    Output: ~/.pyCulus.json
    
    Controls for launched windows:
        W increases parallax
        S decreases parallax
        A decreases window size
        D increases window size
        Q quits
        R resets
    
    LICENSE:
        THE BEER-WARE LICENSE" (Revision 42):
        D3RGPS31@gmail.com> wrote this file.  As long as you retain this notice you
        can do whatever you want with this stuff. If we meet some day, and you think
        this stuff is worth it, you can buy me a beer in return.
"""

import cv2
import platform
import math
import json
from pprint import pprint
import os.path
from os.path import expanduser

debug = 1
home = expanduser("~")

if (debug):
    print("Detecting operating system")

# Determine platform and resolution
#if (platform.system() == "Linux" or platform.system() == "Windows"):
    import Tkinter
    root = Tkinter.Tk()
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
#elif (platform.system() == "Windows"):
#    from win32api import GetSystemMetrics
#    width = GetSystemMetrics (0)
#    height = GetSystemMetrics (1)
#else: # No OSX support, lol
#    exit('System not supported. Quitting.')

if (debug):
    print("Operating system is " + platform.system())

# Loads configuration
if (os.path.isfile(home + "/.pyCulus.json")):
    try:
        if (debug):
            print("Loading configuration from file")
        with open(home + "/.pyCulus.json", "r+") as config_file:
            config = json.load(config_file)
        config_file.close()
        oWidth = config["width"]
        oHeight = config["height"]
        oParallax = config["parallax"]
    except:
        if (debug):
            print("Loading configuration from defaults")
        oWidth = 640
        oHeight = 480
        oParallax = 1
else:
    if (debug):
        print("Loading configuration from defaults")
    oWidth = 640
    oHeight = 480
    oParallax = 1

cWidth = oWidth
cHeight = oHeight
cParallax = oParallax

# Create first video capture window
if (debug):
    print("Creating camera 0")
vc1 = cv2.VideoCapture(0)
if (vc1.get(3) != 0.0):
    if (debug):
        print("Camera 0 found")
    vc1.set(3, cWidth)
    vc1.set(4, cHeight)
else:
    exit('No cameras found')

# Create second video capture window
if (debug):
    print("Creating camera 1")
vc2 = cv2.VideoCapture(1)
if (vc2.get(3) != 0.0):
    if (debug):
        print("Camera 1 found")
    vc2.set(3, cWidth)
    vc2.set(4, cHeight)
    cam1 = 1
else:
    if (debug):
        print("Camera 1 not found")
    cam1 = 0

cv2.namedWindow("right", 1)
cv2.namedWindow("left", 1)
cv2.moveWindow("left", ((width / 2) - cWidth), ((height - cHeight ) / 2))
cv2.moveWindow("right", (width / 2), ((height - cHeight ) / 2))

status = 1
ycr = 0
gry = 0
while(status):
    ret,frameA = vc1.read()
    if (ycr):
        frameA = cv2.cvtColor(frameA, cv2.COLOR_BGR2YCR_CB)
    
    if (gry):
        frameA = cv2.cvtColor(frameA, cv2.COLOR_BGR2GRAY)
    
    if (cam1):
        ret,frameB = vc2.read()
        if (ycr):
            frameB = cv2.cvtColor(frameB, cv2.COLOR_BGR2YCR_CB)
        if (ycr):
            frameB = cv2.cvtColor(frameB, cv2.COLOR_BGR2GRAY)
    else:
        frameB = frameA
    
    cv2.imshow("left",cv2.resize(frameA, (cWidth, cHeight), interpolation = cv2.INTER_AREA))
    cv2.imshow("right", cv2.resize(frameB, (cWidth, cHeight), interpolation = cv2.INTER_AREA))
    
    k = cv2.waitKey(30)
    if (k != -1):
        if (k == ord('q')): #quit
            status = 0
            print("Quitting.")
        elif (k == ord('w') and cParallax < 50): #increases parallax value
            cParallax += 1
            print("Parallax: " + str(cParallax))
        elif (k == ord('s') and cParallax > -50): #decreases parallax value
            cParallax -= 1
            print("Parallax: " + str(cParallax))
        elif (k == ord('r')): #resets all values
            cParallax = oParallax
            cWidth = oWidth
            cHeight = oHeight
            print("Parallax reset to " + str(cParallax))
            print("Width set to " + str(cWidth))
            print("Height set to " + str(cHeight))
        elif (k == ord('a') and cWidth > (oWidth / 2)): #decreases window and frame size values
            cWidth = cWidth - 10
            cHeight = cHeight - 10
            print("Width set to " + str(cWidth))
            print("Height set to " + str(cHeight))
        elif (k == ord('d') and cWidth < (oWidth * 2)): #increases window and frame size values
            cWidth = cWidth + 10
            cHeight = cHeight + 10
            print("Width set to " + str(cWidth))
            print("Height set to " + str(cHeight))
        elif (k == ord('y')):
            if (ycr):
                ycr = 0
            else:
                ycr = 1
        elif (k == ord('g')):
            if (ycr):
                gry = 0
            else:
                gry = 1
    
    # Changes frame size
    cv2.resizeWindow("left", cWidth, cHeight)
    cv2.resizeWindow("right", cWidth, cHeight)
    # Moves windows apart from eachother
    cv2.moveWindow("left", int((width / 2) - cWidth + cParallax * 5), int((height - cHeight ) / 2))
    cv2.moveWindow("right", int((width / 2) - cParallax * 5), int((height - cHeight ) / 2))

cv.DestroyWindow("left")
if (cam1):
    cv.DestroyWindow("right")

# Saves configuration
if(os.path.isfile(home + "/.pyCulus.json")):
    config = {}
    config["width"] = cWidth
    config["height"] = cHeight
    config["parallax"] = cParallax
    json_config = json.dumps(config)
    try:
        if (debug):
            print("Saving configuration to file")
        with open(home + "/.pyCulus.json", "w") as config_file:
            config_file.write(json_config)
        config_file.close()
    except:
        print("Problem writing to configuration file.")
