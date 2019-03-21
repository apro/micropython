# requires: https://github.com/boochow/MicroPython-ST7735

import time
from ST7735 import TFT
from sysfont import sysfont
from terminalfont import terminalfont
from machine import SPI,Pin
import math
from myconfig import config
import os
import temperature as temp
from wificonnect import wlan 
import display
import mqtt


display.init()
temp.init()

t1rom, ok = temp.check_rom(config['t1'])
if ok:
  print('T1 found')
  display.info('T1 found')
time.sleep(2)

t2rom, ok = temp.check_rom(config['t2'])
if ok:
  print('T2 found')
  display.info('T2 found',top=10)

print('T1:',t1rom,' T2:',t2rom)
time.sleep(2)

interval = 10
t1 = 0
t2 = 0
tref = 22
power = 0
mqtt.init()
mqtt.mtref = tref
mqtt.minterval = interval

display.clear_header()
display.header(wlan.ifconfig()[0])

while True:
  display.error('')
  temp.convert()
  try:
    t1, ok = temp.read(t1rom)
    t2, ok = temp.read(t2rom)
    print('tref: %.2f T1: %.2f T2: %.2f power: %.2f interval: %ds' % (tref, t1, t2, power, interval))
    mqtt.publish(tref, t1, t2, power, interval)
    display.temp(tref, t1, t2)
  except:
    print('err or what???')
    display.error('error reading temp?')
        
  i = 0
  while i<=interval: 
    mqtt.mqclient.check_msg()
    time.sleep(1)
    i +=1
    if not mqtt.mtref is None:
      tref = mqtt.mtref
    if not mqtt.minterval is None:
      interval = mqtt.minterval
 
