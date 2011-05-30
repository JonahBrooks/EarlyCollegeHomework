##############################################################
# Main controls & Control functions to interact with Comms   #
##############################################################
# This file is the set of functions designed to handle the   #
# controlal thread, and to interact with the Communications  #
# thread. This version contains Nathan's new threading code, #
# including his queue system for exchanging commands between #
# controls and Communications. It was modified slightly by me#
# to incorporate a new modular layout for our program by     #
# adding hooks for additional GUI or control modules. The    #
# Controls module in the ROV_GUIFunctions package is a slight#
# modification of Keith's latest controller interface for the#
# motors, streamlined a bit by Nathan, and altered to allow  #
# this file to run it as a module.                           #
##############################################################
# New thread locking system implemented by Nathan Murrow     #
#                   Dec. 21st 2010                           #
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# Updated controller interface and GUI by Keith Smee         #
# New queue system and updated structure by Nathan Murrow    #
# New modular program layout by Jonah Brooks                 #
#                   Dec. 17th 2010                           #
## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##
# Note: To use the ROV_GUIFunctions package to store extra   #
# functions, create one or more .py files that contain the   #
# functions you need. Each file can contain any number of    #
# logically related functions and/or variables. To add the   #
# file to the ROV_GUIFunctions package, save the .py file in #
# the ROV_GUIFunctions folder, then add the name of the file #
# (without the .py) to the list held in the __init__.py file #
# found in the ROV_GUIFunctions folder. You can then call the#
# function with the following syntax:                        #
#               fileName.functionName(arguments)             #
# This modularity might be a bit of a hassle right now, but  #
# it should save quite a bit of time and effort in the future#
##############################################################

# controls module for ROV interface
import time, threading
from collections import deque
import ROV_Communications
from ROV_ControlFunctions import *
from pygame.locals import *

#flag to shut down all threads and close program
exitFlag = False

#variables to send commands from communications to GUI
controlCommand = ""
controlQueue = deque([])
controlLock = threading.Lock()

#pushes a new controls command into the queue
def pushcontrolCommand(arg):
    global controlQueue
    global controlLock
    controlLock.acquire()
    try:
        controlQueue.append(arg)
        ###print "controlQueue pushed", arg ### test code
    except Exception, e:
        print "controlQueue.append(arg)",e
    controlLock.release()

#executes commands from Communications in GUI
def controlExecute():
    global controlQueue
    global controlLock
    returnvalue = None
    #interpret commands here
    controlLock.acquire()
    ### Test code May 18th
    ###print "Popped controlQueue"
    ### end test code
    try:
        returnvalue = controlQueue.popleft() # For communication testing, remove if needed
    except Exception, e:
        returnvalue = None
    controlLock.release()
    return returnvalue


###############process for the GUI thread######################

def control():
    global exitFlag
    global controlQueue
    try:
        Controls.init()    # Set up the control functions for first use
    except Exception, e:
        print "Error initializing ROV_Control.py", e
        #pygame.init()
        
    while exitFlag == False:
        #strip off events and pass them to ROV_GUI here
        try:
            #GUIEvents = pygame.event.get([MOUSEMOTION, MOUSEBUTTONUP, MOUSEBUTTONDOWN, KEYUP, KEYDOWN])
            #print GUIEvents
            pass
        except Exception, e:
            print "Error gathering events in ROV_Control"
        
        #detect and execute commands from user
        try:
            newCommand = Controls.Refresh(controlExecute())
            if newCommand:      # newCommand is a bytearray returned
                # print newCommand    # by controls, to be sent to comms
                ROV_Communications.pushCommCommand(newCommand[0])
                time.sleep(0.01)
                ROV_Communications.pushCommCommand(newCommand[1])
                time.sleep(0.01)
                ROV_Communications.pushCommCommand(newCommand[2])
                time.sleep(0.01)
            ### Test code, May 18th
            ###while controlQueue:
            ###    Controls.setSensorData(controlExecute())
        except Exception, e:
            print "Error in Controls.Refresh()", e
            #executes commands from communications
##        if controlQueue:    # if controlQueue is not empty
##            controlExecute()
       #update screen here
###############end of the main GUI thread######################
