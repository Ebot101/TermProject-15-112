'''this file supports the code for the perspective projection, 
rotation matrices and scalling of the 3D cube at the beginning of the game'''
#imports
import math, copy 
import numpy as np
import decimal
from cmu_112_graphics import *
import tkinter as tk
#################################################
# app-test
#################################################
def multiplyMatrix(app, matProj):
    '''    for triangle in range(len(app.scaled)):
       
        for i in range(len(app.scaled[triangle])-1):
            app.scaled[triangle][i][2] += 3'''
 
 
    multipliedMesh = [ ]
    for triangle in range(len(app.projected)):
        triContainer = [ ]
 
        for coor in range(len(app.projected[triangle])):
            triProj =np.array(app.projected[triangle][coor] +[1])
            triProj= triProj.dot(matProj.proj)
            if triProj[3]!= 0:
               
                triProj[0]/=triProj[3]
                triProj[1]/=triProj[3]
                triProj[2]/=triProj[3]
                triProj[3]/= triProj[3]
   
            triContainer.append(triProj )
        multipliedMesh.append(triContainer )
 
    '''the south and the north sides have the same normals and the
    east and the west sides have the same normal, this might be the problem'''
    return multipliedMesh
def appStarted(app):
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
 
    app.mesh = [
                #South
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
    app.mesh = multiplyMatrix(app, matProj)
    app.timerDelay=10
def rotateMesh(app):
    matRotz = Matrix(np.array ([[0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],]))
    matRotz.proj[0][0] = math.cos(app.theta)
    matRotz.proj[0][1] = math.sin(app.theta)
    matRotz.proj[1][0] = -(math.sin(app.theta))
    matRotz.proj[1][1] = math.cos(app.theta)
    matRotz.proj[2][2] = 1
    matRotz.proj[3][3] = 1
   
    matRotx = Matrix(np.array([ [0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],]))
    matRotx.proj[0][0] = 1
    matRotx.proj[1][1] = math.cos(app.theta)
    matRotx.proj[1][2] = math.sin(app.theta)
    matRotx.proj[2][1] = -(math.sin(app.theta))
    matRotx.proj[2][2] = math.cos(app.theta)
    matRotx.proj[3][3] = 1    
 
    matRoty = Matrix(np.array([ [0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],
                                [0.0,0.0,0.0,0.0],]))
    matRoty.proj[0][0] = math.cos(app.theta)
    matRoty.proj[1][1] = 1  
    matRoty.proj[0][2] = (math.sin(app.theta))
    matRoty.proj[2][0] = -(math.sin(app.theta))
    matRoty.proj[2][2] = math.cos(app.theta)
    matRoty.proj[3][3] = 1    
 
    matRotf = Matrix(np.array(matRotx.proj.dot(matRotz.proj)))
    app.mesh = multiplyMatrix(app,matRotx)

def timerFired(app):
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
    
    """replacing app.projected with app.mesh"""
    app.mesh = multiplyMatrix(app, matProj)    

    app.theta+=.05

    rotateMesh(app)

    ScaleTri(app)
def ScaleTri(app):
 
 
    app.scaled= copy.deepcopy(app.mesh)
    smallest = min( app.width, app.height)
 
  #1084488 ITEM 0-A3
 
    for triangle in app.scaled:
        for i in range(len(triangle)-1):
            triangle[i][0] = (triangle[i][0]+9)*(.1* smallest)
 
            triangle[i][1]  = (triangle[i][1]+5)*(.1* smallest)
def redrawAll(app, canvas):
    '''changes'''
 
    for tri in range (len(app.scaled)):
        if(app.scaled[tri][3][1] <= 0 ):
            for i in range(len(app.scaled[tri])):
                canvas.create_line(app.scaled[tri][0][0], app.scaled[tri][0][1],
                                    app.scaled[tri][1][0], app.scaled[tri][1][1],
                fill= 'black'  )
                canvas.create_line(app.scaled[tri][1][0], app.scaled[tri][1][1],
                                app.scaled[tri][2][0], app.scaled[tri][2][1],
                fill= 'black'  ),
                canvas.create_line(app.scaled[tri][2][0], app.scaled[tri][2][1],
                                app.scaled[tri][0][0], app.scaled[tri][0][1],
                fill= 'black' )
def s21Midterm1Animation():
 
    runApp()
class Matrix:
    def __init__(self, proj):
 
        self.proj = proj 
#################################################
# main
#################################################
def main():
    s21Midterm1Animation()
if __name__ == '__main__':
    main()