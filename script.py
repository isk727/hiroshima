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
xgame = game.GameClass(config_ini['setting']['json_file'])


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
  global config_ini
  GPIO.setmode(GPIO.BCM)

  GPIO.setup(int(config_ini['GPIO']['IN']), GPIO.IN)
  GPIO.setup(int(config_ini['GPIO']['OUT']), GPIO.IN)
  GPIO.setup(int(config_ini['GPIO']['RB']), GPIO.IN)
  GPIO.setup(int(config_ini['GPIO']['BB']), GPIO.IN)

  GPIO.setup(int(config_ini['GPIO']['PAYOUT1']), GPIO.OUT)#（50msec ON OFF)
  GPIO.setup(int(config_ini['GPIO']['PAYOUT2']), GPIO.OUT)
  GPIO.setup(int(config_ini['GPIO']['CLEAR1']), GPIO.OUT)
  GPIO.setup(int(config_ini['GPIO']['CLEAR2']), GPIO.OUT)
  GPIO.setup(int(config_ini['GPIO']['CREDIT']), GPIO.OUT)# （50msec ON OFF)




  
#  for i in range(16):
#    GPIO.setup(i + 2, GPIO.OUT)
#  for i in range(8):
#    GPIO.setup(i + 20, GPIO.IN)
#    GPIO.setup(i + 20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#  for i in range(16):
#    GPIO.output(i + 2, 0)


#  GPIO.add_event_detect(CREDIT_DEC, GPIO.RISING, bouncetime=5)
#  GPIO.add_event_callback(CREDIT_DEC, event_callback_credit_dec)
#  GPIO.add_event_detect(CREDIT_INC, GPIO.RISING, bouncetime=5)
#  GPIO.add_event_callback(CREDIT_INC, event_callback_credit_inc)
  GPIO.add_event_detect(int(config_ini['GPIO']['IN']), GPIO.RISING, bouncetime=5)
  GPIO.add_event_callback(int(config_ini['GPIO']['IN']), event_callback_credit_dec)
  GPIO.add_event_detect(int(config_ini['GPIO']['OUT']), GPIO.RISING, bouncetime=5)
  GPIO.add_event_callback(int(config_ini['GPIO']['OUT']), event_callback_credit_inc)

#    GPIO.add_event_detect(STATUS_AP, GPIO.BOTH, bouncetime=5)
#    GPIO.add_event_callback(STATUS_AP, event_callback_status_ap)
  GPIO.add_event_detect(int(config_ini['GPIO']['RB']), GPIO.BOTH, bouncetime=5)
  GPIO.add_event_callback(int(config_ini['GPIO']['RB']), event_callback_status_rb)
  GPIO.add_event_detect(int(config_ini['GPIO']['BB']), GPIO.BOTH, bouncetime=5)
  GPIO.add_event_callback(int(config_ini['GPIO']['BB']), event_callback_status_bb)
#  GPIO.add_event_detect(STATUS_CT, GPIO.BOTH, bouncetime=5)
#  GPIO.add_event_callback(STATUS_CT, event_callback_status_ct)
#    GPIO.add_event_detect(22, GPIO.BOTH, bouncetime=5)
#    GPIO.add_event_callback(22, event_callback_status_ap)

def loop():
  webiopi.sleep(0.1)

def event_callback_credit_dec(gpio_pin):
    global credit
    global point
    global xgame
    time.sleep(0.05) # 200402
#    if GPIO.input(CREDIT_INC) == GPIO.LOW: # 200402
#    if credit != 0: # 200305
    if xgame.credit != 0: # 200305
        xgame.credit = int(xgame.credit) - 1
        xgame.point = int(xgame.point) - 1
#        credit = int(credit) - 1
#        point = int(point) - 1

def event_callback_credit_inc(gpio_pin):
    global credit
    global point
    global xgame
    time.sleep(0.05) # 200402
#    if GPIO.input(CREDIT_INC) == GPIO.LOW: # 200402
#    credit = int(credit) + 1
#    point = int(point) + 1
    xgame.credit = int(xgame.credit) + 1
    xgame.point = int(xgame.point) + 1


def event_callback_status_rb(gpio_pin):
  global st_rb
  global rbCount
  global bwCount
  global rb_sig_timer
  global xgame
  global config_ini
  if GPIO.input(int(config_ini['GPIO']['RB'])) == GPIO.LOW:
    time.sleep(0.01)
    rb_sig_timer
    if GPIO.input(int(config_ini['GPIO']['RB'])) == GPIO.LOW:
      time.sleep(0.1)
      if GPIO.input(int(config_ini['GPIO']['RB'])) == GPIO.LOW:
#        if (st_bb == 0 and st_rb == 0):
        if (xgame.st_bb == 0 and xgame.st_rb == 0):
          log('rb1')
#          st_rb = 1
          xgame.st_rb = 1
          xgame.ct_rb = int(xgame.ct_rb) + 1
#          rbCount = int(rbCount) + 1
          xgame.rbCount = int(xgame.rbCount) + 1
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
  if GPIO.input(int(config_ini['GPIO']['BB'])) == GPIO.LOW:
    time.sleep(0.01)
    log('bb')
    rb_sig_timer
    if GPIO.input(int(config_ini['GPIO']['BB'])) == GPIO.LOW:
      time.sleep(0.1)
      if GPIO.input(int(config_ini['GPIO']['BB'])) == GPIO.LOW:
#        if (st_bb == 0 and st_rb == 0):
        if (xgame.st_bb == 0 and xgame.st_rb == 0):
          log('bb1')
#          st_rb = 1
          xgame.st_bb = 1
          xgame.ct_bb = int(xgame.ct_bb) + 1
#          bbCount = int(bbCount) + 1
          xgame.bbCount = int(xgame.bbCount) + 1
          #countUp(bwCount, 2) # bb:2
          bwCount = 0
  else:
    bb_sig_timer = 0
    log('bb0')

# --------------------------------
# 開始ポイントを設定
# --------------------------------
def set_point(n):
  global config_ini
  interval = float(config_ini['setting']['ssd_interval'])
  gpn = int(config_ini['GPIO']['CREDIT'])
  for i in range(n):
    GPIO.output(gpn, GPIO.HIGH)
    time.sleep(interval)
    GPIO.output(gpn, GPIO.LOW)
    time.sleep(interval)

# debug ###########################
def log(s):
  with open('/usr/share/webiopi/htdocs/api/debug.log', 'a') as f:
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + s, file=f)

# ################################
def destroy():
  global config_ini
  GPIO.remove_event_detect(int(config_ini['GPIO']['RB']))
  GPIO.remove_event_detect(int(config_ini['GPIO']['BB']))
#  GPIO.remove_event_detect(CREDIT_INC)
#  GPIO.remove_event_detect(STATUS_AP)
#  GPIO.remove_event_detect(STATUS_RB)
#  GPIO.remove_event_detect(STATUS_BB)
#  GPIO.remove_event_detect(STATUS_CT)
  GPIO.cleanup()


# --------------------------------
# API
# --------------------------------
@webiopi.macro
def start_game(gkey, point):
  global xgame
  set_point(int(point))
  xgame.start(gkey, point)
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
