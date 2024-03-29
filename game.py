#import os
from datetime import datetime
import json

class GameClass:

#st_rb = 0
#rbCount = 0
#rb_sig_timer = 0

#st_bb = 0
#bbCount = 0
#bb_sig_timer = 0


  global config_ini
  global DNS
#  global gkey
#  gkey = ""
  global jsonkey
  global RP_ID
  global userid
  global sess
  global start_flg
  global ct_bb
  global ct_rb
  global start_at
  global stop_at
#  global json_file
#  json_file = ""

  def __init__(self, name, json_file):
    self.name = name
    self.json_file = json_file
#    self.name = config_ini['DEFAULT']['User']

  def __del__(self):
    print('インスタンスが破棄されました')
 
  def start(self, gkey):
    self.ct_rb = 0
    self.ct_bb = 0
    self.gkey = gkey
    self.start_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.stop_at = ""

  def stop(self, gkey):
    #self.ct_rb = 45
    #self.ct_bb = 12345
    self.gkey = gkey
    self.stop_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  def my_method(self):
#    print("クラスの名前は「" + self.name + "」です。" )
    return self.name

#  @property
  def json_dump(self):
#  def distance(self, fn):
#    cwd = os.getcwd()
    dict = {
      "gkey": self.gkey,
      "rb": self.ct_rb,
      "bb": self.ct_bb,
      "ccc": self.name,
#      "cwd": cwd,
      "jsonpath" : self.json_file,
      "start_at": self.start_at,
      "stop_at": self.stop_at,
#           datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
#    with open(self.json_file, 'w') as f:
    with open(self.json_file, 'w') as f:
#    with open('/usr/share/webiopi/htdocs/rec/game.json', 'w') as f:
#    with open('./rec/game.json', 'w') as f:
      json.dump(dict, f, ensure_ascii=False)

#  def log(self, s):
#    with open('/usr/share/webiopi/python/logs/log.txt', 'a') as f:
#      print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + s, file=f)
