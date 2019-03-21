import network

def connect():
    import webrepl
    import myconfig
    import time
    global wlan
    
    retries=5
    while retries>0:
      print('try:',6-retries)
      retries -= 1
      for wifi in myconfig.config['connections']:
        if not wlan.isconnected():
          print('connecting to network...',wifi['ssid'])
          wlan.active(True)
          wlan.connect(wifi['ssid'], wifi['password'])
          wait = 20
          while not wifi.isconnected() and wait>0:
            wait -= 1
            time.sleep_ms(200)
            print('.')
            pass
            
    if wlan.isconnected():
      print('network config:', wlan.ifconfig())
      webrepl.start()
    else:
      print('network unavailable', wlan.ifconfig())

def no_debug():
    import esp
    # this can be run from the REPL as well
    esp.osdebug(None)
    
def init():
  global wlan
  wlan=network.WLAN(network.STA_IF)



