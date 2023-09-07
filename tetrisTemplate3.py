#########################################
# Programmer: Ben Sadeh
# Date: 21/11/2021
# File Name: tetrisClasses3.py
# Description: Tetris Game
#########################################
import pygame

BLACK     = (  0,  0,  0)                       
RED         = (255,  0,  0)                     
GREEN    = (  0,255,  0)                     
BLUE       = (  0,  0,255)                     
ORANGE = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA  = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255) 
COLOURS  = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]
CLRNames = ['black','red','green','blue','orange','cyan','magenta','yellow','white']
figures        = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]

class Block(object):                    
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):                  
        return '('+str(self.col)+','+str(self.row)+') '+CLRNames[self.clr]


    def __eq__(self, other):
        if self.row==other.row and self.col==other.col:
            return True
        return False

    def draw(self, surface, gridsize=20):                     
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 0)
        pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 1)

    def moveRight(self):                
        self.col = self.col + 1   
#######################################################################################################################
# 1. Delete the move_left, move_right  in class Block since they are no longer used  
#######################################################################################################################        
    def moveLeft(self):                
        self.col = self.col - 1
        
    def moveDown(self):                
        self.row = self.row + 1 
        
    def moveUp(self):                  
        self.row = self.row - 1  

#---------------------------------------#
class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0                          
        self.blocks = [Block()]*blocksNo      
        self._colOffsets = [0]*blocksNo  
        self._rowOffsets = [0]*blocksNo  

    def _update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i] 
            blockROW = self.row+self._rowOffsets[i] 
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)

    def collides(self, other):
        for block in self.blocks:
            for obstacle in other.blocks:
                if block==obstacle:
                    return True
                
        return False 
            
    def append(self, other): 
        """ Append all blocks from another cluster to this one.
        """
###########################################################################################
# 9.  Add code here that appends the blocks of the other object to the self.blocks list.
#     Use a for loop to take each individual block from the other.blocks list 
############################################################################################
        for block in other.blocks:
            self.blocks.append(block)

#---------------------------------------#
class Obstacles(Cluster):
    """ Collection of tetrominoe blocks on the playing field, left from previous shapes.
        
    """        
    def __init__(self, col = 0, row = 0, blocksNo = 0):
        Cluster.__init__(self, col, row, blocksNo)      # initially the playing field is empty(no shapes are left inside the field)

    def show(self):
        print("\nObstacle: ")
        for block in self.blocks:
            print (block)

    def findFullRows(self, top, bottom, columns):
        fullRows = []
        rows = []
        for block in self.blocks:                       
            rows.append(block.row)                      # make a list with only the row numbers of all blocks
            
        for row in range(top, bottom):                  # starting from the top (row 0), and down to the bottom
            if rows.count(row) == columns:           # if the number of blocks with certain row number
                fullRows.append(row)                     # equals to the number of columns -> the row is full
        return fullRows                                       # return a list with the full rows' numbers


    def removeFullRows(self, fullRows):
        for row in fullRows:                            # for each full row, STARTING FROM THE TOP (fullRows are in order)
            for i in reversed(range(len(self.blocks))): # check all obstacle blocks in REVERSE ORDER,
                                                                 # so when popping them the index doesn't go out of range !!!
                if self.blocks[i].row == row:
                    self.blocks.pop(i)                   # remove each block that is on this row
                elif self.blocks[i].row < row:
                    self.blocks[i].moveDown()    # move down each block that is above this row
   
#---------------------------------------#
class Shape(Cluster):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        Cluster.__init__(self, col, row, 4)
        self.clr = clr

        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1] 
        self._rowOffsets = [-1,-1, 0, 0] 
        self._rotate() 
        
    def __str__(self):                  
        return figures[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]


    def _rotate(self):
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]] 
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]]       
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]] 
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]] 
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]] 
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]]             
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
            _colOffsets = [[-1, 1, 1,-1], [-1, 1, 1,-1], [-1, 1, 1,-1], [-1, 1, 1,-1]] 
            _rowOffsets = [[-1,-1, 1, 1], [-1,-1, 1, 1], [-1,-1, 1, 1], [-1,-1, 1, 1]] 
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]] 
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]]            
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]] 
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]] 
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]] 
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]] 
        self._colOffsets = _colOffsets[self._rot] 
        self._rowOffsets = _rowOffsets[self._rot] 
        self._update() 

    def moveLeft(self):                
        self.col = self.col - 1                   
        self._update() 
        
    def moveRight(self):               
        self.col = self.col + 1                   
        self._update() 
        
    def moveDown(self):                
        self.row = self.row + 1                   
        self._update() 
        
    def moveUp(self):                  
        self.row = self.row - 1                   
        self._update() 

    def rotateClkwise(self):
        self._rot=(self._rot+1)%4
        self._rotate()
###################################################################################################################
# 5.  Add code here that rotates the shape one step clockwise. Use the rotation section from the previous template
###################################################################################################################

    def rotateCntclkwise(self):
       self._rot=(self._rot-1)%4
       self._rotate()
##########################################################################################################################
# 6.  Add code here that rotates the shape one step counterclockwise. Use the rotation section from the previous template
##########################################################################################################################


#---------------------------------------#
class Floor(Cluster):
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i  
        self._update()         
            
#---------------------------------------#
class Wall(Cluster):
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i 
        self._update() 



#Start of template
from random import randint
pygame.init()

HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))
GREY = (192,192,192)

#---------------------------------------#
COLUMNS = 14                      #
ROWS = 22                            # 
LEFT = 9                                # 
RIGHT = LEFT + COLUMNS   # 
MIDDLE = LEFT + COLUMNS//2  #
TOP = 1                                  #
FLOOR = TOP + ROWS         #
#---------------------------------------#

#---------------------------------------#
#   functions                            #
#---------------------------------------#
def redrawScreen():               
    screen.fill(BLACK)
    tetra.draw(screen, GRIDSIZE)
    floor.draw(screen, GRIDSIZE)
    leftWall.draw(screen, GRIDSIZE)
    rightWall.draw(screen, GRIDSIZE)
    obstacle.draw(screen,GRIDSIZE)
#####################################################################################################
# 11.  Draw the object obstacles on the screen
#####################################################################################################
    pygame.display.update() 
        
#---------------------------------------#
#   main program                    #
#---------------------------------------#    
shapeNo = randint(1,7)      
tetra = Shape(MIDDLE,1,shapeNo)
floor = Floor(LEFT,FLOOR,COLUMNS)
ceiling = Floor(LEFT,TOP,COLUMNS)
leftWall = Wall(LEFT-1, TOP, ROWS)
rightWall = Wall(RIGHT, TOP, ROWS)
obstacle=Obstacles(LEFT,FLOOR)
#####################################################################################################
# 10.  Create an object obstacles of Obstacles class. Give it two parameters only - LEFT & FLOOR
#####################################################################################################
inPlay = True                                         

while inPlay:               
    for event in pygame.event.get():
        if event.type == pygame.QUIT:         
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
#####################################################################################################
# 7.  Modify the code below, so it calls rotateClkwise() method and it doesn't access _rot private variable
#     and the rotation method. Use the code below in the class template to write the new rotation methods
#####################################################################################################                     
                tetra.rotateClkwise()
                if tetra.collides(leftWall) or tetra.collides(rightWall) or tetra.collides(obstacle) or tetra.collides(floor):
                    tetra.rotateCntclkwise()
#####################################################################################################
# 8.  Modify the code so it uses rotateCntclkwise() method when collision is detected during rotation
#####################################################################################################
            if event.key == pygame.K_LEFT:
                tetra.moveLeft()
                if tetra.collides(leftWall) or tetra.collides(obstacle):
                    tetra.moveRight()
            if event.key == pygame.K_RIGHT:
                tetra.moveRight()
                if tetra.collides(rightWall) or tetra.collides(obstacle):
                    tetra.moveLeft()
            if event.key == pygame.K_SPACE:
                while not tetra.collides(floor) and not tetra.collides(obstacle):
                    tetra.moveDown()
                tetra.moveUp()
            
    tetra.moveDown()
    if tetra.collides(floor) or tetra.collides(obstacle):
        tetra.moveUp()
        obstacle.append(tetra)
        shapeNo=randint(1,7)
        tetra=Shape(MIDDLE,1,shapeNo)
        obstacle.show()
        fullRows=obstacle.findFullRows(TOP,FLOOR,COLUMNS)
        score=100*len(fullRows)
        #print("full rows: ".fullRows,score)
        obstacle.removeFullRows(fullRows)

    redrawScreen()
    pygame.time.delay(250)
    
pygame.quit()
    
