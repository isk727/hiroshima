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
xgame = game.GameClass(config_ini['DEFAULT']['json_file'])

def setup():
  global config_ini
  GPIO.setmode(GPIO.BCM)
  GPIO.setup(int(config_ini['GPIO']['IN']), GPIO.IN)
  GPIO.setup(int(config_ini['GPIO']['OUT']), GPIO.IN)
  GPIO.setup(int(config_ini['GPIO']['RB']), GPIO.IN)
  GPIO.setup(int(config_ini['GPIO']['BB']), GPIO.IN)
  GPIO.setup(int(config_ini['GPIO']['PAYOUT1']), GPIO.OUT)
  GPIO.setup(int(config_ini['GPIO']['PAYOUT2']), GPIO.OUT)
  GPIO.setup(int(config_ini['GPIO']['CLEAR1']), GPIO.OUT)
  GPIO.setup(int(config_ini['GPIO']['CLEAR2']), GPIO.OUT)
  GPIO.setup(int(config_ini['GPIO']['CREDIT']), GPIO.OUT)
  GPIO.add_event_detect(int(config_ini['GPIO']['IN']), GPIO.RISING, bouncetime=5)
  GPIO.add_event_callback(int(config_ini['GPIO']['IN']), event_callback_credit_dec)
  GPIO.add_event_detect(int(config_ini['GPIO']['OUT']), GPIO.RISING, bouncetime=5)
  GPIO.add_event_callback(int(config_ini['GPIO']['OUT']), event_callback_credit_inc)
  GPIO.add_event_detect(int(config_ini['GPIO']['RB']), GPIO.BOTH, bouncetime=5)
  GPIO.add_event_callback(int(config_ini['GPIO']['RB']), event_callback_status_rb)
  GPIO.add_event_detect(int(config_ini['GPIO']['BB']), GPIO.BOTH, bouncetime=5)
  GPIO.add_event_callback(int(config_ini['GPIO']['BB']), event_callback_status_bb)

def loop():
  webiopi.sleep(0.1)

def event_callback_credit_dec(gpio_pin):
  global xgame
  time.sleep(0.05)
  if xgame.credit > 0:
    xgame.credit = int(xgame.credit) - 1
    xgame.point = int(xgame.point) - 1
    xgame.st_bw = int(xgame.st_bw) + 1
    xgame.st_rbw = int(xgame.st_rbw) + 1
    xgame.st_bbw = int(xgame.st_bbw) + 1
    if xgame.st_bw == 3:
      xgame.ct_bw = int(xgame.ct_bw) + 1
      xgame.st_bw = 0
    if xgame.st_rbw == 3:
      xgame.ct_rbw = int(xgame.ct_rbw) + 1
      xgame.st_rbw = 0
    if xgame.st_bbw == 3:
      xgame.ct_bbw = int(xgame.ct_bbw) + 1
      xgame.st_bbw = 0

def event_callback_credit_inc(gpio_pin):
  global xgame
  time.sleep(0.05)
  xgame.credit = int(xgame.credit) + 1
  xgame.point = int(xgame.point) + 1

def event_callback_status_rb(gpio_pin):
  global config_ini
  global xgame
  if GPIO.input(int(config_ini['GPIO']['RB'])) == GPIO.LOW:
    if (xgame.st_bb == 0 and xgame.st_rb == 0):
      xgame.last_bonus = 'RB'
      xgame.st_rb = 1
      xgame.ct_rb = int(xgame.ct_rb) + 1
      xgame.listw.append(xgame.ct_bw)
      xgame.listr.append(xgame.ct_rbw)
      log("listr.append " + str(xgame.ct_rbw))
      xgame.ct_bw = 0
      xgame.st_bw = 0
      xgame.ct_rbw = 0 # db
      xgame.st_rbw = 0 # db
  else:
    xgame.st_rb = 0
    xgame.st_rbw = 0

def event_callback_status_bb(gpio_pin):
  global config_ini
  global xgame
  if GPIO.input(int(config_ini['GPIO']['BB'])) == GPIO.LOW:
    if (xgame.st_bb == 0 and xgame.st_rb == 0):
      xgame.last_bonus = 'BB'
      xgame.st_bb = 1
      xgame.ct_bb = int(xgame.ct_bb) + 1
      xgame.listw.append(xgame.ct_bw)
      xgame.listb.append(xgame.ct_bbw)
      log("listb.append " + str(xgame.ct_bbw))
      xgame.ct_bw = 0
      xgame.st_bw = 0
      xgame.ct_bbw = 0 # db
      xgame.st_bbw = 0 # db
  else:
    xgame.st_bb = 0

# --------------------------------
# 開始ポイントを設定
# --------------------------------
def set_point(n):
  global config_ini
  interval = float(config_ini['DEFAULT']['ssd_interval'])
  gpn = int(config_ini['GPIO']['CREDIT'])
  for i in range(n):
    GPIO.output(gpn, GPIO.HIGH)
    time.sleep(interval)
    GPIO.output(gpn, GPIO.LOW)
    time.sleep(interval)

# --------------------------------
# 制御基板内のメモリー消去
# --------------------------------
def clear():
  global config_ini
  GPIO.output(int(config_ini['GPI0']['CLEAR1']), GPIO.HIGH)
  time.sleep(0.1)
  GPIO.output(int(config_ini['GPI0']['CLEAR2']), GPIO.HIGH)

# ################################
def destroy():
  global config_ini
  GPIO.remove_event_detect(int(config_ini['GPIO']['IN']))
  GPIO.remove_event_detect(int(config_ini['GPIO']['OUT']))
  GPIO.remove_event_detect(int(config_ini['GPIO']['RB']))
  GPIO.remove_event_detect(int(config_ini['GPIO']['BB']))
  GPIO.cleanup()

# debug ###########################
def log(s):
  with open('/usr/share/webiopi/htdocs/api/debug.log', 'a') as f:
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + s, file=f)

# --------------------------------
# WebIoPi Macro
# --------------------------------
@webiopi.macro
def start_game(gkey, point):
  global xgame
  set_point(int(point))
  xgame.start_game(gkey, point)
  xgame.json_dump()

@webiopi.macro
def check_game(gkey, point):
  global xgame
  xgame.check_game()
  xgame.json_dump()

@webiopi.macro
def stop_game(gkey, point):
  global xgame
  log("last_bonus=" + xgame.last_bonus + " ct_bw=" + str(xgame.ct_bw) + " ct_rbw=" + str(xgame.ct_rbw) + " ct_bbw=" + str(xgame.ct_bbw)) 
  log("last_bonus=" + xgame.last_bonus + " listr_size=" + str(len(xgame.listr)) + " listb_size=" + str(len(xgame.listb))) 
  xgame.stop_game()
  xgame.json_dump()
  clear()
