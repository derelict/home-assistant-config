import paho.mqtt.client as mqttClient
import time


import subprocess
import time
import datetime
import sys, socket, os

import json

shieldips = {}
shieldips['10.2.71.1'] = {}
shieldips['10.2.71.2'] = {}

# https://developer.android.com/reference/android/view/KeyEvent

# adb shell am start -n com.package.name/com.package.name.ActivityName
# adb shell monkey -p your.app.package.name 1
# pm list packages -f

# com.google.android.youtube.tv
# com.aviq.wilmaa.android.lounge
# com.plexapp.android


apps = {

"Wilmaa TV" : {
                                   "app" : "com.aviq.wilmaa.android.lounge",
                  "videoplayback_detect" : True,
      "videoplayback_required_wakelocks" : 2,
       "videoplayback_required_activity" : "LoungeActivity",
"videoplayback_transission_count_needed" : 3,
},

"Home Screen" : {
                 "app" : "com.google.android.leanbacklauncher",
"videoplayback_detect" : False,
},

}


adb_keycodes = {
"0"              : 7,
"1"              : 8,
"2"              : 9,
"3"              : 10,
"4"              : 11,
"5"              : 12,
"6"              : 13,
"7"              : 14,
"8"              : 15,
"9"              : 16,
"power"          : 26,      # Power Button
"sleep"          : 223,     # Sleep Button
"suspend"        : 276,     # Soft Sleep Button
"resume"         : 224,     # Wakeup Button 
"pairing"        : 225,     # Pairing Button
"settings"       : 176,     # Settings Button
                 
"input"          : 178,     # Source TV
"sat"            : 237,     # Source SAT
"hdmi1"          : 243,     # Source HDMI1
"hdmi2"          : 244,     # Source HDMI2
"hdmi3"          : 245,     # Source HDMI3
"hdmi4"          : 246,     # Source HDMI4
"composite1"     : 247,     # Source Compsite1
"composite2"     : 248,     # Source Compsite2
"component1"     : 249,     # Source Component1
"component2"     : 250,     # Source Component2
"vga"            : 251,     # Source VGA
"text"           : 233,     # Source Video-Text
                            
"fast_forward"   : 90,      # media button
"next"           : 87,      # media button
"pause"          : 127,     # media button
"play"           : 126,     # media button
"play_pause"     : 85,      # media button
"previous"       : 88,      # media button
"record"         : 130,     # media button
"rewind"         : 89,      # media button
"skip_backward"  : 273,     # media button
"skip_forward"   : 272,     # media button
"step_backward"  : 275,     # media button
"step_forward"   : 274,     # media button
"stop"           : 86,      # media button
"top_menu"       : 226,     # media button

"home"           : 3,       # Home Button
"menu"           : 82,      # Menu Button
"back"           : 4,       # Back Button
"top"            : 122,     # Top Button
"end"            : 123,     # End Button
"enter"          : 66,      # Enter Button
"up"             : 19,      # UP Button
"down"           : 20,      # DOWN Button
"left"           : 21,      # LEFT Button
"right"          : 22,      # RIGHT Button
"sysup"          : 280,     # SysUp Button
"sysdown"        : 281,     # SysDown Button
"sysleft"        : 282,     # SysLeft Button
"sysright"       : 283,     # SysRight Button
                 
"blue"           : 186,     # Blue Button
"green"          : 184,     # Green Button
"red"            : 183,     # Red Button
"yellow"         : 185,     # Yellow Button
"move_home"      : 122,     # MoveHome Button
"search"         : 84,      # Search Button
                 
"volup"          : 24,      # VolUp Button
"voldown"        : 25,      # VolDown Button
"mute"           : 164,     # Mute Button
                 
"lastch"         : 229,     # LastChannel Button
}

def startapp(myIP, myApptoStart):

    try:
      apps[myApptoStart]["app"]
      print "    --> App found with Package Name: " + apps[myApptoStart]["app"]
    except:
      print "    --> APP NOT Found in my registry"
      return 1
           
           
#adb shell monkey -p your.app.package.name 1

    sendbutton(myIP, "224")
        
    try:
        appstart_output = subprocess.check_output(['adb', '-s', myIP, 'shell', 'monkey', '-p', apps[myApptoStart]["app"], '1'])
    except subprocess.CalledProcessError as sperr:
        appstart_output = ""
    
    print appstart_output
    
def on_connect(client, userdata, flags, rc):
 
    if rc == 0:
 
        print("Connected to broker")
 
        global Connected                #Use global variable
        Connected = True                #Signal connection 
 
    else:
 
        print("Connection failed")
 
def sendbutton(myIP, myKeycode):

   #print myIP
   #print myKeycode

    try:
       adb_keycodes[myKeycode]
       print "    --> Button found with keycode: " + str(adb_keycodes[myKeycode])
    except:
       print "    --> Button NOT Found"
       return 1
           
    try:
        cmd_output = subprocess.check_output(['adb', '-s', myIP, 'shell', 'input', 'keyevent', str(adb_keycodes[myKeycode])])
    except subprocess.CalledProcessError as sperr:
        cmd_output = ""
    
    print cmd_output
    
def on_message(client, userdata, message):

    #print "------------------------------------------------------------[ Message received ]------------------------------------------------------------"

    
    print "#######################################################################################"
    print "# Message Received"
    print "#######################################################################################"

    
    val1 = message.topic.split('/shield/')
    val2 = val1[1].split('/')
    myIP = val2[0]
    myPayload = message.payload.lower()
    myTopic = message.topic
        
    print "Message Topic   : "  + myTopic
    print "Message Payload : "  + myPayload
    
    check_online_and_connect(myIP)
    
    if "sendbutton" in myTopic:
               
        print " --> Button : " + myPayload + " for ip : " + myIP
        
        sendbutton(myIP, myPayload)
    
    if "/appstart/set" in myTopic:
    
        print " --> Start request for App : " + myPayload + " for ip : " + myIP
        
        startapp(myIP, myPayload)
        
    
    if "/powerstate/set" in myTopic:
                
        print " --> Powerstate : " + myPayload + " for ip : " + myIP
        
        turn_device_on_off(myIP, myPayload)
        
    print "#######################################################################################"
    print

        
def check_online_and_connect(ip):

    devices = subprocess.check_output(['adb', 'devices'])
    
    for row in devices.split('\n'):
       if ip in row and "online" in row :
           print " --> Device " + ip + " is online"
           return
       
       
    print " --> Device " + ip + " is offline. Trying to Connect"
    output = subprocess.check_output(['adb', 'connect', ip])
    print output
                   

def turn_device_on_off(myIP, myState):

        myCurrentPowerState = check_power_state(myIP)

        if myCurrentPowerState != myState :
            print "    --> Payload : " + myState + " differs from current state : " + myCurrentPowerState + " .. Therefore toggling Power"
            sendbutton(myIP, str(adb_keycodes["power"]))
        else:
            print "    --> Payload : " + myState + " is the same as current state : " + myCurrentPowerState + " .. Therefore nothing todo here."
            
        #time.sleep(1)
        
        client.publish("/adb/shield/" +  myIP + "/powerstate",         myState)
        
        

def check_power_state(ip):

    #check_online_and_connect(ip)

    try:
        mypower_output = subprocess.check_output(['adb', '-s', ip, 'shell', 'dumpsys', 'power'])
    except subprocess.CalledProcessError as sperr:
        mypower_output = ""

    for row in mypower_output.split('\n'):
    
        if 'Display Power: state' in row:
        
            value = row.split('=')
            
            if value[1].lower() == "on":
                print "Current Display Status is ON"
                return "on"
            else:
                print "Current Display Status is OFF"
                return "off"
        
    
    print "Current Display Status is unknown. Defaulting to OFF"
    return "off"
        
def detailedstatus():

    for ip in shieldips:
    
        myWakeLocks = 0
        mWakefulness = "Fault"
        mDisplayPowerState = "Fault"
        mSerial = "Fault"
        focusapp = "Fault"
        focuswindow = "Fault"
        appname = "Unknown"
        mVideoPlayback = "off"
        
        #print "--------------------------------------------------------[ CHECKING SHIELD STATUS ]--------------------------------------------------------"
        
        print "#######################################################################################"
        print "# Checking Shield Status"
        print "#######################################################################################"
      
        check_online_and_connect(ip)
        
        try:
            power_output = subprocess.check_output(['adb', '-s', ip, 'shell', 'dumpsys', 'power'])
        except subprocess.CalledProcessError as sperr:
            power_output = ""
            continue        

        for row in power_output.split('\n'):
 
           if 'mWakefulness=' in row:
                value = row.split('=')
                mWakefulness=value[1]
                #gotstatus += 1

           if 'Display Power: state' in row:
                value = row.split('=')
                mDisplayPowerState=value[1]
                #gotstatus += 1

           if 'SCREEN_BRIGHT_WAKE_LOCK' in row:
                myWakeLocks += 1
                #gotstatus += 1
       
           if 'AudioMix' in row:
                myWakeLocks += 1
                #gotstatus += 1   

                
        try:
            prop_output = subprocess.check_output(['adb', '-s', ip, 'shell', 'getprop'])
        except subprocess.CalledProcessError as sperr:
            prop_output = ""
            continue
        

        for row in prop_output.split('\n'):
             
         if '[ro.serialno]' in row:
            value = row.split(': ')
            mSerial = value[1].strip('[').strip(']')           
 

        try:
            window_output = subprocess.check_output(['adb', '-s', ip, 'shell', 'dumpsys', 'window', 'windows'])
        except subprocess.CalledProcessError as sperr:
            window_output = ""
            continue  

        for row in window_output.split('\n'):
 
           if 'mCurrentFocus=' in row:
                
                value = row.split('=')

                try:
                    currfocus = value[1]
                except:
                    currfocus = "none"
                
                   
                
                if 'dream' in currfocus:
                    focusapp = "dream"
                    focuswindow = "dreaming"
                    
                else:
                    
                    appvalue = currfocus.split('/')
                    
                    try:
                        focusapp = appvalue[0].split(' ')[2]
                    except:
                        focusapp = "none"
                        
                    try:
                        focuswindow = appvalue[1].strip('}')
                    except:
                        focuswindow = "none"
                    


        
        
        for myApp in apps:
              
              if apps[myApp]["app"] == focusapp:
                print "  --> Found Match in APP DB: " + myApp
                appname = myApp
                
                if apps[myApp]["videoplayback_detect"]:
                    print "  --> " + myApp + " is offering Video Playback Detection. Checking..."
                    
                    if myWakeLocks >= apps[myApp]["videoplayback_required_wakelocks"]:
                        print "    --> Wakelocks matched. Needed : " + str(apps[myApp]["videoplayback_required_wakelocks"]) + " ... Current : " + str(myWakeLocks)
                        
                        if apps[myApp]["videoplayback_required_activity"].lower() in focuswindow.lower():
                            print "    --> Window Name also matched successfully. Setting VidepPlayBack to on!"
                            mVideoPlayback = "on"
                        else:
                            print "No Videoplayback detected"
                            
                    else:
                        print "No Videoplayback detected"

                        
          
        myPowerState = mDisplayPowerState.lower()
		
        myWakeLocks = str(myWakeLocks)        
       
        previousshieldips = json.dumps(shieldips[ip])
        
        shieldips[ip]['mWakefulness'] = mWakefulness
        shieldips[ip]['mDisplayPowerState'] = mDisplayPowerState
        shieldips[ip]['myWakeLocks'] = myWakeLocks
        shieldips[ip]['mSerial'] = mSerial
        shieldips[ip]['focusapp'] = focusapp
        shieldips[ip]['focuswindow'] = focuswindow
        shieldips[ip]['powerstate'] = myPowerState
        shieldips[ip]['mVideoPlayback'] = mVideoPlayback
        shieldips[ip]['appname'] = appname
        
        currentshieldips = json.dumps(shieldips[ip]) 
        
        
        if previousshieldips != currentshieldips:
        
            #print "---------------------------------------[ STATUS has changed ]---------------------------------------"
            print
            print "##############################################################"
            print "# Status has Changed"
            print "##############################################################"
        
            now = datetime.datetime.now()    
            
            print "Time Changed   : " + str(now)
            print
            print "IP Address     : " + ip
            print           
            print "Wakestate      : " + shieldips[ip]['mWakefulness']
            print "Display Power  : " + shieldips[ip]['mDisplayPowerState']
            print "Powerstate     : " + shieldips[ip]['powerstate']
            print "WakeLocks      : " + shieldips[ip]['myWakeLocks']
            print "Serial         : " + shieldips[ip]['mSerial']
            print "Focused app    : " + shieldips[ip]['focusapp']
            print "Focused window : " + shieldips[ip]['focuswindow']
            print "App Name       : " + shieldips[ip]['appname']
            print "Video Playback : " + shieldips[ip]['mVideoPlayback']

            print "##############################################################"
            print


            client.publish("/adb/shield/" +  ip + "/mWakefulness",       shieldips[ip]['mWakefulness'])
            client.publish("/adb/shield/" +  ip + "/mDisplayPowerState", shieldips[ip]['mDisplayPowerState'])
            client.publish("/adb/shield/" +  ip + "/myWakeLocks",        shieldips[ip]['myWakeLocks'])
            client.publish("/adb/shield/" +  ip + "/focusapp",           shieldips[ip]['focusapp'])
            client.publish("/adb/shield/" +  ip + "/focuswindow",        shieldips[ip]['focuswindow'])
            client.publish("/adb/shield/" +  ip + "/appname",            shieldips[ip]['appname'])
            client.publish("/adb/shield/" +  ip + "/mVideoPlayback",     shieldips[ip]['mVideoPlayback'])

            client.publish("/adb/shield/" +  ip + "/powerstate",         shieldips[ip]['powerstate'])
            
        else:
            print "   --> No State Changes so far"
        
        print "#######################################################################################"
        print
        print

       
 
Connected = False   #global variable for the state of the connection
 
broker_address= "mqtt"  #Broker address
port = 1883                        #Broker port
user = ""                    #Connection username
password = ""            #Connection password
 
client = mqttClient.Client("Python")               #create new instance
#client.username_pw_set(user, password=password)    #set username and password
client.on_connect= on_connect                      #attach function to callback
client.on_message= on_message                      #attach function to callback
 
client.connect(broker_address, port=port)          #connect to broker
 
client.loop_start()        #start the loop
 
while Connected != True:    #Wait for connection
    time.sleep(0.1)
 
client.subscribe("/adb/shield/+/sendbutton")
client.subscribe("/adb/shield/+/powerstate/set")
client.subscribe("/adb/shield/+/appstart/set")
 
try:
    while True:
        detailedstatus()
        time.sleep(1)
 
except KeyboardInterrupt:
    print "exiting"
    client.disconnect()
    client.loop_stop()
    
    
# /shieldcontrol_v1/10.2.71.1/power/set
# /shieldcontrol_v1/10.2.71.1/presskey/set
# /shieldcontrol_v1/10.2.71.1/detailedstatus/set
