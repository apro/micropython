
from umqtt.simple import MQTTClient
#import network
#import time
import myconfig
import json

mtref = 0
minterval = 10
mqclient = None

def sub_cb(topic, msg):
  global mtref
  global minterval
  m = json.loads(msg)
  print((topic, msg))
  
  try:
    mtref = float(m['tref'])
    minterval = int(m['interval'])
  except:
    print('invalid float value:',msg)


def init():
  global mqclient
  m = myconfig.config['mqtt']
  print('mqtt init:',m['client_id'], m['server'],m['user'],m['password'])
  try:
    mqclient = MQTTClient(m['client_id'], m['server'],0,m['user'],m['password'])     #create a mqtt client
    mqclient.set_callback(sub_cb)                    #set callback
    mqclient.connect()                               #connect mqtt
    mqclient.subscribe(m['topic_in'])                        #client subscribes to a topic
    print("Connected to %s, subscribed to %s topic" % (m['server'],m['topic_in']))
  except:
    print('MQTT connection error')

def publish(tref, t1, t2, power, interval):  
  global mqclient
  msg = {'tref': tref, 't1': t1, 't2': t2, 'power': power, 'interval': interval}
# print(json.loads(msg))
  try:
    mqclient.publish(myconfig.config['mqtt']['topic_out'], json.dumps(msg))
  except:
    print('mqtt publish error')


