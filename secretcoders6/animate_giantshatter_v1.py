#!/usr/bin/python3
# -*- coding: utf-8 -*-

from math import sqrt 

class GiantShatter():
    '''Class to animate giant shatter.

       Required Options:

       screen = class Screen() from from Python's turtle module
       pen    = class Turtle() from from Python's turtle module
       origin = the start point to draw giant 
    '''   
    def __init__(self, screen, pen, origin, *args, **kwargs):
        print("\nclass GiantShatter():")
        
        #Attributes
        self.screen = screen
        self.pen = pen
        self.origin = origin
        
        self._Lleg = (0,0)
        self._Rleg = (0,0)
        self._Body = (0,0)
        self._Larm = (0,0)
        self._Rarm = (0,0)
        self._Head = (0,0)

        #For debugging
        #self._get_giant_origins( origin ) 
        #print('self._Lleg =',self._Lleg )
        #print('self._Rleg =',self._Rleg )
        #print('self._Body =',self._Body )
        #print('self._Larm =',self._Larm )
        #print('self._Rarm =',self._Rarm )
        #self._shatter()

        
    def animate(self):
        self.pen.hideturtle() #hide pen, only see the drawn lines
        self.screen.tracer(0) #stop turtle's default screen animation 
        self._get_giant_origins( self.origin ) 
        self._shatter()
        self.screen.tracer(1) #restart turtle's default screen animation
        self.pen.pu()
        self.pen.home()
        #self.pen.showturtle() #show pen
       

    def _get_giant_origins(self, origin):
        '''Get origins Lleg, Rleg, Body, Larm, Rarm and Head.'''
        pen=self.pen
        pen.pu()
        pen.goto( origin )
        #draw legs
        self._Rleg=pen.pos() #get
        self._giant_drawRleg()
        self._giant_Rleg_to_Lleg()
        self._Lleg=pen.pos() #get
        self._giant_drawLleg()
        self._giant_Lleg_to_body()
        pen.pu()
        pen.fd(200)
        self._Rarm=pen.pos() #get
        self._giant_drawRarm()
        self._Body=pen.pos() #get
        self._giant_drawBody()
        pen.pu()
        pen.fd(195)
        self._Larm=pen.pos() #get
        self._giant_drawLarm()
        pen.pu()
        pen.fd(85)
        pen.rt(90)
        pen.fd(169)
        pen.lt(90)
        self._Head=pen.pos() #get
        self._giant_drawhead_shatter()
        self.screen.update()
        

    def _shatter(self):
        pen = self.pen

        incre = 0
        for i in range(900):
            incre += 0.0001
            pen.clear()
            self._gotoRleg( pen, incre )
            self._giant_drawRleg()
            self._gotoLleg( pen, incre )
            self._giant_drawLleg()
            self._gotoRarm( pen, incre )
            self._giant_drawRarm()
            self._gotoBody( pen, incre )
            self._giant_drawBody()
            self._gotoLarm( pen, incre )
            self._giant_drawLarm()
            self._gotoHead( pen, incre )
            self._giant_drawhead_shatter()
            self.screen.update()
        

    def _gotoRleg( self, pen, incre ):
        pen.pu()
        pen.goto(self._Rleg)
        pen.rt(90)
        pen.fd(incre)
        pen.rt(90)
        pen.fd(incre)
        pen.lt(180)
        self._Rleg=pen.pos()

        
    def _gotoLleg( self, pen, incre ):
        pen.pu()
        pen.goto(self._Lleg)
        pen.lt(90)
        pen.fd(incre)
        pen.lt(90)
        pen.fd(incre)
        pen.rt(90)
        self._Lleg=pen.pos()
        
        
    def _gotoRarm( self, pen, incre ):
        pen.pu()
        pen.goto(self._Rarm)
        pen.rt(90)
        pen.fd(incre)
        pen.lt(90)
        self._Rarm=pen.pos()
        

    def _gotoBody( self, pen, incre ):
        pen.pu()
        pen.goto(self._Body)
        pen.fd(incre)
        pen.rt(90)
        pen.fd(incre)
        pen.lt(90)
        self._Body=pen.pos()
        

    def _gotoLarm( self, pen, incre ):
        pen.pu()
        pen.goto(self._Larm)
        pen.fd(incre)
        pen.lt(90)
        pen.fd(incre)
        pen.rt(90)
        self._Larm=pen.pos()
        

    def _gotoHead( self, pen, incre ):
        pen.pu()
        pen.goto(self._Head)
        pen.fd(incre*2)
        pen.lt(0.01)
        pen.fd(0.005)
        self._Head=pen.pos()
        

#############################################################
# LEGS
#############################################################
    def _giant_drawRleg( self ):
        pen=self.pen
        pen.pd()   #start left toe
        pen.lt(45) 
        pen.fd(25)
        pen.rt(45)
        pen.fd(220)
        pen.lt(90)
        pen.fd(97) #right leg top end
        pen.lt(90)
        pen.pu()   # gap
        pen.fd(68)
        pen.lt(90)
        pen.pd()
        pen.fd(30) #continue draw right leg
        pen.rt(90)
        pen.fd(170)
        pen.lt(90)
        pen.fd(85)
        pen.lt(90)

    def _giant_Rleg_to_Lleg( self ):
        pen=self.pen
        pen.pu()   #goto left leg startpoint
        pen.fd(238)
        pen.lt(90)
        pen.fd(117)

    def _giant_drawLleg( self ):
        pen=self.pen
        pen.pd()   #draw right leg 
        pen.fd(97) 
        pen.lt(90)
        pen.fd(220)
        pen.rt(45)
        pen.fd(25)
        pen.lt(135)
        pen.fd(85) #
        pen.lt(90)
        pen.fd(170)
        pen.rt(90)
        pen.fd(30)
        pen.lt(90)
        pen.pu()
        pen.fd(68)

    def _giant_Lleg_to_body( self ):
        pen=self.pen
        pen.pu()   #goto body
        pen.rt(90)
        pen.fd(97)
        pen.lt(90)

    #############################################################
    # BODY
    #############################################################
    def _giant_drawfingers( self ):
        pen=self.pen
        d2=sqrt(((75/6)**2)*2)
        pen.lt(45)
        for i in range(3):
            pen.fd(d2)
            pen.rt(90)
            pen.fd(d2)
            pen.lt(90)
        pen.lt(45)


    def _giant_drawRarm( self ):
        pen=self.pen
        pen.pd()
        pen.rt(90)
        pen.fd(25)
        pen.rt(90)
        pen.fd(195)
        pen.lt(90)
        self._giant_drawfingers()
        pen.fd(280)
        pen.lt(90)
        pen.fd(100)

    def _giant_drawBody( self ):
        pen=self.pen
        pen.pd()
        pen.fd(195)
        pen.lt(90)
        pen.pu()
        pen.fd(85)
        pen.pd()
        pen.fd(200)
        pen.lt(90)
        pen.fd(195)
        pen.lt(90)
        pen.fd(200)
        pen.pu()
        pen.fd(85)
        pen.pd()
        pen.lt(90)

    def _giant_drawLarm( self ):
        pen=self.pen
        pen.pd()
        pen.fd(100)
        pen.lt(90)
        pen.fd(280)
        pen.lt(90)
        self._giant_drawfingers()
        pen.fd(195)
        pen.rt(90)
        pen.fd(25)
        pen.lt(90)


    #############################################################
    # HEAD
    #############################################################
    def _giant_drawhead_shatter( self ):
        pen=self.pen
        pen.pd()
        for i in range(3): #draw head w/o neck
            pen.fd(140)
            pen.lt(90)
        pen.pu()           #goto head start
        pen.fd(140)
        pen.lt(90)
        pen.fd(50)         #goto mouth
        pen.lt(45)
        d2=sqrt(2*(140/6)**2)
        pen.pd()
        for i in range(3): #draw mouth
            pen.fd(d2)
            pen.lt(90)
            pen.fd(d2)
            pen.rt(90)
        pen.pu()           #goto eye
        pen.rt(45)
        pen.fd(50)
        pen.rt(90)
        pen.fd(25)
        pen.pd()           #draw eye
        pen.fd(90)         
        pen.pu()           #goto head start
        pen.fd(25)
        pen.lt(90)
        pen.bk(100)


#GIANT_ORIGIN = (-390, -420) # x, y coordinate
GIANT_ORIGIN = (-90,-340)    # x, y coordinate

def main():
    import tkinter as tk
    import turtle as tt
    
    tt.mode('logo')
    screen = tt.Screen()
    screen.screensize(1173,990)
    pic_background_clearsky  ='./image/battleground2_clearsky.gif'
    screen.bgpic( pic_background_clearsky )    

    pen = tt.Turtle()
    pen.speed(5)
    pen.width(12)

    giant = GiantShatter(screen, pen, GIANT_ORIGIN)
    giant.animate()


if __name__ == '__main__':
    main()
