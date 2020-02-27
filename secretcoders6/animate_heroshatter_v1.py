#!/usr/bin/python3
# -*- coding: utf-8 -*-



class HeroShatter(object):
    '''Class to animate hero shatter.

       Required Options:

       screen = class Screen() from from Python's turtle module
       pen    = class Turtle() from from Python's turtle module
       origin = the start point to draw giant 
    '''   
    def __init__(self, screen, pen, origin, *args, **kwargs):
        print("Instance of class HeroShatter()")

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
        #self._get_hero_origins( origin )
        #print('self._Lleg =',self._Lleg )
        #print('self._Rleg =',self._Rleg )
        #print('self._Body =',self._Body )
        #print('self._Larm =',self._Larm )
        #print('self._Rarm =',self._Rarm )
        #self._shatter()

        
    def animate(self):
        self.pen.hideturtle() #hide pen, only see the drawn lines
        self.screen.tracer(0) #stop turtle's default screen animation
        self._get_hero_origins( self.origin )
        self._shatter()
        self.screen.tracer(1) #restart turtle's default screen animation
        self.pen.pu()
        self.pen.home()
        #self.pen.showturtle() #show pen
       

    def _get_hero_origins(self, origin):
        '''Get origins Lleg, Rleg, Body, Larm, Rarm and Head.'''
        pen=self.pen
        pen.pu()
        pen.goto( origin )
        #draw legs
        self._Lleg=pen.pos() #get
        self._hero_drawLleg()
        self._hero_Lleg_to_Rleg()
        self._Rleg=pen.pos() #get
        self._hero_drawRleg()
        self._hero_Rleg_to_body()
        pen.pu()
        pen.fd(200)
        self._Larm=pen.pos() #get
        self._hero_drawLarm()
        self._Body=pen.pos() #get
        self._hero_drawBody()
        pen.pu()
        pen.fd(195)
        self._Rarm=pen.pos() #get
        self._hero_drawRarm()
        pen.pu()
        pen.fd(85)
        pen.lt(90)
        pen.fd(169)
        pen.rt(90)
        self._Head=pen.pos() #get
        self._hero_drawhead_shatter()
        self.screen.update()
        

    def _shatter(self):
        pen = self.pen

        incre = 0
        for i in range(900):
            incre += 0.0001
            pen.clear()
            self._gotoLleg( pen, incre )
            self._hero_drawLleg()
            self._gotoRleg( pen, incre )
            self._hero_drawRleg()
            self._gotoLarm( pen, incre )
            self._hero_drawLarm()
            self._gotoBody( pen, incre )
            self._hero_drawBody()
            self._gotoRarm( pen, incre )
            self._hero_drawRarm()
            self._gotoHead( pen, incre )
            self._hero_drawhead_shatter()
            self.screen.update()
        

    def _gotoLleg( self, pen, incre ):
        pen.pu()
        pen.goto(self._Lleg)
        pen.lt(90)
        pen.fd(incre)
        pen.lt(90)
        pen.fd(incre)
        pen.rt(180)
        self._Lleg=pen.pos()

        
    def _gotoRleg( self, pen, incre ):
        pen.pu()
        pen.goto(self._Rleg)
        pen.rt(90)
        pen.fd(incre)
        pen.rt(90)
        pen.fd(incre)
        pen.lt(90)
        self._Rleg=pen.pos()
        
        
    def _gotoLarm( self, pen, incre ):
        pen.pu()
        pen.goto(self._Larm)
        pen.lt(90)
        pen.fd(incre)
        pen.rt(90)
        self._Larm=pen.pos()
        

    def _gotoBody( self, pen, incre ):
        pen.pu()
        pen.goto(self._Body)
        pen.fd(incre)
        pen.lt(90)
        pen.fd(incre)
        pen.rt(90)
        self._Body=pen.pos()
        

    def _gotoRarm( self, pen, incre ):
        pen.pu()
        pen.goto(self._Rarm)
        pen.fd(incre)
        pen.rt(90)
        pen.fd(incre)
        pen.lt(90)
        self._Rarm=pen.pos()
        

    def _gotoHead( self, pen, incre ):
        pen.pu()
        pen.goto(self._Head)
        pen.fd(incre*2)
        pen.rt(0.01)
        pen.fd(0.005)
        self._Head=pen.pos()
        

    #############################################################
    # LEGS
    #############################################################
    def _hero_drawLleg( self ):
        pen=self.pen
        pen.pd()   #start left toe
        pen.rt(45)
        pen.fd(25)
        pen.lt(45)
        pen.fd(220)
        pen.rt(90)
        pen.fd(97) #left leg top end
        pen.rt(90)
        pen.pu()   # gap
        pen.fd(68)
        pen.rt(90)
        pen.pd()
        pen.fd(30) #continue draw left leg
        pen.lt(90)
        pen.fd(170)
        pen.rt(90)
        pen.fd(85)
        pen.rt(90)

    def _hero_Lleg_to_Rleg( self ):
        pen=self.pen
        pen.pu()   #goto right leg startpoint
        pen.fd(238)
        pen.rt(90)
        pen.fd(117)

    def _hero_drawRleg( self ):
        pen=self.pen
        pen.pd()   #draw right leg 
        pen.fd(97) 
        pen.rt(90)
        pen.fd(220)
        pen.lt(45)
        pen.fd(25)
        pen.rt(135)
        pen.fd(85) #
        pen.rt(90)
        pen.fd(170)
        pen.lt(90)
        pen.fd(30)
        pen.rt(90)
        pen.pu()
        pen.fd(68)

    def _hero_Rleg_to_body( self ):
        pen=self.pen
        pen.pu()   #goto body
        pen.lt(90)
        pen.fd(97)
        pen.rt(90)

    #############################################################
    # BODY
    #############################################################
    def _hero_drawfingers( self ):
        pen=self.pen
        for i in range(3):
            pen.fd(25)
            pen.rt(90)
            pen.fd(30)
            pen.bk(30)
            pen.lt(90)


    def _hero_drawLarm( self ):
        pen=self.pen
        pen.pd()
        pen.lt(90)
        pen.fd(25)
        pen.lt(90)
        pen.fd(195)
        pen.rt(90)
        self._hero_drawfingers()
        pen.rt(90)
        pen.fd(280)
        pen.rt(90)
        pen.fd(100)

    def _hero_drawBody( self ):
        pen=self.pen
        pen.pd()
        pen.fd(195)
        pen.rt(90)
        pen.pu()
        pen.fd(85)
        pen.pd()
        pen.fd(200)
        pen.rt(90)
        pen.fd(195)
        pen.rt(90)
        pen.fd(200)
        pen.pu()
        pen.fd(85)
        pen.pd()
        pen.rt(90)

    def _hero_drawRarm( self ):
        pen=self.pen
        pen.pd()
        pen.fd(100)
        pen.rt(90)
        pen.fd(280)
        pen.rt(90)
        self._hero_drawfingers()
        pen.rt(90)
        pen.fd(195)
        pen.lt(90)
        pen.fd(25)
        pen.rt(90)


    #############################################################
    # HEAD
    #############################################################
    def _hero_drawhead_shatter( self ):
        pen=self.pen
        pen.pd()
        for _ in range(3): #draw head w/o neck
            pen.fd(145)
            pen.rt(90)
        pen.pu()           #goto head start
        pen.fd(145)
        pen.rt(90)
        pen.fd(50)         #goto mouth
        pen.rt(90)
        pen.fd(50)
        pen.pd()
        pen.fd(45)         #draw mouth
        pen.pu()           #goto spec bridge
        pen.bk(35)
        pen.lt(90)
        pen.fd(50)
        pen.rt(90)
        pen.pd()           #draw spec bridge
        pen.fd(25)
        pen.pu()           #goto spec frame start
        pen.bk(65)
        pen.lt(90)
        pen.fd(20)
        pen.rt(90)
        for _ in range(2): #draw spec frame
            pen.pd()
            for i in range(4):
                pen.fd(40)
                pen.rt(90)
            pen.pu()
            pen.fd(65)
        pen.bk(150)        #goto head start
        pen.lt(90)
        pen.bk(120)


#HERO_ORIGIN = (-390, -420) # x, y coordinate
HERO_ORIGIN = (-90,-340)    # x, y coordinate

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

    hero = HeroShatter(screen, pen, HERO_ORIGIN)
    hero.animate()


if __name__ == '__main__':
    main()


