'''This file holds the code for the game and all of it's features'''


import math, copy, random
import numpy as np
from cmu_112_graphics import *
import tkinter as tk
import game_test

##########################################
# introScrene1 Mode
##########################################
class Matrix:
    def __init__(self, proj):
 
        self.proj = proj 
def introScrene1_redrawAll(app, canvas):
    font = 'Arial 26 bold'
    canvas.create_rectangle(0,0,app.width, app.height, fill = 'yellow')
    canvas.create_text(app.width/2, 150, text='Welcome to Pac-Pac!',
                       font=font, fill='black')

    canvas.create_text(app.width/2, 250, 
    text='''Click on the rotating cube to start!''', font=font, fill='black')
    game_test.redrawAll(app,canvas)
    

def introScrene1_mousePressed(app, event):
    if ((  (app.width/2)+30 > event.x and event.x > (app.width/2)-60)  and
        ((app.height*.45)-70 < event.y and event.y < (app.height*.45)+150)):
            app.mode = 'GameExpo1'



def introScrene1_timerFired(app):
        
        matProj = Matrix(np.array( [[0.0,0.0,0.0,0.0],
                                    [0.0,0.0,0.0,0.0],
                                    [0.0,0.0,0.0,0.0],
                                    [0.0,0.0,0.0,0.0],]))
        matProj.proj[0][0] = app.aspectRatio * app.fFovRad
        matProj.proj[1][1] = app.fFovRad
        matProj.proj[2][2] = app.fFar/ (app.fFar-app.fNear)
        matProj.proj[3][2] = ((-app.fFar* app.fNear)/ (app.fFar-app.fNear))
        matProj.proj[2][3] = 1.0
        matProj.proj[3][3] = 0.0
       
        app.mesh = game_test.multiplyMatrix(app, matProj)    
    
        #updates the theta in the rotation matrices by .05 radians per call
        app.theta+=.05
 
        game_test.rotateMesh(app)
 
        game_test.ScaleTri(app)
##########################################
# GameExpo1 screen
##########################################
def GameExpo1_redrawAll(app, canvas):

    canvas.create_rectangle(0,0,app.width, app.height, fill = 'red')

    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, 
    text=''' Pac-Pac is little special, so there will be an explanation of some special rules ''', 
                       font=font, fill='black')
    canvas.create_text(app.width/2, 350, text='Press the Right Arrow Key to learn more!',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 550, text='Press the Left Arrow Key to return to a previous screen!',
                       font=font, fill='black')
def GameExpo1_keyPressed(app, event):
    if (event.key == "Left"):
        app.mode = 'introScrene1'
    if event.key == "Right":
        app.mode = 'GameExpo2'
##########################################
# GameExpo2 Mode
##########################################
def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'
def GameExpo2_redrawAll(app, canvas):
    pink = rgbString(255,184,255)

    canvas.create_rectangle(0,0,app.width, app.height, fill = pink)

    font = 'Arial 26 bold'

    canvas.create_text(app.width/2, 150, 
    text='The main twist of this Pac-Pac is that you get to make the map!',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 250, 
    text="There's only one rule: you can only fill half the board with the walls you raise",
                       font=font, fill='black')
    canvas.create_text(app.width/2, 350, 
    text='Other than that, go crazy!',
                       font=font, fill='black')
def GameExpo2_keyPressed(app, event):
    if (event.key == "Left"):
        app.mode = 'GameExpo1'
    if (event.key == "Right"):
        app.mode = 'GameExpo3'
##########################################
# GameExpo3
##########################################


def rgbString(r, g, b):
    # Don't worry about the :02x part, but for the curious,
    # it says to use hex (base 16) with two digits.
    return f'#{r:02x}{g:02x}{b:02x}'
def GameExpo3_redrawAll(app, canvas):
    blue = rgbString(0,255,255)

    canvas.create_rectangle(0,0,app.width, app.height, fill = blue)

    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, 
    text='This new twist does also add some important gameplay...',
                       font=font, fill='black')
    canvas.create_text(app.width/2, 350, 
    text="1:If you get eat more that 15 pellets during gameplay, you can recreate the map on the fly!",
                       font=font, fill='black')
 

    canvas.create_text(app.width/2, 450, 
    text="2: If you try to enclose a pellet in all walls, the pellet might spawn in it" ,
        font = font, fill = 'black')


    canvas.create_text(app.width/2, 550, 
    text = "3: not all walls you raise will help you, only ghosts can travel through diagonal walls!",
        font = font, fill = 'black')

    canvas.create_text(app.width/2, 750, 
    text='''with all that out of the way, lets make the board, shall we?''',
                       font=font, fill='black')
def GameExpo3_keyPressed(app, event):
    if (event.key == "Right"):
        app.mode = 'boardCreation'
    if (event.key == "Left"):
        app.mode = 'GameExpo2'


##########################################
# boardCreation
##########################################


def boardCreation_keyPressed(app, event):
    if (event.key == "Left"):
        app.mode = 'GameExpo3'
    if(event.key == "Enter"):
        createPathGraph(app)
        app.mode = 'Game'
#linets 172-196 were from 15-112 website: https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

def pointInGrid(app, x, y):
    
    # return True if (x, y) is inside the grid defined by app.
    return ((app.margin <= x <= app.width-app.margin) and
            (app.margin <= y <= app.height-app.margin))
def getCell(app, x, y):
    # aka "viewToModel"
    # return (row, col) in which (x, y) occurred or (-1, -1) if outside grid.
    if (not pointInGrid(app, x, y)):
        return (-1, -1)
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth  = gridWidth / app.cols
    cellHeight = gridHeight / app.rows

    # Note: we have to use int() here and not just // because
    # row and col cannot be floats and if any of x, y, app.margin,
    # cellWidth or cellHeight are floats, // would still produce floats.
    
    row = int((y - app.margin) / cellHeight)
    col = int((x - app.margin) / cellWidth)

    return (row, col)
def getCellBounds(app, row, col):
    # aka "modelToView"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = app.width - 2*app.margin
    gridHeight = app.height - 2*app.margin
    cellWidth = gridWidth / app.cols
    cellHeight = gridHeight / app.rows
    x0 = app.margin + col * cellWidth
    x1 = app.margin + (col+1) * cellWidth
    y0 = app.margin + row * cellHeight
    y1 = app.margin + (row+1) * cellHeight
    return (x0, y0, x1, y1)


def boardCreation_mousePressed(app,event):


    if (((app.width/4)+320 > event.x and event.x > (app.width/4)-320)  and
        ((app.height*.90)-50 < event.y and event.y < (app.height*.90)+50)):
        app.mode = "difficultyLevel"
        
        # go to menu to ask how complex you want the maze
            #the make the pick out of three choices and deploy map algo right 
    (row, col) = getCell(app, event.x, event.y)
    # select this (row, col) unless it is selected
    if (app.selection == (row, col)):
        app.selection = (-1, -1)
    else:
        app.selection = (row, col)
        if (row,col) not in app.wall.map:
            app.wall.map[(row,col)] = set()

        checkIfConnected(row,col, app)
        
        if app.clicked <= app.rows* app.cols:
            app.clicked +=1

def boardCreation_redrawAll(app,canvas):


    canvas.create_rectangle(0,0,app.width, app.height, fill = 'black')
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, 
    text='Click which cells to raise into walls!',
                       font=font, fill='white')
    
    canvas.create_text(app.width/2, 50, 
    text='Press Enter to start Game!',
                       font=font, fill='white')

    canvas.create_text(app.width/4, app.height*.90, 
    text='Click here to generate premade map!',
                       font=font, fill='white')
    canvas.create_rectangle((app.width/4)-320,(app.height*.90)-50,
                        (app.width/4)+320,(app.height*.90)+50)
    


    # draw grid of cells
    for row in range(app.rows):
        for col in range(app.cols):
            if (row,col) not in app.wall.map:

                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill= 'blue')
            else:

                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill= 'red')

##########################################
# difficultyLevel
##########################################
def difficultyLevel_redrawAll(app,canvas):
    orange = rgbString(255,184,81)

    canvas.create_rectangle(0,0,app.width, app.height, fill = 'black')
    font = 'Arial 26 bold'
    canvas.create_text(app.width/2, 150, 
    text='Pick a difficulty level!',
                       font=font, fill='white')

    canvas.create_rectangle((app.width*.25)-50, (app.height*.80)-50,
                            (app.width*.25) + 50, (app.height*.80)+50)
    canvas.create_text(app.width*.25, app.height*.80, 
    text='Easy',font=font, fill='white')


    canvas.create_rectangle((app.width*.5)-75, (app.height*.80)-50,
                            (app.width*.5) + 75, (app.height*.80)+50)
    canvas.create_text(app.width*.5, app.height*.80, 
    text='Medium',font=font, fill='white')

    
    canvas.create_rectangle((app.width*.75)-50, (app.height*.80)-50,
                            (app.width*.75) + 50, (app.height*.80)+50)
    canvas.create_text(app.width*.75, app.height*.80, 
    text='Hard',font=font, fill='white')
def difficultyLevel_keyPressed(app, event):

    if (event.key == "Left"):
        app.mode = 'boardCreation'
def difficultyLevel_mousePressed(app,event):
    
    if((app.width*.25)+50 >  event.x and (app.width*.25)-50 <  event.x and
    (app.height*.80)+50>  event.y and (app.height*.80)-50<  event.y ):
        
        for col in [10]:
            for row in range (app.rows-1, 0 ,-1):
                app.wall.map[(row,col)] = set()


        for col in [2, 18]:
            for row in range (app.rows-1):
            
        
                app.wall.map[(row,col)] = set()
        checkIfConnected(row,col, app)
        createPathGraph(app)

        app.mode = "Game"


    if((app.width*.5)+75 >  event.x and (app.width*.5)-75 <  event.x and
    (app.height*.80)+50>  event.y and (app.height*.80)-50<  event.y ):
        #do maze generation with the medium alogrithm

        
        checkerow = 6
        checkercol = 0 
        for block in range (13):
            blocksrows = checkerow + block
            blockscols =  checkercol + block
            app.wall.map[(blocksrows, blockscols)] = set()


        checkerow = app.rows
        checkercol = app.cols     
        #19 blocks diagonal starting from 19,19

        for block in range (app.rows-1):
            app.wall.map[(checkerow -block, checkercol - block)] = set()


        checkerow = 0
        checkercol = 6 
        for block in range (13):
            blocksrows = checkerow + block
            blockscols =  checkercol + block
            app.wall.map[(blocksrows, blockscols)] = set()
            
        checkIfConnected(blocksrows, blockscols, app)
        createPathGraph(app)

        app.mode = "Game"

    if((app.width*.75)+50 >  event.x and (app.width*.75)-50 <  event.x and
    (app.height*.80)+50>  event.y and (app.height*.80)-50<  event.y ):
        
        points = []

        for i in range(1,15):
            points.append((19,i))

        for i  in range(16,7,-1):
            points.append((i,17))
        points += [(7,16),(6,15)]

        for i in range(14,6,-1):
            points.append((5,i))
        points += [(6,6),(7,5),(8,5),(9,4),(10,5)]

        for i in range(6,13):
            points.append((11,i))

        for i in range(15, 5,-1):
            points.append((0,i))
        points += [(1,5),(2,2),(3,1)]

        for i in range(4,16):
            points.append((i,0))
        
        for i in range(2, 15):
            points.append((16,i))
        
        
        points += [(16,15)]
        for i in range(15,9,-1):
           points.append((i,15))
  
        for point in points:
            app.wall.map[point] = set()

        checkIfConnected(point[0], point[1], app)
        createPathGraph(app)

        app.mode = "Game"
      

##########################################
# Game
##########################################


def Game_redrawAll(app,canvas):
    orange = rgbString(255,184,81)
    font = 'Arial 26 bold'


    canvas.create_rectangle(0,0,app.width, app.height, fill = 'black')
    canvas.create_text(app.width/4,100, text ='Points', font = font,
    fill = "white")

    canvas.create_text(app.width/4,150, text = f'{app.pacman.points}',
        font = font, fill = "white")

    canvas.create_text(app.width/2,100, text ='Lives', font = font,
    fill = "white")

    canvas.create_text(app.width/2,150, text = f'{app.pacman.lives}',
        font = font,fill = "white")
    
    drawBoard(app,canvas)

    drawPac(app,canvas)
            
    drawPointPellet(app,canvas)

    drawGhosts(app,canvas)
def drawBoard(app,canvas):
    for row in range (app.rows):
        for col in range (app.cols):
            if (row,col) not in app.wall.map:

#lines 443-448 were from 15-112 website: https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html

                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill= 'blue')
            else:

                (x0, y0, x1, y1) = getCellBounds(app, row, col)
                canvas.create_rectangle(x0, y0, x1, y1, fill= 'red')
            
            while (app.pacman.row,app.pacman.col)  in app.wall.map:
                app.pacman.row=  random.randint(1,20)
                app.pacman.col = random.randint(1,20)
def drawPac(app,canvas):
    (x0, y0, x1, y1) = getCellBounds(app, app.pacman.row, app.pacman.col)
    canvas.create_oval(x0, y0, x1, y1, fill= 'yellow')
def drawPointPellet(app,canvas):
    (x0, y0, x1, y1) = getCellBounds(app, app.pointPellet.row, app.pointPellet.col)
    canvas.create_oval(x0, y0, x1, y1, fill= 'green')
def drawGhosts(app,canvas):

    for Ghost in app.ghosts:
        (x0, y0, x1, y1) = getCellBounds(app, Ghost.row, Ghost.col)
        canvas.create_oval(x0, y0, x1, y1, fill= Ghost.color)
def Game_timerFired(app):
    
    for Ghost in app.ghosts:
        start = (Ghost.row,Ghost.col)
        
        target =(app.pacman.row,app.pacman.col)
        
        result = bfs(app,start, target )


        if type(result) == dict:
            Ghost.getpath(result,target)
        if(app.pacman.row,app.pacman.col) ==  ( Ghost.row, Ghost.col):
            app.pacman.lives -=1
        if app.pacman.lives == 0:
            app.mode = "GameOver"
def Game_keyPressed(app,event):


    if event.key == "Up":

        nrow = app.pacman.row - 1
        ncol = app.pacman.col + 0 
        if checkLegalMove(app,nrow,ncol):
            app.pacman.row  = nrow
            app.pacman.col  = ncol


    if event.key == "Down":
        nrow = app.pacman.row + 1
        ncol = app.pacman.col + 0 
        if checkLegalMove(app,nrow,ncol):
            app.pacman.row  = nrow
            app.pacman.col  = ncol


    if event.key == "Right":
        nrow = app.pacman.row + 0 
        ncol = app.pacman.col + 1
        if checkLegalMove(app,nrow,ncol):
            app.pacman.row  = nrow
            app.pacman.col  = ncol

    if event.key == "Left":
    
        nrow = app.pacman.row + 0 
        ncol = app.pacman.col - 1
        if checkLegalMove(app,nrow,ncol):
            app.pacman.row  = nrow
            app.pacman.col  = ncol

    if ((app.pacman.row,app.pacman.col) ==
    (app.pointPellet.row, app.pointPellet.col)):
        app.pointPellet.relocate(app)
        app.pacman.points+=1

        if app.pacman.points %15 ==0:
            app.mode = "boardCreation"

        if app.pacman.points == 44:

           app.mode = "WinningMode"
 
def checkLegalMove(app, nrow,ncol):
    if ((nrow>=0 and nrow< app.rows) and(ncol>=0 and ncol< app.rows) and 
        (nrow,ncol) not in app.wall.map):
        return True
    return False


##########################################
#  WinningMode
##########################################
def WinningMode_redrawAll(app,canvas):


    font = 'Arial 26 bold'    
    
    
    canvas.create_rectangle(0,0,app.width, app.height, fill ="white")
  
    canvas.create_text(app.width/2,app.height/2, text ='You Win!', 
        font = font, fill = "black")



##########################################
# GameOver
##########################################

def GameOver_redrawAll(app,canvas):
    canvas.create_rectangle(0,0,app.width, app.height, fill ="black")

    font = 'Arial 26 bold'

    canvas.create_text(app.width/2,app.height/2, text ='Game Over!', 
        font = font, fill = "white")



##########################################
# Main App
##########################################
def appStarted(app):


 #lines 577-580 from 15-112 website: https://www.cs.cmu.edu/~112/notes/notes-animations-part2.html
    app.mode = 'introScrene1'
    
    #info to generate board in boardCreation 
    app.rows = 20
    app.cols = 20
    app.margin = 200 # margin around grid
    app.selection = (-1, -1) # (row, col) of selection, (-1,-1) for none
    
    #info about board
    app.clicked  = 0
    app.board  = [([] * app.cols) for i in range (app.rows)]
    app.wall = Graph()
    app.path = Graph()

    #info on pointpellets
    app.pointPellet = PointPellet(app)

    #info on Pacman
    app.pacman = Pac_Man(app)
    pink = rgbString(255,184,255)
    blue = rgbString(0,255,255)
    orange = rgbString(255,184,81)
    red = rgbString(255,0,0)
    app.ghost1 = Ghost(app,pink)
    app.ghost2 = Ghost(app,blue)
    app.ghost3 = Ghost(app, orange)
    app.ghost4 = Ghost(app, red)


    app.ghosts =[app.ghost1,app.ghost2,app.ghost3,app.ghost4 ]
    app.aspectRatio  = app.height/app.width
    app.fNear = 0.1
    app.fFar = 1000.0
    app.Fov = 90.0
    app.fFovRad = 1.0/ math.tan((app.Fov /2) /(180.0 * math.pi))
    app.theta =0
 
    matProj = Matrix(np.array([[0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],]))
    matProj.proj[0][0] = app.aspectRatio * app.fFovRad
    matProj.proj[1][1] = app.fFovRad
    matProj.proj[2][2] = app.fFar/ (app.fFar-app.fNear)
    matProj.proj[3][2] = ((-app.fFar* app.fNear)/ (app.fFar-app.fNear))
    matProj.proj[2][3] = 1.0
    matProj.proj[3][3] = 0.0
    '''Hardcodes the cube into 3D space with the normal information'''
 
    app.mesh = [
[[0, 1, 0], [0, 0, 0], [1, 0, 0], [0, 0, -1]] ,
[[0, 1, 0], [1, 0, 0], [1, 1, 0], [0, 0, -1]] ,
[[1, 1, 1], [0, 0, 1], [1, 0, 1], [0, 0, 1]] ,
[[1, 1, 1], [0, 1, 1], [0, 0, 1], [0, 0, 1]] ,
[[1, 1, 0], [1, 0, 0], [1, 0, 1], [1, 0, 0]] ,
[[1, 1, 0], [1, 0, 1], [1, 1, 1], [1, 0, 0]] ,
[[0, 1, 1], [0, 0, 1], [0, 0, 0], [-1, 0, 0]] ,
[[0, 1, 1], [0, 0, 0], [0, 1, 0], [-1, 0, 0]] ,
[[0, 0, 0], [0, 0, 1], [1, 0, 1], [0, 1, 0]] ,
[[0, 0, 0], [1, 0, 1], [1, 0, 0], [0, 1, 0]] ,
[[1, 1, 1], [0, 1, 0], [0, 1, 1], [0, -1, 0]] ,
[[1, 1, 1], [1, 1, 0], [0, 1, 0], [0, -1, 0]] ,   
               ]
       
   
 
    app.projected = copy.deepcopy(app.mesh)
    app.scaled = copy.deepcopy(app.mesh)
    app.mesh = game_test.multiplyMatrix(app, matProj)

def createPathGraph(app):
    for row in range (app.rows):
        for col in range (app.cols):
            if (row,col) not in app.wall.map:
                app.path.map[(row,col)]  = set()
                for (drow,dcol) in [(-1,0),(-1,1),(0,1),
                                     (1,1),(1,0),(1,-1),(0,-1),(-1,-1)]:                                       

                    if ((0 <= drow+row and drow+row < app.rows) and
                        (0 <= dcol+col and dcol+col < app.cols)and
                        (drow+row,dcol+col) not in app.wall.map):
                        newrow = drow+row
                        newcol = dcol+col

                        if (newrow,newcol) not in app.path.map:
                            app.path.map[(newrow,newcol)] = set()
                        else:
                            app.path.map[(newrow,newcol)].add((row,col))
                        app.path.map[(row,col)].add((newrow,newcol))

def checkIfConnected(row,col,app):
    for (drow,dcol) in [(-1,0),(-1,1), (0,1), (1,1),(1,0),(1,-1),(0,-1),(-1,-1)]:
        if ((0 < drow+row and drow+row < app.rows) and
            (0 < dcol+col and dcol+col < app.cols)):
            newrow = drow+row
            newcol = dcol+col
    
            if (newrow,newcol) in app.wall.map and (newrow,newcol) != (-1,-1):
                
                app.wall.map[(newrow,newcol)].add((row,col))
                app.wall.map[(row,col)].add((newrow,newcol))

def bfs(app,self, target):
    queue =   [(self[0], self[1])]
    visited =  [(self[0], self[1])]
    previous = {}

    if queue[0] == target:
        return target
       
    while queue != set(): #use while loop

        if  queue != [] and queue[0] == target :
            return previous
        
        else:
            for (drow,dcol) in [(-1,0),(-1,1), (0,1), (1,1),(1,0),
                                                        (1,-1),(0,-1),(-1,-1)]:
                if((queue[0][0] + drow,queue[0][1] + dcol) not in visited and
                (queue[0][0] + drow, queue[0][1] + dcol) not in app.wall.map and 
                queue[0][0] + drow >=0  and queue[0][0] + drow < app.rows and 
                queue[0][1] + dcol >= 0 and queue[0][1] + dcol < app.cols ):
                    
                    queue.append( (queue[0][0] + drow, queue[0][1] + dcol))
                    visited.append( (queue[0][0] + drow, queue[0][1] + dcol))
                    previous[(queue[0][0] + drow, queue[0][1] + dcol)] = queue[0]
            queue.pop(0)
    
    return None

class PointPellet(object):
    def __init__(self,app):
        self.row = random.randint(1, app.rows-1)
        self.col = random.randint(1, app.cols-1)

        if (self.row, self.col) in app.wall.map:
            while(self.row, self.col) in app.wall.map:
                self.row = random.randint(1, app.rows-1)
                self.col = random.randint(1, app.cols-1)

    def relocate(self,app):

        self.row = random.randint(1, app.rows-1)
        self.col = random.randint(1, app.cols-1)

        if (self.row, self.col) in app.wall.map:
            while(self.row, self.col) in app.wall.map:
                self.row = random.randint(1, app.rows-1)
                self.col = random.randint(1, app.cols-1)
class Graph(object):
    def __init__(self):
        self.map = {}
class Pac_Man (object):
    
    def __init__(self,app):
        self.row = 0
        self.col = app.cols-1
        self.points = 0
        self.lives = 10 

        if (self.row, self.col) in app.wall.map:
            while(self.row, self.col) in app.wall.map:
                self.row = random.randint(1, app.rows-1)
                self.col = random.randint(1, app.cols-1)
class Ghost (object):
    def __init__(self,app, color):
        self.row = random.randint(1, app.rows-1)
        self.col = random.randint(1, app.cols-1)
        if (self.row, self.col) in app.wall.map:
            while((self.row, self.col) in app.wall.map and
            (self.row, self.col) !=  (app.pointPellet.row, app.pointPellet.col)):
                self.row = random.randint(1, app.rows-1)
                self.col = random.randint(1, app.cols-1)        
        
        self.color = color
        self.test = True
        
    def getpath(self,prev,target):
        path = target
        while prev[path] in prev:
            if prev[path] == (self.row,self.col):
                break

            path = prev[path]
        self.row = path[0]
        self.col = path[1]

runApp()