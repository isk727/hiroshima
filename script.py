import os
import sys
import time
from datetime import datetime
import configparser
import webiopi
import RPi.GPIO as GPIO
sys.path.append("../python")
import game

config_ini = configparser.ConfigParser()
config_ini.read('../python/config.ini', encoding='utf-8')
xgame = game.GameClass(config_ini['setting']['Name'], config_ini['setting']['json_file'])

#IN       16(23)
#OUT   18(24)
#RB      22(25)
#BB      37(26)
#PAYBACK 40(21)
STATUS_AP  = 22

st_rb = 0
st_bb = 0

rb_sig_timer = 0
bb_sig_timer = 0
gmCount = 0
bbCount = 0
rbCount = 0
bwCount = 0
BBCT = 0

def setup():
  global xgame
  global config_ini
#  config_ini.read('../python/config.ini', encoding='utf-8')
  GPIO.setmode(GPIO.BCM)
  for i in range(16):
    GPIO.setup(i + 2, GPIO.OUT)
  for i in range(8):
    GPIO.setup(i + 20, GPIO.IN)
    GPIO.setup(i + 20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
  for i in range(16):
    GPIO.output(i + 2, 0)
#  GPIO.add_event_detect(CREDIT_DEC, GPIO.RISING, bouncetime=5)
#  GPIO.add_event_callback(CREDIT_DEC, event_callback_credit_dec)
#  GPIO.add_event_detect(CREDIT_INC, GPIO.RISING, bouncetime=5)
#  GPIO.add_event_callback(CREDIT_INC, event_callback_credit_inc)

#    GPIO.add_event_detect(STATUS_AP, GPIO.BOTH, bouncetime=5)
#    GPIO.add_event_callback(STATUS_AP, event_callback_status_ap)
  GPIO.add_event_detect(int(config_ini['GPIO']['STATUS_RB']), GPIO.BOTH, bouncetime=5)
  GPIO.add_event_callback(int(config_ini['GPIO']['STATUS_RB']), event_callback_status_rb)
  GPIO.add_event_detect(int(config_ini['GPIO']['STATUS_BB']), GPIO.BOTH, bouncetime=5)
  GPIO.add_event_callback(int(config_ini['GPIO']['STATUS_BB']), event_callback_status_bb)
#  GPIO.add_event_detect(STATUS_CT, GPIO.BOTH, bouncetime=5)
#  GPIO.add_event_callback(STATUS_CT, event_callback_status_ct)
#    GPIO.add_event_detect(22, GPIO.BOTH, bouncetime=5)
#    GPIO.add_event_callback(22, event_callback_status_ap)

def loop():
#  global xgame
#  now = datetime.now()
#    if int(evRT) + int(evRM) != 46:
  webiopi.sleep(0.1)

def event_callback_status_rb(gpio_pin):
  global st_rb
  global rbCount
  global bwCount
  global rb_sig_timer
  global xgame
  global config_ini
  if GPIO.input(int(config_ini['GPIO']['STATUS_RB'])) == GPIO.LOW:
    time.sleep(0.01)
    rb_sig_timer
    if GPIO.input(int(config_ini['GPIO']['STATUS_RB'])) == GPIO.LOW:
      time.sleep(0.1)
      if GPIO.input(int(config_ini['GPIO']['STATUS_RB'])) == GPIO.LOW:
        if (st_bb == 0 and st_rb == 0):
          log('rb1')
          st_rb = 1
          xgame.ct_rb = int(xgame.ct_rb) + 1
          rbCount = int(rbCount) + 1
          #countUp(bwCount, 2) # bb:2
          bwCount = 0
  else:
    rb_sig_timer = 0
    log('rb0')

def event_callback_status_bb(gpio_pin):
  global st_bb
  global bbCount
  global bwCount
  global bb_sig_timer
  global xgame
  global config_ini
  if GPIO.input(int(config_ini['GPIO']['STATUS_BB'])) == GPIO.LOW:
    time.sleep(0.01)
    log('bb')
    rb_sig_timer
    if GPIO.input(int(config_ini['GPIO']['STATUS_BB'])) == GPIO.LOW:
      time.sleep(0.1)
      if GPIO.input(int(config_ini['GPIO']['STATUS_BB'])) == GPIO.LOW:
        if (st_bb == 0 and st_rb == 0):
          log('bb1')
          st_rb = 1
          xgame.ct_bb = int(xgame.ct_bb) + 1
          bbCount = int(bbCount) + 1
          #countUp(bwCount, 2) # bb:2
          bwCount = 0
  else:
    bb_sig_timer = 0
    log('bb0')

# --------------------------------
# オート
# --------------------------------
def set_point(n):
  global config_ini
#  interval = float(config_ini['setting']['ssd_interval'])
  interval = 1.5
  for i in range(n):
    log(str(i))
#    GPIO.output(AUTO, GPIO.LOW)
    time.sleep(interval)
    GPIO.output(23, GPIO.LOW)
    time.sleep(interval)
    GPIO.output(23, GPIO.HIGH)
    #time.sleep(0.05) config_ini['DEFAULT']['ssd_interval']
  log("set?")


# --------------------------------
# debug
# --------------------------------
def log(s):
  with open('/usr/share/webiopi/htdocs/api/debug.log', 'a') as f:
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + s, file=f)


# --------------------------------
# API
# --------------------------------
@webiopi.macro
def start_game(gkey, point):
  global xgame
  set_point(int(point))
  xgame.start(gkey)
  xgame.json_dump()

@webiopi.macro
def check_game(gkey, point):
  global xgame
  xgame.json_dump()

@webiopi.macro
def stop_game(gkey, point):
  global xgame
  xgame.stop(gkey)
  xgame.json_dump()
