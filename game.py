from datetime import datetime
import json

class GameClass:
  def __init__(self, json_file):
    self.json_file = json_file

  def __del__(self):
    print('instance has been destroyed.')
 
  def start(self, gkey, point):
    self.gkey = gkey
    self.start_pt = int(point)
    self.stop_pt = int(point)
    self.point = 0
    self.credit = int(point)

    self.ct_rb = 0
    self.st_rb = 0
    self.rbCount = 0
    self.rb_sig_timer = 0

    self.ct_bb = 0
    self.st_bb = 0
    self.bbCount = 0
    self.bb_sig_timer = 0
    
    self.ct_bw = 0
    self.bwCount = 0

    self.start_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    self.stop_at = ""

  def stop(self, gkey):
    self.stop_pt = self.credit
    self.stop_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

  def json_dump(self):
    dict = {
      "gkey": self.gkey,
      "start_pt": int(self.start_pt),
      "stop_pt": int(self.stop_pt),
      "credit": int(self.credit),
      "rb": int(self.ct_rb),
#      "rb2": int(self.rbCount),
      "bb": int(self.ct_bb),
      "bw": int(self.bwCount),
#      "credit": int(self.credit),
#      "point": int(self.point),
      "start_at": self.start_at,
      "stop_at": self.stop_at,
    }
    with open(self.json_file, 'w') as f:
      json.dump(dict, f, ensure_ascii=False)
