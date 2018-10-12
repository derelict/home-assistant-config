import paho.mqtt.client as mqttClient
import time

import os
import serial


import subprocess
import time
import datetime
import sys, socket, os

import json

debug = "true"

if socket.gethostname().lower().find("hcp") >= 0:
 print "Set Hostname to mediapc02"
 myname="mediapc02"
 myzone="zone10"
elif socket.gethostname().lower().find("r003") >= 0:
 print "Set Hostname to mediapc03"
 myname="mediapc03"
 myzone="zone03"
elif socket.gethostname().lower().find("r001") >= 0:
 print "Set Hostname to mediapc01"
 myname="mediapc01"
 myzone="zone01"
elif socket.gethostname().lower().find("r002") >= 0:
 print "Set Hostname to mediapc02"
 myname="mediapc02"
 myzone="zone02"
else :
 print "Set Hostname to unknown"
 myname="unknown"
 myzone="zone10"

print "myname : " + myname
print "myzone : " + myzone

if myname == "mediapc02":

        if debug == "true":
         print "Connecting Serial Ports"


        try:
        
#         conndenon = serial.Serial('/dev/denon',
#                     baudrate=9600,
#                     bytesize=serial.EIGHTBITS,   
#                     parity=serial.PARITY_NONE,   
#                     stopbits=serial.STOPBITS_ONE,
#                     timeout=1,
#                     xonxoff=0,
#                     rtscts=0  
#                     )
#
#         conndenon.setDTR(True)
#         conndenon.setRTS(True)


         connbeamer = serial.Serial('/dev/beamer',
                     baudrate=115200,
                     bytesize=serial.EIGHTBITS,   
                     parity=serial.PARITY_NONE,   
                     stopbits=serial.STOPBITS_ONE,
                     timeout=1,
                     xonxoff=0,
                     rtscts=0
                     )
                      
         connbeamer.setDTR(True)
         connbeamer.setRTS(True)

         print " --> Success"
        
        except:
         print " --> Serial Connection Error"





def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
    
def on_message(client, userdata, message):

   
    print "#######################################################################################"
    print "# Message Received"
    print "#######################################################################################"

    
# topic: /rpi_support/mediapc02/sendserial
# payload: pow=on

# topic: /rpi_support/mediapc02/sendir/samsung
# payload: on

# /rpi_support/mediapc/powerstate/climate/set

    #val1 = message.topic.split("/rpi_support/" + myname + "/")
    #val2 = val1[1].split('/')
    myPayload = message.payload.lower()
    myTopic = message.topic.lower()
        
    print "Message Topic   : "  + myTopic
    print "Message Payload : "  + myPayload
    
    
    if "sendserial" in myTopic:

        if myname == "mediapc02":

            print " --> SendSerial : " + myPayload
            connbeamer.write(chr(13) + "*" + myPayload + "#" + chr(13))

        

    if "sendir" in myTopic:

        val1 = myTopic.split("/rpi_support/" + myname + "/")
        val2 = val1[1].split('/')
        myDevice = val2[1]
        myButton = myPayload

        print " --> Send IR : -> Device : " + myDevice + " -> Button : " + myButton
        os.system('/usr/bin/irsend SEND_ONCE ' + myDevice + ' ' + myButton )

    #client.publish( myTopic + "/state", myPayload)    

    print "#######################################################################################"
    print






Connected = False   #global variable for the state of the connection
 
broker_address= "10.2.151.1"  #Broker address
port = 1883                        #Broker port
user = ""                    #Connection username
password = ""            #Connection password
 
client = mqttClient.Client(myname + "_MQTT_Connection")               #create new instance
#client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe("/rpi_support/" + myname + "/#")
#client.subscribe("/rpi_support/+/powerstate/set")
#client.subscribe("/rpi_support/+/appstart/set")
 
try:
    while True:
        #detailedstatus()
        time.sleep(1)
 
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()
    
    
