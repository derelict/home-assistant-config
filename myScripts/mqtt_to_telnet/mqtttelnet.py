import paho.mqtt.client as mqttClient
import telnetlib
import subprocess
import sys, socket, os, time


debug = "true"

HOST = "10.2.20.128"
PORT = "2167"

broker_address= "10.2.151.1"  #Broker address
port = 1883                        #Broker port
user = ""                    #Connection username
password = ""            #Connection password

myname = "mqtt_to_telnet"


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

  
    myPayload = message.payload.lower()
    myTopic = message.topic.lower()
        
    print "Message Topic   : "  + myTopic
    print "Message Payload : "  + myPayload
    
    telnetObj=telnetlib.Telnet(HOST,PORT)
    message = ("\r" + myPayload + "\r").encode('ascii')
    telnetObj.write(message)
    telnetObj.close()
  

    print "#######################################################################################"
    print

Connected = False   #global variable for the state of the connection
 
client = mqttClient.Client(myname + "_MQTT_Connection")               #create new instance
#client.username_pw_set(user, password=password)    #set username and password

client.on_connect = on_connect                      #attach function to callback
client.on_message = on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    print("In Wait loop")
    time.sleep(0.1)
 
client.subscribe("/1OG/mediaroom/beamer/serialdata")

 
try:
    while True:
        #detailedstatus()
        time.sleep(1)
 
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()
    
    
