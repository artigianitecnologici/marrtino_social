#!/usr/bin/env python

from __future__ import print_function

import thread
import socket

import argparse

import sys, time, os, glob, shutil, math, datetime

from tmuxsend import TmuxSend


def run_server(port):

    # Create a TCP/IP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #sock.settimeout(3)
    # Bind the socket to the port
    server_address = ('', port)
    sock.bind(server_address)
    sock.listen(1)
    print("ROS social server started on port %d ..." %port)

    tmux = TmuxSend('bringup', ['social','cmd'])

    connected = False
    dorun = True
    while dorun:

        if not connected:
            print("-- Waiting for connection ...")
        while (dorun and not connected):
            try:
                # Wait for a connection
                connection, client_address = sock.accept()
                connected = True
                print ('-- Connection from %s'  %client_address[0])
            except KeyboardInterrupt:
                print("User interrupt (quit)")
                dorun = False
            except Exception as e:
                print(e)
                pass # keep listening
    
        if not dorun:
            return

        # print("-- Waiting for data...")
        data = None
        while dorun and connected and data is None:
            # receive data
            try:
                #connection.settimeout(3) # timeout when listening (exit with CTRL+C)
                data = connection.recv(320)  # blocking
                data = data.strip()
            except KeyboardInterrupt:
                print("User interrupt (quit)")
                dorun = False
            except socket.timeout:
                data = None
                print("socket timeout")

        if data is not None:
            if len(data)==0:
                connected = False
            else:
                print(data)
                rfolder = "~/src/marrtino_social/launch"
                cfolder = "~/src/marrtino_social/config"
                                
                # social normale con pan e
                if data=='@social_robot_start':
                    tmux.cmd(0,'cd %s' %rfolder)
                    tmux.cmd(0,'roslaunch social.launch')             
                elif data=='@robot_start': 
                    tmux.cmd(0,"echo '@robot' | netcat -w 1 localhost 9236") # robot

                elif data=='@robot_kill': 
                    tmux.cmd(0,"echo '@robotkill' | netcat -w 1 localhost 9236") # robot
                
                
                elif data=='@audio_start': 
                    tmux.cmd(0,"echo '@audio' | netcat -w 1 localhost 9239") # audio start
                    
               
                elif data=='@speech_start': 
                    tmux.cmd(0,"echo '@audio' | netcat -w 1 localhost 9239") # audio start
                    sfolder = "~/src/marrtino_social/script"
                    tmux.cmd(0,'cd %s' %sfolder)
                    tmux.cmd(0,'python speech.py')

                # start social no servo 
                elif data=='@socialns_start': 
                    tmux.cmd(0,'cd %s' %rfolder)
                    tmux.cmd(0,'roslaunch socialnoservo.launch')
                     
                elif data=='@audio_stop': 
                    tmux.cmd(0,"echo '@audiokill' | netcat -w 1 localhost 9239") # audio stop    
                    
                elif data=='@tracker_start': 
                    tmux.cmd(0,'cd %s' %rfolder)
                    tmux.cmd(0,'roslaunch tracker.launch')
                
   
                                
                else:
                    print('Unknown command %s')



if __name__ == '__main__':

    default_port = 9250

    parser = argparse.ArgumentParser(description='social bringup')
    parser.add_argument('-server_port', type=int, default=default_port, help='server port')

    args = parser.parse_args()

    run_server(args.server_port)

