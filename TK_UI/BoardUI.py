import math
from Tkinter import *
from Controller import *
import sys
sys.path.append('../')
from Game import *
import os
import socket
import pickle

class UI:
  INIT_WIN_HEIGHT = 900
  INIT_WIN_WIDTH = 1200

  CANVAS_OPTIONS = { "height": INIT_WIN_HEIGHT, "width": INIT_WIN_WIDTH } 
  HEX_RADIUS = 32

  def __init__(self, major_size, minor_size, controller):
    self.major = major_size * 2 - 1
    self.minor = minor_size  / 2 + 1

    self.hex_radius = UI.HEX_RADIUS
    self.x_pad = self.hex_radius + 2
    self.y_pad = self.hex_radius + 3
 
    self.window = Tk()

    self.canvas = Canvas(self.window, **UI.CANVAS_OPTIONS)
    self.canvas.bind("<Button-1>", self.on_click)
    self.canvas.grid(column = 0, row = 0, sticky=(N, W))

    self.drawn = []

    self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.socket.bind(('', 50001))
    self.socket.listen(1)
    self.controller = controller
    self.pc = []
    self.pos_btns = []
    self.status_lbls = []
    self.grim = []

    self.window.createfilehandler(self.socket, tkinter.READABLE, self.outside)

    self.paintWindow()
    

  def outside(self, f, mask):
    conn, addr  = f.accept()
    pickled_game  = conn.recv(1024 * 16)
    
    game = pickle.loads(pickled_game)
    self.updateState(game)

  def updateState(self, game):
    for d in self.drawn:
      self.canvas.delete(d)
    for position, unit in game.board.grid.iteritems():
      vis_pos = self.backend_position_to_visual_position(position[0], position[1])
      self.drawn.extend(self.draw_char_on_visual_position(vis_pos[0], vis_pos[1], \
          unit.card.name, unit.get_curr_hp(), unit.get_curr_ammo(), unit.owner))
    
  def paintWindow(self):
    self.paintCanvas()
    self.paint_player()

  def paint_status(self):
    y = 400
    x = 30
    line_height = 120

    for i, p in self.controller.game.players.iteritems():
      lbl = Label(text=''.join(['Player: ', str(i), '\n', str(p)]), justify=LEFT)
      lbl_opts = { "window": lbl, "anchor": NW}
      self.status_lbls.append(self.canvas.create_window(x, y+(i*line_height), **lbl_opts))
    

  def paint_player(self):
    for placed in self.pc:
      self.canvas.delete(placed)
    self.pc = []

    for btn in self.pos_btns:
      self.canvas.delete(btn)
    self.pos_btns = []

    for lbl in self.status_lbls:
      self.canvas.delete(lbl)
    self.status_lbls = []

    for btn in self.grim:
      self.canvas.delete(btn)
    self.grim = []

    turn_text = ''.join(["Turn ", str(self.controller.game.turn)])
    turn_opts = { "window": Label(text=turn_text), "anchor":W }
    self.pc.append(self.canvas.create_window(30, 280, **turn_opts))

    label_text = ''.join(["Player ", str(self.controller.current_player_id)])
    label_opts = { "window": Label(text=label_text), "anchor": W }
    self.pc.append(self.canvas.create_window(30, 300, **label_opts)) 
      
    next_opts = { "window": Button(text=">", command=self.go_next), "anchor": W }
    self.pc.append(self.canvas.create_window(125, 300, **next_opts))
    
    self.paint_player_hand(self.controller.get_hand(self.controller.current_player_id))
    self.paint_status()
    self.paint_player_grimoire(self.controller.get_grimoire(self.controller.current_player_id))

  def go_next(self):
    self.controller.next_step()
    self.paint_player()

  def paint_player_grimoire(self, grim_list):
    x = 700
    y = 350

    height = 40

    for amount, name, cost in grim_list:
      btn_text = ''.join([str(amount), 'x ', name, ' $', str(cost)])
      buy_opts = { "window": Button(text=btn_text, \
          command=self.create_grim_buy_function(name)), \
          "anchor": W}

      self.grim.append(self.canvas.create_window(x, y, **buy_opts))
      y += height

  def buy_card(self, player_id, name):
    self.controller.buy_card(player_id, name)
    self.paint_player()

  def create_grim_buy_function(self, name):
    return lambda: self.buy_card(self.controller.current_player_id, name)

  def paint_player_hand(self, hand):
    x = 30
    y = 350
    width = 150
    height = 250
    xoffset = 100
    for card in hand:
      btn_text = card.name
      card_opts = { "window": Button(text=btn_text, \
          command=self.create_card_clicked_function(card)), "anchor":W }

      self.pc.append(self.canvas.create_window(x, y, **card_opts))
      x += xoffset
      
  def card_clicked(self, card):
    for btn in self.pos_btns:
      self.canvas.delete(btn)
    self.pos_btns = []

    pid = self.controller.current_player_id
    be_loc_list = self.controller.get_playable_locations(pid)

    for i, loc in enumerate(be_loc_list):
      btn = Button(text=str(i), command=self.create_place_card_function(card,pid,loc))
      btn_opts = { "window": btn }
      pixel = self.backend_position_to_center_pixel(loc[0], loc[1])
      
      self.pos_btns.append(self.canvas.create_window(pixel[0], pixel[1], **btn_opts))
      

  def create_place_card_function(self, card, pid, loc):
    return lambda: self.place_card(card, pid, loc)

  def place_card(self, card, player_id, location):
    self.controller.play_card(card.name, player_id, location)
    self.paint_player()

  def create_card_clicked_function(self, card):
    return lambda: self.card_clicked(card)  

  def paintCanvas(self):
    self.paintBoard()

  def paintBoard(self):
    def drawHexVerticalBoard(canvas, width, height, radius):
      def drawVerticalHexagon(canvas, centerx, centery, radius):
        yoffset = radius / 2
        xoffset = radius * math.sqrt(3) / 2 

        coords = [centerx, centery + radius, \
                  centerx + xoffset, centery + yoffset, \
                  centerx + xoffset, centery - yoffset, \
                  centerx, centery - radius, \
                  centerx - xoffset, centery - yoffset, \
                  centerx - xoffset, centery + yoffset] 

        options = {"fill": "grey", "outline": "black"}
       
        return canvas.create_polygon(*coords, **options)

      rowYOffset = radius * 3 
      colXOffset = radius * math.sqrt(3) / 2
      
      
      for i in xrange(width):
        for j in xrange(height):
          oddOffset = 0
          if i % 2 == 1:
            oddOffset = rowYOffset / 2
          if i % 2 == 1 and j == height - 1:
            continue
          drawVerticalHexagon(canvas, self.x_pad + (i * colXOffset), \
              self.y_pad + oddOffset + (j * rowYOffset), radius) 
      return 
    drawHexVerticalBoard(self.canvas, self.major, self.minor, self.hex_radius)
    #self.drawSquareCoords(self.canvas, self.major, self.minor, self.hex_radius)

    for ii in xrange(int(math.ceil(self.major / 2.0))):
      for jj in xrange(self.minor * 2 -1):
        if ii == int(math.ceil(self.major / 2.0)) - 1 and jj % 2 == 1:
          continue
        self.draw_coord_on_visual_position(ii, jj) 
         

    #for ii in xrange(3):#self.major):
      #for jj in xrange(3):#self.minor * 2 - 1):
        #self.fillHex(ii, jj)
        #self.fillCenter(ii, jj) 
    
  
  def on_click(self, event):
    click_position = self.pixel_to_visual_position(event.x, event.y)
    print "Click position: ", click_position[0], click_position[1]

    #self.draw_char_on_visual_position(4, 4, "H", 4, 20)

  def draw_coord_on_visual_position(self, x, y):
    p = self.visual_position_to_center_pixel(x, y)
    coord = self.visual_position_to_backend_position(x, y)
    coord_str = ''.join([str(coord[0]), ", ", str(coord[1])])
    
    text_opts = {"text": coord_str, "fill": "black", "font": ("ms serif", 10)}
    self.canvas.create_text(p[0], p[1] - 20, **text_opts)

    fe_coord = self.backend_position_to_visual_position(coord[0], coord[1])
    fe_coord_str = ''.join([str(fe_coord[0]), ", ", str(fe_coord[1])])
    text2_opts = {"text": fe_coord_str, "fill": "black", "font": ("ms serif", 10)}
    #self.canvas.create_text(p[0], p[1] + 20, **text2_opts)

  def draw_char_on_visual_position(self, x, y, text, ammo, life, owner):
    drawn = []
    t1_opts = {"text": text, "fill": "black", "font": ("ms serif", 14)}
    p = self.visual_position_to_center_pixel(x, y)
    drawn.append(self.canvas.create_text(p[0], p[1] - 9, **t1_opts))

    t2_opts = {"text": ammo, "fill": "black", "font": ("ms serif", 10)}
    drawn.append(self.canvas.create_text(p[0] - 11, p[1] + 10, **t2_opts))

    t3_opts = {"text": life, "fill": "black", "font": ("ms serif", 10)}
    drawn.append(self.canvas.create_text(p[0] + 12, p[1] + 10, **t3_opts))

    direct = '>'
    if owner.get_direction() == owner.FACING_LEFT:
      direct = '<'
    t4_opts = {"text": direct, "fill": "black", "font": ("ms serif", 8)}
    drawn.append(self.canvas.create_text(p[0] , p[1] + 20, **t4_opts))
    return drawn
    

  def pixel_to_visual_position(self, x, y):
    xside = self.hex_radius * math.sqrt(3)
    yside = self.hex_radius * 3 / 2

    xpad = self.x_pad - (xside / 2)
    ypad = self.y_pad  - (self.hex_radius / 4) - (yside / 2)

    visual_row = (y - ypad) // yside 
    visual_col_denom = (x - xpad) 
    if visual_row % 2 == 1:
      visual_col_denom -= xside / 2
    visual_col = visual_col_denom // xside 


    line_x = x - xpad - (visual_col * xside)
    line_y = y - ypad - (visual_row * yside)
    if visual_row % 2 == 1:
      line_x -= xside / 2
    line_x = line_x // 1

     
    if(line_y + (line_x  / math.sqrt(3)) < yside / 3 or #left triangle
       line_y - (line_x / math.sqrt(3)) <= yside / -3): #right triangle
      return self.pixel_to_visual_position(x, y - (yside / 4))

    return (visual_col, visual_row)

  def backend_position_to_visual_position(self, x, y):
    new_y = (self.minor - 1) * 2 - y 
    new_x = int(x + math.floor(y/2))
    return (new_x, new_y)

  def visual_position_to_backend_position(self, x, y):
    new_y = (self.minor - 1) * 2 - y
    new_x = int(x - math.floor(new_y/2))
    return (new_x, new_y)

  def visual_position_to_center_pixel(self, x, y):
    rowYOffset = self.hex_radius * 3 / 2
    colXOffset = self.hex_radius * math.sqrt(3) 

    oddOffset = 0
    if y % 2 == 1:
      oddOffset = colXOffset / 2

    x_pixel = self.x_pad + oddOffset + (x * colXOffset)
    y_pixel = self.y_pad + (y * rowYOffset) 
    return (x_pixel, y_pixel)

  def backend_position_to_center_pixel(self, x, y):
    visual_position = self.backend_position_to_visual_position(x, y)
    pixel = self.visual_position_to_center_pixel(visual_position[0], visual_position[1])
  
    return pixel
    

  def translateToBackendPosition(self, x_from_left, y_from_top):
    x = x_from_left
    y = ((self.minor - 1) * 2) - y_from_top
    return (x, y)
  
  def loop(self):
    self.window.mainloop()

  #test functions
  def drawSquareCoords(self, canvas, width, height, hex_radius):
    def drawRect(canvas, centerx, centery, xside, yside):
      yoffset = yside / 2
      xoffset = xside / 2 

      coords = [centerx - xoffset, centery - yoffset, \
                centerx + xoffset, centery - yoffset, \
                centerx + xoffset, centery + yoffset, \
                centerx - xoffset, centery + yoffset] 

      options = {"fill": "", "outline": "red"}
       
      return canvas.create_polygon(*coords, **options)
    
    yside = hex_radius * 3 / 2
    xside = hex_radius * math.sqrt(3)

    rowYOffset = hex_radius * 3 
    colXOffset = hex_radius * math.sqrt(3) / 2

    for i in xrange(width + 1):
      for j in xrange(height):
        oddOffset = 0
        if i % 2 == 1:
          oddOffset = rowYOffset / 2
        drawRect(canvas, self.x_pad + (i * colXOffset), \
            self.y_pad - (self.hex_radius / 4) + \
            oddOffset + (j * rowYOffset), xside, yside) 
         

  def fillHex(self, x, y):
    opt = [[{"fill": "blue" }, {"fill": "green"}], [{"fill": "orange"}, {"fill": "yellow"}]]
    for i in xrange(UI.INIT_WIN_WIDTH):
      jstart = None
      for j in xrange(UI.INIT_WIN_HEIGHT):
        inn = self.pixel_to_visual_position(i, j) == (x, y)
        if inn and jstart == None:
          jstart = j
        jend = j
        if jstart != None and not inn:
          break
      if jstart != None:
        self.canvas.create_line(i, jstart, i, jend, **(opt[x%2][y%2]))
       
  def fillCenter(self, x, y):
    opt = {"fill": "black"}
    pixel = self.visual_position_to_center_pixel(x, y)
    self.canvas.create_line(pixel[0], pixel[1], pixel[0] + 1, pixel[1], **opt)



if __name__ == "__main__":
  con = Controller(None, Game(input_type=''))
  ui = UI(BOARD_LENGTH, BOARD_WIDTH, con)
  ui.loop()
