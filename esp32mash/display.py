import time
from ST7735 import TFT
from sysfont import sysfont
from terminalfont import terminalfont
from machine import SPI,Pin

header_size=2*8+20

def init():
  global tft
  spi = SPI(2, baudrate=20000000, polarity=0, phase=0, sck=Pin(14), mosi=Pin(13), miso=Pin(12))
  tft=TFT(spi,16,17,18)
  tft.initr()
  tft.rgb(True)
  tft.rotation(3)
  tft.fill(TFT.BLACK)

# 
def info(text, top=0, color=TFT.WHITE, bground=TFT.BLACK, size=1):
  tft.fillrect((0,top),(tft.size()[0],sysfont["Height"]*size),bground)
  tft.text((0, top), text, color, sysfont, size, nowrap=True)

def error(text):
  info(text,tft.size()[1]-8, color=TFT.RED)
  
def clear_header():  
  tft.fillrect((0,0),(tft.size()[0],header_size),TFT.BLACK)

def header(ip):
  info('IP: %s' % ip , 0, TFT.YELLOW, TFT.GRAY)
  info('Tref  T1   T2', 20, color=TFT.YELLOW, size=2)  

# temp panel 8 to 32 pixels
def temp(tref, t1, t2, diff=1, bground=TFT.BLACK):
  t1color=TFT.GREEN
  t2color=TFT.GREEN
  trefcolor=TFT.WHITE
  y=header_size+4
  x1=0
  x2=3*8*2+8
  x3=x2+3*8*2+8
  
  if t1>tref+diff:
    t1color=TFT.RED
  elif t1<tref-diff:
    t1color=TFT.BLUE
  
  if t2>tref+diff:
    t2color=TFT.RED
  elif t2<tref-diff:
    t2color=TFT.BLUE
    
  tft.fillrect((0,y),(tft.size()[0],y+3*sysfont["Height"]),bground)
  tft.text((x1, y), '%.1f' % tref, trefcolor, sysfont, 2, nowrap=True)
  tft.text((x2, y), '%.1f' % t1  ,   t1color, sysfont, 2, nowrap=True)
  tft.text((x3, y), '%.1f' % t2  ,   t2color, sysfont, 2, nowrap=True)


