#minesweeper

from uagame import Window
import pygame
from pygame.locals import *
import random

# User-defined classes

# An object in this class represents a complete game.
class Game:

  
   def __init__(self, window):
     
      '''
      Initialize a Game.
      Arg: self, window
      Returns: none
      self - the Game to be initialized
      window - the uagame window object
      '''
     
      self.window = window
      Box.set_window(window) # call box class function to create a new window
      self.close_clicked = True
      self.continue_game = True
      self.board_size = 8
      self.mines = 20
      self.board = []
      self.ordered_list = [] # stores the coordinates of all boxes on the game board
      self.create_board()
      self.new_list_X =[] # stores the list of randomly generated mines (i.e. X)
      self.new_list_O =[] # stores the list of numbers representing the number of mines in the surrounding 8 boxes
      random.shuffle(self.ordered_list)
      self.create_new_list()
      self.total_mines=0
      self.timer=0
      Box.coord_list(self.new_list_X, self.new_list_O)
    
   def create_new_list(self):
      '''
      Creates the list after shuffling.
      Arg: self - the Game itself
      Returns: none
      '''     
     
      for i in range(0, self.mines):
         self.new_list_X.append(self.ordered_list[i])
      for j in range(self.mines, len(self.ordered_list)):
         self.new_list_O.append(self.ordered_list[j])
    

   def create_board(self):
      '''
      Create the game board.
      Arg: self - the Game whose board is created
      Returns: none
      Each row is appended to the board to form the game board.
      '''
     
      for row_index in range(0, self.board_size):
         row = self.create_row(row_index)
         self.board.append(row)
    

  
   def create_row(self, row_index):
      '''
      Create one row of the board.
      Arg: self - the Game whose board row is being created
           row_index - the int index of the row starting at 0
      Returns: row - one row of the board
  
      This function first calculates the width and height of the row,
      then it finds the x and y coordinate of each box in the row.
      Finally it appends each box onto the row, then one row is created
      as such and returned to the create_board function
      '''
     
      row = []
      # plus 3 to fit each row in the middle of the window
      width = self.window.get_width() // (self.board_size+3)
      height = self.window.get_height() // (self.board_size+3)
      y = 150+row_index * height # get y coordinate
      for col_index in range(0,  self.board_size):
         x = 135+col_index * width  # get x coordinate
         # store the coordinate (i.e. upper-left corner) of the box in ordered_list
         coord=(x,y)   
         self.ordered_list.append(coord)
         # create the box and append it to form the row
         box = Box(x, y, width, height) 
         row.append(box)
      return row


  
   def play_game(self):
     
      '''
      Play the game until the player presses the close box.
      Arg: self - the Game that should be continued or not.
      Returns: none
      Once the close button is clicked, make_grid function is called
      to display the game board
      '''
     
      while self.close_clicked:  # until player clicks close box
         self.click_event()
         self.make_grid()
         if self.continue_game:
            self.update()


   def click_event(self):
      '''
      Handle each user event by changing the game state appropriately.
      Arg: self - the Game whose events will be handled
      Returns: none
      '''     

      event = pygame.event.poll()  # get one event at a time
      # checks if the game is over
      if event.type == QUIT:
         self.close_clicked = False
      elif event.type == MOUSEBUTTONUP and self.continue_game:
         self.click_mouse_up_event(event)
 

   def click_mouse_up_event(self, event):
      '''
      Respond to the player releasing the mouse button by
      taking appropriate actions.
      Arg: self - the Game where the mouse up occurred
      event - the pygame.event.Event object to be handled
      '''
     
      for row in self.board:
         for box in row:
            valid_selection=box.select(event.pos) 
            if valid_selection:
               self.continue_game=False
      

            
   def make_grid(self):
      '''
      Draw all game objects.
      Arg: self - the Game to be drawn
      Returns: none
      This function calls draw_num_mines function to display the number of mines around
      the selected box, then it calls draw_timer to display the current time countdown.
      '''
     
      for row in self.board:
         for box in row:
            box.draw()
      self.draw_num_mines()
      self.draw_timer()
      box.draw_mines()
      self.window.update()
  

  
   def update(self):
      '''
      This function updates the timer as long as the user is still playing the game.
      Arg: self - the Game to be updated
      Returns: none
      '''   
     
      # Update the game objects.
      self.timer = pygame.time.get_ticks()//1050

  
   def draw_num_mines(self):
      '''
      This function displayes the total number of mines on the upper left corner of the window.
      Arg: self - the Game window
      Returns: none
      '''  
     
      self.total_mines= 'Mines: ' + str(self.mines)
      self.window.set_font_color('green')
      self.window.set_font_size(60)
      # display the number of surrounding mines on the selected box
      self.window.draw_string(str(self.total_mines),self.window.get_width()-self.
         window.get_string_width(str(self.total_mines))*2,50)
  


   def draw_timer(self):
      '''
      This function draw the timer onto the window.
      Arg: self - the Game window
      Returns: none
      '''
     
      self.window.set_font_color('green')
      self.window.set_font_size(60)
      self.window.draw_string('Timer: '+str(self.timer),0,50)
   

class Box:
  
   # An object in this class represents a Rectangular box
   # initializes the class attributes that are common to all boxes
  
   fg_color = pygame.Color('blue')
   border_width = 8
   font_size = 40
   mine_counter = 0
   position=(0,0)
   content = ''
   new_list_X = []
   new_list_O = []
   window = None
 

   @classmethod
   def set_window(cls, window):
      # remember the window
      cls.window = window
    
   @classmethod 
   def coord_list(cls, new_list_X, new_list_O):
      #remembers the new_list_X, new_list_O from Game class
      cls.new_list_X= new_list_X
      cls.new_list_O= new_list_O
    
   def __init__(self, x, y, width, height):
      '''
      Args:
      -x is the int x coord of the upper left corner
      -y is the int y coord of the upper left corner
      -width is the int width of the box
      -height is the int height of the box
      '''

      self.rectangle = pygame.Rect(x, y, width, height)

   def select(self, mouse_position):
      '''
      A position was selected. If the position is in the Box
      and the Box coordinate is in new_list_X, then update the Box content to 'X'
      else update the box content to the number of mines around the box
      -self is the Box
      -position is the selected location (tuple)
      -content is the new str contents of the box
     
      Args: None
      Returns: Nothing
      '''
  
      position=(0,0)
      mine_clicked=False
      if self.rectangle.collidepoint(mouse_position):
         position=(self.rectangle.left, self.rectangle.top)
         mine_counter=self.count_mines(position)
         num_of_mines = str(mine_counter)
         if position in Box.new_list_X :
            Box.content = 'X'
            mine_clicked=True
         elif position not in Box.new_list_X :
            Box.content = num_of_mines
            Box.position = mouse_position       
      return(mine_clicked) 
  
   def count_mines(self, position):
      '''
      Given a coordinate position(tuple), check whether there are any mines
      in the eight surrounding boxes
     
      Args: a coordinate (tuple)
      Returns: Nothing
      '''
     
      mine_counter=0
      if position not in self.new_list_X:
         width = 90
         height = 72
         if((position[0]+width,position[1]) in self.new_list_X):
            mine_counter+=1
         if((position[0]-width,position[1]) in self.new_list_X):
            mine_counter+=1
         if((position[0],position[1]+height) in self.new_list_X):
            mine_counter+=1
         if((position[0],position[1]-height) in self.new_list_X):
            mine_counter+=1
         if((position[0]-width,position[1]-height) in self.new_list_X):
            mine_counter+=1
         if((position[0]-width,position[1]+height) in self.new_list_X):
            mine_counter+=1
         if((position[0]+width,position[1]-height) in self.new_list_X):
            mine_counter+=1
         if((position[0]+width,position[1]+height) in self.new_list_X):
            mine_counter+=1
      return(mine_counter)   

   def draw(self):
      '''
      checks if a box has been clicked on
      if it has, then chekc whether the position is in the list of mines
      it is not, then it draws the number of mines around the box in the box
      Args: None
      Returns: Nothing
      '''
     
      self.surface=self.window.get_surface()
      pygame.draw.rect(self.surface, pygame.Color('blue'), self.rectangle, Box.border_width) 
      if self.rectangle.collidepoint(Box.position):
         position =(self.rectangle.left, self.rectangle.top)
         if(Box.content!='X'):
            content_width= Box.window.get_string_width(Box.content)
            content_height= Box.window.get_font_height()        
            content_x = position[0] + (self.rectangle.width - content_width) // 2
            content_y = position[1] +  (self.rectangle.height - content_height) // 2
            Box.window.draw_string(Box.content, content_x, content_y)
     
   def draw_mines(self):
      '''
      check if the box content is 'X'
      if it is, then it draws an 'X' in all the coordinates in the new_list_X
      Args: None
      Returns: Nothing
      '''
     
      content_width= Box.window.get_string_width(Box.content)
      content_height= Box.window.get_font_height()
      if(Box.content=='X'):
         for i in range (len(Box.new_list_X)):
            content_x = Box.new_list_X[i][0] + (self.rectangle.width - content_width) // 2
            content_y = Box.new_list_X[i][1] + (self.rectangle.height - content_height) // 2
            Box.window.draw_string(Box.content, content_x, content_y)
           

if __name__=="__main__":
  
   # create a window
   window = Window('Minesweeper', 1000, 800)
  
   # declare an object of Game class
   game = Game(window)
  
   # call to play function of Game class
   game.play_game()
  
   window.close() 