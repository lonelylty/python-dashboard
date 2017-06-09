#!/usr/bin/python

import time
import serial
import sys
import signal
import websocket
import subprocess
import math
import requests
from sys import stdout

def signal_handler(signum, frame):
    print ('exiting...')
    try:
        ser.close()
    except:
        pass
    sys.exit(0)

# configure the serial connections (the parameters differs on the device you are connecting to)
version = '0.1 - 25th May 2017'
    
WSURL = "ws://cnadashboard.sq2.cards/ws"
    
timeout = 10
waittime = 1
counter = 1

def on_message(ws, message):
    print ("{}".format(message))
    
def on_error(ws, error):
    global WSURL,timeout
    print ("## {} (retry in 10s)##".format(error))
    signal.signal(signal.SIGINT, signal_handler)
    time.sleep(timeout)
    ws = websocket.WebSocketApp(WSURL,on_message=on_message,on_error=on_error,on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
    
def on_close(ws):
    global WSURL,timeout
    print ('## connection to server closed (retry in 10s)##')
    signal.signal(signal.SIGINT, signal_handler)
    time.sleep(timeout)
    ws = websocket.WebSocketApp(WSURL,on_message=on_message,on_error=on_error,on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()

def on_open(ws):
    global WSURL,timeout,waittime,counter
    signal.signal(signal.SIGINT, signal_handler)
                    
if __name__ == "__main__":
    print ("Websocket Agent v{}\n".format(version))
    
    websocket.enableTrace(False)
    ws = websocket.WebSocketApp(WSURL,on_message=on_message,on_error=on_error,on_close=on_close)
    ws.on_open = on_open
    ws.run_forever()
