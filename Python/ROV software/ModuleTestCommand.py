##############################################################
# Main driver program for the threading/modular layout       #
##############################################################
# This program imports the two main modules, ROV_Graphical   #
# and ROV_Communications, and launches two threads to manage #
# them. All the magic happens in those two threads~          #
##############################################################
#             Full program changes/updates:                  #
# Updated controller interface and GUI by Keith Smee         #
# New queue system and updated structure by Nathan Murrow    #
# New modular program layout by Jonah Brooks                 #
#                   Dec. 17th 2010                           #
##############################################################

#######################################################################
# Changes for swim test 2, January 13th, 2011:
#       Swapped the "forward-left" and "forward-right" code
#       Moved the Y-Inversion hack to before the redundancy test
#           to solve a "sticking" bug in hard right to hard left
#       Removed the GUI, print statements, and rate() calls
#           to reduce latency
#
#       Arduino code: PID functions are commented out
#
#       TODO: Modify both ends to send full 10 bit data from sensor
#           
######################################################################


import ROV_Communications, ROV_Control
import thread
import time

#starts threads for communications and GUI
try:
    thread.start_new_thread( ROV_Communications.communications, () )
    time.sleep(0.1)
    thread.start_new_thread( ROV_Control.control, () )
except:
    print "Error: unable to start thread"

#waits while the threads are executing
while ROV_Communications.exitFlag and ROV_Control.exitFlag == False:
    pass
