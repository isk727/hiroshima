from datetime import datetime
import json

class GameClass:
  def __init__(self, json_file):
    self.json_file = json_file

  def __del__(self):
    print('instance has been destroyed.')

  def start_game(self, gkey, point):
    self.gkey = gkey
    self.start_pt = int(point)
    self.stop_pt = int(point)
    self.point = 0
    self.credit = int(point)
    self.ct_rb = 0
    self.st_rb = 0
    self.ct_bb = 0
    self.st_bb = 0
    self.ct_bw = 0
    self.st_bw = 0
    self.ct_rbw = 0
    self.st_rbw = 0
    self.ct_bbw = 0
    self.st_bbw = 0
    self.listw = []
    self.listr = []
    self.listb = []
    self.bw_rb = ''
    self.bw_bb = ''
    self.last_bonus = ''
    self.start_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.stop_at = ""

  def check_game(self):
    self.listw.append(self.ct_bw)
    self.bw_rb = ','.join(map(str, self.listr))
    self.bw_bb = ','.join(map(str, self.listb))
    self.stop_pt = self.credit
    self.stop_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  def stop_game(self):
    self.listw.append(self.ct_bw)
    self.listr.append(self.ct_rbw)
    self.listb.append(self.ct_bbw)
    self.bw_rb = ','.join(map(str, self.listr))
    self.bw_bb = ','.join(map(str, self.listb))
    self.stop_pt = self.credit
    self.stop_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  def json_dump(self):
    dict = {
      "gkey": self.gkey,
      "start_pt": int(self.start_pt),
      "stop_pt": int(self.stop_pt),
      "credit": int(self.credit),
      "rb": int(self.ct_rb),
      "bb": int(self.ct_bb),
      "bw": int(self.ct_bw),
      "rbw": int(self.ct_rbw),
      "bbw": int(self.ct_bbw),
      "bw_rb": self.bw_rb,
      "bw_bb": self.bw_bb,
      "start_at": self.start_at,
      "stop_at": self.stop_at,
    }
    with open(self.json_file, 'w') as f:
      json.dump(dict, f, ensure_ascii=False)

  def log(self, s):
    with open('/usr/share/webiopi/htdocs/api/debug2.log', 'a') as f:
      print(datetime.now().strftime("%Y-%m-%d %H:%M:%S") + ' ' + s, file=f)

