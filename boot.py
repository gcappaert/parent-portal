## Functions to connect ESP8266 to WLAN and turn off wifi

import network
import uos, machine
import gc
gc.collect()
#import webrepl
#webrepl.start()

#Connect to local WiFi

def do_connect(ssid,pw):
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print('Connecting to network')
        wlan.connect(ssid,pw)
        while not wlan.isconnected():
            pass
        print ('network config:', wlan.ifconfig())
    else:
        print ('already connected')

def disable_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(False)
    print ('Wifi is disabled')