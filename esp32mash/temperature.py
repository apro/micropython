# temperature module
import onewire
import ds18x20
from machine import Pin
from time import sleep_ms

def init():
  print('init wire')
  global ds
  global roms
  ow = onewire.OneWire(Pin(25))   #Init wire
  ow.scan()
  print('ds create')
  ds=ds18x20.DS18X20(ow)          #create ds18x20 object
  roms=ds.scan()                #scan ds18x20


def check_rom(addr):
  found = None
  for rom in roms:
#    print(rominfo(rom))
    if addr == rominfo(rom):
      found = rom
  if found is None:
    print('no rom %s found' % addr)
  return found, found != None


def convert():
  try:
    ds.convert_temp()             #convert temperature
    sleep_ms(750)
  except:
    print('convert error')
  

def read(rom):
  temp = None
  try:
    temp = ds.read_temp(rom)
#    print(rom, ' ',temp )
  except:
    print('temp read err')
  return temp, temp != None


def rominfo(rom):
  return ''.join('{:02x}'.format(x) for x in rom)
  



