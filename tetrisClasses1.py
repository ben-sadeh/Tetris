#########################################
# Programmer: Ben Sadeh
# Date: 17/11/2021
# File Name: tetrisClasses1.py
# Description: Tetris classes
#########################################
import pygame

BLACK     = (  0,  0,  0)                       
RED         = (255,  0,  0)                     
GREEN    = (  0,255,  0)                     
BLUE       = (  0,  0,255)                     
ORANGE = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA= (255,  0,255)                   
YELLOW = (255,255,  0)
WHITE    = (255,255,255) 
COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]
CLRNames  = ['black','red','green','blue','orange','cyan','magenta','yellow','white']
figures    = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]

class Block(object):                    
    """ A square - basic building block
        data:                    behaviour:
            col - column        move left/right/up/down
            row - row             draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):                  
        return '('+str(self.col)+','+str(self.row)+') '+CLRNames[self.clr]

    def draw(self, surface, gridsize=20):                     
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 0)
        
###################################################################
# 1. add here your code that draws a white frame around the block
###################################################################

    def moveLeft(self):                
        self.col = self.col - 1    
        
    def moveRight(self):
########################################################################
# 2. add here your code that moves the block to the right and remove the pass
########################################################################        
        pass

    def moveDown(self):                
########################################################################
# 3. add here your code that moves the block down and remove the pass
########################################################################   
        pass

    def moveUp(self):                  
#######################################################################
# 4.add here your code that moves the block up and remove the pass
#######################################################################
        pass
#---------------------------------------#
class Shape(object):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
        auxiliary data:
            blocksXoffset - list of horizontal offsets for each block, in reference to the anchor block
            blocksYoffset - list of vertical offsets for each block, in reference to the anchor block
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col         
        self.row = row
        self.clr = clr    
        self.rot = 1
        self.blocks = [Block()]*4        
        self.blocksXoffset = [-1, 0, 0, 1] 
        self.blocksYoffset = [-1,-1, 0, 0] 
        self.rotate()
        
    def __str__(self):                  
        return figures[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLRNames[self.clr]
    
    def rotate(self):
        """ offsets are assigned starting from the farthest block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            blocksXoffset = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]]
            blocksYoffset = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]]        
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            blocksXoffset = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]]
            blocksYoffset = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]]
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            blocksXoffset = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]]
            blocksYoffset = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]]            
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
#########################################################################################
# 5. fix the offsets for the L-shape below:
#########################################################################################                         
            blocksXoffset = [[-1, 0, 0, 0], [1, 1, 0,-1], [1, 0, 0, 0], [-1, 1, 0,-1]]
            blocksYoffset = [[-1,-1, 0, 1], [-1,0, 0, 0], [1,1, 0, -1], [1,0, 0, 0]]
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            blocksXoffset = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]]
            blocksYoffset = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]]            
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            blocksXoffset = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]]
            blocksYoffset = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]]
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            blocksXoffset = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]]
            blocksYoffset = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]]
        self.blocksXoffset = blocksXoffset[self.rot]
        self.blocksYoffset = blocksYoffset[self.rot]
        self.update()
        
    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)

    def moveLeft(self):                
        ##########################################################
        # 6. add here your code that moves the block to the left 
        #########################################################                   
        self.update()
        
    def moveRight(self):               
        ##########################################################
        # 7. add here your code that moves the block to the right 
        ##########################################################                     
        self.update()
        
    def moveDown(self):                
        ####################################################
        # 8. add here your code that moves the block down
        ####################################################               
        self.update()
        
    def moveUp(self):                  
        ################################################
        # 9. add here your code that moves the block up
        ################################################                   
        self.update()
            
    def update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col+self.blocksXoffset[i]
            blockROW = self.row+self.blocksYoffset[i]
            blockCLR = self.clr
            self.blocks[i]= Block(blockCOL, blockROW, blockCLR)

from random import randint
import pygame
pygame.init()

HEIGHT = 600
WIDTH  = 800
GRIDSIZE = HEIGHT//24
screen=pygame.display.set_mode((WIDTH,HEIGHT))

#---------------------------------------#
#   functions                           #
#---------------------------------------#
def redrawScreen():               
    screen.fill(BLACK)
    drawGrid()
    tetra.draw(screen, GRIDSIZE)
##########################################################################
# 10. remove the line below, after you have added white frames to the blocks
##########################################################################  
    pygame.display.update() 


def drawGrid():
    """ Draw horisontal and vertical lines on the entire game window.
        Space between the lines is GRIDSIZE.
    """
    for x in range(0, WIDTH, GRIDSIZE):
        pygame.draw.line(screen, WHITE, (x,0),(x,HEIGHT))
    for y in range(0, HEIGHT, GRIDSIZE):
        pygame.draw.line(screen, WHITE, (0,y),(WIDTH,y))
       
##################################################################################
# 11. add here your code that draws the grid and remove the pass ( use for loops)
#     Code for drawing a line:  pygame.draw.line(surface, color, (startX,startY),(endX,endY))
#########################################################################
#---------------------------------------#
#   main program                        #
#---------------------------------------#    
shapeNo = randint(1,7)      
tetra = Shape(1,1,shapeNo)
inPlay = True                                         

while inPlay:               
    for event in pygame.event.get():
        if event.type == pygame.QUIT:         
            inPlay = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                tetra.rot = (tetra.rot + 1)%4  # changes the possition of the shape from 0,1,2,3 according to the indexes
                tetra.rotate()                        # blocksXoffset = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]]
            if event.key == pygame.K_LEFT:
                tetra.moveLeft()
            if event.key == pygame.K_RIGHT:
                tetra.moveRight()
            if event.key == pygame.K_DOWN:
                tetra.moveDown()                
            if event.key == pygame.K_SPACE:

                tetra.clr = tetra.clr %7 +1  # change the shape from 1 to 7 according to the indexes
                                                           # figures= [None ,'Z','S','J','L','I','T','O',None]
                tetra.rotate()              # after chaging the shape/clr the tetra must be updated and rotated: 

# update the screen     
    redrawScreen()
    pygame.time.delay(30)
    
pygame.quit()
