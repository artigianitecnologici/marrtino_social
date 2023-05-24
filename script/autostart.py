#! /usr/bin/python
import requests
import sys,os
import time



sys.path.append(os.getenv("MARRTINO_APPS_HOME")+"/program")

from robot_cmd_ros import *



def speech(msg):
    #rospy.loginfo('Speech : %s' %(msg))
    emotion("speak")
    say(msg,'it')
    emotion("normal")

    

def listener():
    begin()
   
    
    print("Start MARRTINA Robot")
    pan(0)
    tilt(0)
    
  
    emotion("startblinking")
    speech("Ciao sono martina e sono operativa")
   
        
    end()
     
listener()
