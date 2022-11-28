import machine
#OLED screen library
import ssd1306
#library for HTTP reqeuests
import urequests
import network
import time
import credentials

#Initialize i2c connection and ssd1306 to communicate over i2c

sda_pin = machine.Pin(4)
scl_pin = machine.Pin(5)

i2c = machine.SoftI2C(sda=sda_pin, scl=scl_pin)
display = ssd1306.SSD1306_I2C(128, 64, i2c)
screen_width = 16

#powerbank wakeup pin

wakeup_pin = machine.Pin(15, machine.Pin.OUT, value=0)

#display title

display.text('PARENT PORTAL',0,0)
display.show()

#WiFi credentials

ssid = credentials.ssid
pw = credentials.pw

message_url = credentials.message_url

def idle(msecs):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.IDLE)
    rtc.alarm(rtc.ALARM0,msecs)
    machine.idle()

def deep_sleep(msecs):
    rtc = machine.RTC()
    rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)
    rtc.alarm(rtc.ALARM0,msecs)
    machine.deepsleep()

def display_message(text):
    #clears lower half of display
    display.fill_rect(0,16,127,63,0)
    #takes a string and displays each line
    lines = text.split("\n")
    for line, i in zip(lines, [16,26,36,46,56]):
        display.text(line,0,i)
    
    display.show()

def wake_up_powerbank(pin):
    pin.value(1)
    time.sleep(0.3)
    pin.value(0)
    

def wrap_text(text, width):
    text = text.strip()
    if len(text) <= width:
        return text
    else:
        last_space = text.rfind(" ",0,width)
        
        index_to_split = last_space if last_space != 1 else width   
        
        split_text = [text[0:index_to_split],text[index_to_split+1:]]
        first_half = split_text[0].rstrip()
        second_half = split_text[1].lstrip()
        return first_half + "\n" + wrap_text(second_half, width)
    
while True:
    # connect to WiFi
    
    do_connect(ssid,pw)
    
    #request response from webserver, most recent post
    
    request = urequests.get(url=message_url)

    #parse response
    
    message_content = request.text
    display_message(wrap_text(message_content,screen_width))

    #Turn off wifi and cycle wakeup
    
    disable_wifi()
    
    #Keep powerbank awake
    
    for i in range(240):
        wake_up_powerbank(wakeup_pin)
        time.sleep(15)
        
    

