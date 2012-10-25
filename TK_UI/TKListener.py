

import socket

class TKListener:
  def __init__(self):
    pass

  def state_changed(self, game_dump):
    try:
      s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.connect(('localhost', 50001))
      s.sendall(game_dump)
      s.close()
    except:
      pass

  def __getstate__(self):
    return None 
