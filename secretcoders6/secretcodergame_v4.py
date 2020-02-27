#!/usr/bin/python3
# -*- coding: utf-8 -*-

import turtle as tt
import tkinter as tk
import tkinter.ttk as ttk
from tkinter import font

import platform
from math import sqrt
import random
import functools
from playsound import playsound

from animate_heroshatter_v1 import HeroShatter
from animate_giantshatter_v1 import GiantShatter

###############################################################################
# Global variables
###############################################################################
#Styles
HEROCOLORS = ( 'mediumseagreen','DeepSkyBlue','medium slate blue','gold',
               'tan1','peach puff', 'khaki1','chocolate1','LightCyan','thistle')
GIANTCOLORS = ( 'light slate blue','DeepSkyBlue','aqua','blue2','spring green',
                'DarkOrchid2', 'maroon2','goldenrod2','dark orange')
HERO_FG = HEROCOLORS[0]
GIANT_FG = GIANTCOLORS[0]
GAMEGUI_BG = '#c3d6d5'
#GAMEGUI_BG = 'light green'

LIFEPOINTS = 20

#Decorators
def set_herobutton( func ):
    @functools.wraps(func)    
    def wrapper_set_herobutton( self, startup=False, *args,**kwargs ):
        #print('\ndef wrapper_set_herobutton( self,*args,**kwargs ):')
        
        if self.nplayers.get()==1:
            #print('OnePlayer')
            if self.player1.get() == 'Secret Coders':
                #print('Player = Secret Coders')
                #print('startup = ', startup)
                if startup:
                    #print('-startup')
                    #1.Pre-func: Get Hero and Giant origins.
                    #2.Run passed-in function.
                    #3.Post-func: Do nothing
                    #print(func.__name__)
                    self.setHeroGiantOrigins() 
                    func( self,*args,**kwargs )
                else:
                    #1.Pre-func
                    #   -Disable all hero buttons 
                    #   -Set background 
                    #   -Get hero action's name
                    #   -Get giant action
                    #   -Get giant action's name
                    #   -Get origin for hero and giant actions
                    #2.Show hero action (Run passed-in function)
                    #3.Post-func
                    #   -Show giant action
                    #   -Show lifepoint,background,soundeffect
                    #   -Re-enable all hero butttons
                    self.setButtonsState( self.herobuttons,disabled=True );#print('Disabled all hero buttons') 
                    self.screen.bgpic(self.pic_background_clearsky)
                    heroactionname = func.__name__;#print('heroactionname =',heroactionname)
                    giantaction = self.getGiantAction()
                    giantactionname = giantaction.__name__
                    self.setHeroGiantOrigins( heroactionname,giantactionname) 
                    self.hero_pen.clear()
                    self.giant_pen.clear()
                    func( self,*args,**kwargs )
                    giantaction()
                    self.setLifePoints( heroactionname,giantactionname )
                    game_ended = self.checkEndOfLife()
                    if not game_ended:
                        self.setButtonsState( self.herobuttons,disabled=False );#print('Enabled all hero buttons')
            elif self.player1.get() == 'Dr. One-Zero':
                #print('Player = Dr. One-Zero')
                #print('- set_herobutton only run passed-in function')
                #print(func.__name__)
                #1. Pre-func: Do nothing
                #2. Run passed-in function
                #3. Post-func: Do nothing
                func( self,*args,**kwargs )
            else:
                raise Exception('Invalid self.player1 value')                
            self.update_idletasks()
       
    return wrapper_set_herobutton


def set_giantbutton( func ):
    @functools.wraps(func)    
    def wrapper_set_giantbutton( self, startup=False, *args,**kwargs ):
        #print('\ndef wrapper_set_giantbutton( self,*args,**kwargs ):')
       
        if self.nplayers.get()==1:
            #print('OnePlayer')
            if self.player1.get() == 'Dr. One-Zero':
                #print('Dr. One-Zero')
                #print('startup = ', startup)
                if startup:
                    #print('-startup')
                    #1. Pre-func: Get origin for hero and giant actions
                    #2. Run passed-in function
                    #3. Post-func: Do nothing
                    #print(func.__name__)
                    self.setHeroGiantOrigins() 
                    func( self,*args,**kwargs )
                else:
                    #print('Player = Dr. One-Zero')
                    #1. Pre-func
                    #   -Disable all hero buttons 
                    #   -Set background 
                    #   -Get hero action's name
                    #   -Get giant action
                    #   -Get giant action's name
                    #   -Get origin for hero and giant actions
                    #2.Show hero action (Run passed-in function)
                    #3.Post-func
                    #   -Show giant action
                    #   -Show lifepoint,background,soundeffect
                    #   -Re-enable all hero butttons
                    self.setButtonsState( self.giantbuttons,disabled=True );#print('Disabled all giant buttons') 
                    self.screen.bgpic(self.pic_background_clearsky)
                    giantactionname = func.__name__;#print('giantactionname =',giantactionname)
                    heroaction = self.getHeroAction()
                    heroactionname = heroaction.__name__
                    self.setHeroGiantOrigins( heroactionname,giantactionname) 
                    self.hero_pen.clear()
                    self.giant_pen.clear()
                    func( self,*args,**kwargs )
                    heroaction()
                    self.setLifePoints( heroactionname,giantactionname )
                    game_ended = self.checkEndOfLife()
                    if not game_ended:
                        self.setButtonsState( self.giantbuttons,disabled=False );#print('Enabled all giant buttons') 
            elif self.player1.get() == 'Secret Coders':
                #print('Player is Secret Coders')
                #print('- set_giantbutton only need to run passed-in function')
                #1. Pre-func: Do nothing
                #2. Run passed-in function
                #3. Post-func: Do nothing
                #print(func.__name__)
                func( self,*args,**kwargs )
            else:
                raise Exception('Invalid self.player1 value')                
            self.update_idletasks()
                
    return wrapper_set_giantbutton



class FramedButtons( ttk.Frame ):
    
    def __init__( self, *args, **kwargs ):
        super().__init__( *args, **kwargs )
        self.buttons = []
        self.bind("<Configure>", self._redraw)


    def _redraw( self, event=None):
        '''Reposition buttons to fit Frame's width and set Frame's height'''
        #1. Get Frame's max. width
        fr_width = self.winfo_width()
        fr_borderwidth = self['borderwidth']
        if not fr_borderwidth: 
            fr_maxwidth = fr_width # Frame has no borderwidth
        else:
            fr_maxwidth = fr_width-fr_borderwidth*2 # Frame has borderwidth
            
        #2. Re-position buttons
        def totalpad( widget, padtype ):
            pad = widget.grid_info().get(padtype)
            if isinstance( pad, int ):
                pad += pad
            elif isinstance( pad, tuple ):
                pad = sum( pad )
            else:
                pad = 0
            return pad
        row = column = rowwidth = 0
        for button in self.buttons:
            # will it fit? If not, move to the next row
            btn_width = button.winfo_width()
            btn_padx = totalpad( button, 'padx' )
            if rowwidth + btn_width > fr_maxwidth:
                row += 1
                column = 0
                rowwidth = 0
            rowwidth += btn_width + btn_padx
            
            button.grid( row=row, column=column,)
            column += 1


    def add_button( self, *args, **kwargs ):
        '''Add one button to the frame'''
        button = ttk.Button( self, *args, **kwargs )
        self.buttons.append( button )
        self._redraw()



class GameGUI(ttk.Frame):

    # GUI Instance attributes
    def __init__( self, master=None, *args, **kw ):

        #print('GameGUI(ttk.Frame).__init__')

        #Create ttk.Frame (i.e. self) with master as it's master.
        super().__init__( master,style='GameGUI.TFrame',width=1569,height=1020 )
        self.grid(row=0, column=0, sticky='nsew')

        #Attributes
        self.master = master
        self.style = None
        self.lifeframe = None
        self.canvas = None
        self.herobuttonsframe = None
        self.giantbuttonsframe = None
        
        self.herolife_name = None
        self.herolife_value = tk.IntVar(value=100)
        self.herolife_bar = None
        self.heroattackbutton = None
        self.herodefendbutton = None
        self.herocrouchingattackbutton = None
        self.herocrouchingdefendbutton = None
        self.herobuttons = None
        self.heroorigin = None
        
        self.giantlife_name = None
        self.giantlife_value = tk.IntVar(value=100)
        self.giantlife_bar = None
        self.giantattackbutton = None
        self.giantdefendbutton = None
        self.giantcrouchingattackbutton = None
        self.giantcrouchingdefendbutton = None
        self.giantbuttons = None
        self.giantorigin = None

        self.nplayers = tk.IntVar(value=1)
        self.player1  = tk.StringVar( value='Secret Coders' )
        #self.player1  = tk.StringVar( value='Dr. One-Zero' )
        self.player2  = tk.StringVar( value=None )
        self.herolife_value = tk.IntVar(value=100)
        self.giantlife_value = tk.IntVar(value=100)
        self.pic_heroattack           = tk.PhotoImage( file='./image/heroattack_w170p.gif' )
        self.pic_herodefend           = tk.PhotoImage( file='./image/herodefend_w170p.gif' )
        self.pic_herocrouchingattack  = tk.PhotoImage( file='./image/herocrouchingattack_w170p.gif' )
        self.pic_herocrouchingdefend  = tk.PhotoImage( file='./image/herocrouchingdefend_w170p.gif' )
        self.pic_herokickingattack    = tk.PhotoImage( file='./image/herokickingattack_h170p.gif' )
        self.pic_herokickingdefend    = tk.PhotoImage( file='./image/herokickingdefend_h170p.gif' )
        self.pic_giantattack          = tk.PhotoImage( file='./image/giantattack_w170p.gif' )
        self.pic_giantdefend          = tk.PhotoImage( file='./image/giantdefend_w170p.gif' )
        self.pic_giantcrouchingattack = tk.PhotoImage( file='./image/giantcrouchingattack_w170p.gif' )
        self.pic_giantcrouchingdefend = tk.PhotoImage( file='./image/giantcrouchingdefend_h170p.gif' )
        self.pic_gianttornadoattack   = tk.PhotoImage( file='./image/gianttornadoattack_h170p.gif' )
        self.pic_gianttornadodefend   = tk.PhotoImage( file='./image/gianttornadodefend_h170p.gif' )
        self.pic_endgame_coders_win_onezero_lose = tk.PhotoImage( file='./image/coders_win_dr_onezero_lose_h400p.gif' )
        self.pic_endgame_coders_lose_onezero_win = tk.PhotoImage( file='./image/coders_lose_dr_onezero_win_h400p_no-yes.gif' )
        self.pic_background_zigzagsky ='./image/battleground2_zigzagsky.gif'
        self.pic_background_clearsky  ='./image/battleground2_clearsky.gif'
        self.pic_background_krash1    ='./image/battleground2_krash1.gif'
        self.pic_background_krash2    ='./image/battleground2_krash2.gif'
        self.pic_background_shatter   ='./image/battleground2_shatter.gif'
        self.sound_crash1 = './sound/Glass_Break.mp3'
        self.sound_crash2 = './sound/Mirror_Breaking.mp3'
        self.sound_g_ouch = [ './sound/giant_Bu_Hu_Hu.m4a',
                              './sound/giant_No.m4a',
                              './sound/giant_Not_Again.m4a',
                              './sound/giant_Ouch_That_Hurts.m4a',
                              './sound/giant_Seriously.m4a',
                              './sound/giant_Seriously.m4a' ]
        self.sound_h_ouch  = [ './sound/hero_Ouch.m4a',
                               './sound/hero_Help_I_Am_Hurt.m4a' ]
        self.sound_ouch1  = './sound/Ouch1.mp3'
        self.sound_ouch2  = './sound/Ouch-sound-effect.mp3'
        self.sound_explode= './sound/Bomb_Exploding-Sound_Explorer-68256487.mp3'

        #Run class instance methods
        self._create_style()
        self._create_frames()
        self._create_players_lives()
        self._create_turtle_screen_and_pens()
        self._create_hero_colorbuttons()
        self._create_giant_colorbuttons()
        self._create_hero_buttons()
        self._create_giant_buttons()
        self._create_endgame_window()
        self._draw_hero_giant()

        #self.master.update_idletasks()
        #rw = self.master.winfo_reqwidth()
        #rh = self.master.winfo_reqheight()
        #w = self.master.winfo_width()
        #h = self.master.winfo_height()
        #print('GAMEGUI rw, rh = ', rw, rh)
        #print('GAMEGUI  w,  h = ',  w,  h)


    def _draw_returnhome( self, pen ):
        #print('pen = ', pen)
        if pen is self.hero_pen:
            origin = self.heroorigin
        elif pen is self.giant_pen:
            origin = self.giantorigin
        else:
            raise Exception('Unknown pen used.')
        pen.pu()
        pen.goto( origin )
        pen.pd()
        pen.st()


    def _draw_hero_giant( self ): 
        self.herostand( startup=True ) #Always show hero at start of game.
        #self.heroattack( startup=True ) #Always show hero at start of game.
        #self.herodefend( startup=True ) #Always show hero at start of game.
        #self.herocrouchingattack( startup=True ) #Always show hero at start of game.
        #self.herocrouchingdefend( startup=True ) #Always show hero at start of game.
        #self.herokickingattack( startup=True ) #Always show hero at start of game.
        #self.herokickingdefend( startup=True ) #Always show hero at start of game.
        self._draw_returnhome( self.hero_pen)
        #self.hero_pen.goto( self.heroorigin )
        #self.hero_pen.pd()
        #self.hero_pen.st()

        self.giantstand( startup=True ) #Always show giant at start of game.
        #self.giantattack( startup=True ) #Always show giant at start of game.
        #self.giantdefend( startup=True ) #Always show giant at start of game.
        #self.giantcrouchingattack( startup=True ) #Always show giant at start of game.
        #self.giantcrouchingdefend( startup=True ) #Always show giant at start of game.
        #self.gianttornadoattack( startup=True ) #Always show giant at start of game.
        #self.gianttornadodefend( startup=True ) #Always show giant at start of game.
        self._draw_returnhome( self.giant_pen)
        #self.giant_pen.pu()
        #self.giant_pen.goto( self.giantorigin )
        #self.giant_pen.pd()
        #self.giant_pen.st()

        #self.master.deiconify()
        #self.showEndGameWindow('Secret Coders')
        #self.showEndGameWindow('Dr. One-Zero')
        pass

        
    def _create_style(self):
        '''Customise GUI styles.'''
        #Initialise ttk Style
        self.style = ttk.Style()

        #Default
        #s.configure( '.', cap=tk.ROUND, join=tk.ROUND, background='#cde1e0' )
        self.style.configure( '.',cap=tk.ROUND,join=tk.ROUND,background=GAMEGUI_BG,
                              font=('Times New Roman','15','bold'))

        #Frames
        #self.style.configure( 'lives.TFrame', relief='raised' , background='pink')
        #self.style.configure( 'herocolors.TFrame', background='orange')
        #self.style.configure( 'giantcolors.TFrame', background='brown')
        #self.style.configure( 'herobtns.TFrame', background='light green')
        #self.style.configure( 'giantbtns.TFrame', background='green')
        self.style.configure( 'lives.TFrame',  relief='raised')
        self.style.configure( 'herocolors.TFrame', )
        self.style.configure( 'giantcolors.TFrame',  )
        self.style.configure( 'herobtns.TFrame' )
        self.style.configure( 'giantbtns.TFrame' )

        #
        #s.configure( 'GameGUI.TFrame',background=GAMEGUI_BG )
        #Lives Bar
        self.style.configure( 'lives.TLabel',
                              #background='white',
                              font=('Times New Roman',20,'bold'), )
        self.style.configure( 'hero.Horizontal.TProgressbar',
                              background=HERO_FG,
                              borderwidth=0,
                              #pbarrelief='raised',troughrelief='sunken', 
                              troughcolor='red', thickness=30, )
        self.style.configure( 'giant.Horizontal.TProgressbar',
                              background=GIANT_FG,
                              borderwidth=0,
                              #pbarrelief='flat', troughrelief='flat',
                              troughcolor='red', thickness=30, )
        #Color Buttons
        self.style.configure( 'color.TFrame',
                              #background='yellow', #relief='flat',
                              borderwidth=5, 
                             )
        #Action Buttons
        self.style.configure( 'battle.TButton',background='#cde1e0',
                              font=('Times New Roman','10','normal'),
                              borderwidth=3, #relief='flat',
                              )
        self.style.configure( 'endgame.TButton',background='#cde1e0',
                              font=('Times New Roman','20','normal'),
                              borderwidth=5, #relief='flat',
                             )
        self.herocolor_stylenames=[]
        for i,color in enumerate( HEROCOLORS ):
            stylename = 'hb'+str(i)+'.TButton'
            self.herocolor_stylenames.append( stylename )
            self.style.configure( stylename, background=color, width=2 )
        self.giantcolor_stylenames=[]
        for i,color in enumerate( GIANTCOLORS ):
            stylename = 'gb'+str(i)+'.TButton'
            self.giantcolor_stylenames.append( stylename )
            self.style.configure( stylename, background=color, width=2 )

        
    def _create_frames(self):
        self.rowconfigure(2, weight=1)

        self.herolifeframe = ttk.Frame(self, style='lives.TFrame')
        self.giantlifeframe = ttk.Frame(self, style='lives.TFrame')
        image = tk.PhotoImage( file=self.pic_background_zigzagsky )
        w = image.width()
        h = image.height()
        self.canvas = tk.Canvas(self, width=w, height=h, bg=GAMEGUI_BG,
                                borderwidth=0 ) 
        self.herocolorsframe = ttk.Frame(self, style='herocolors.TFrame',)
        self.giantcolorsframe = ttk.Frame(self, style='giantcolors.TFrame')
        self.herobuttonsframe = ttk.Frame(self, style='herobtns.TFrame',)
        self.giantbuttonsframe = ttk.Frame(self, style='giantbtns.TFrame',)
        
        self.herolifeframe.grid(    row=0, column=0, sticky='nsew', ipady=6 )
        self.giantlifeframe.grid(   row=0, column=2, sticky='nsew', ipady=6 )
        self.canvas.grid(           row=0, column=1, sticky='nsew', rowspan=3 )
        self.herobuttonsframe.grid( row=1, column=0, sticky='nsew' )
        self.giantbuttonsframe.grid(row=1, column=2, sticky='nsew' )
        self.herocolorsframe.grid(  row=2, column=0, sticky='nsew' )
        self.giantcolorsframe.grid( row=2, column=2, sticky='nsew' )



    def _create_players_lives(self):
        self.herolife_name = ttk.Label( self.herolifeframe,  style='lives.TLabel',
                                        text='SECRET CODERS' )
        self.giantlife_name = ttk.Label( self.giantlifeframe,  style='lives.TLabel',
                                         text='DR. ONE-ZERO' )
        pbarleng=362
        self.herolife_bar = ttk.Progressbar( self.herolifeframe,
                                             length=pbarleng,
                                             mode='determinate',
                                             orient='horizontal',
                                             variable = self.herolife_value,
                                             style='hero.Horizontal.TProgressbar',
                                             )
        self.giantlife_bar = ttk.Progressbar( self.giantlifeframe,
                                              length=pbarleng,
                                              mode='determinate',
                                              orient='horizontal',
                                              variable = self.giantlife_value,
                                              style='giant.Horizontal.TProgressbar',
                                              )
        self.herolife_name.grid( row=0, pady=[20,10] )
        self.herolife_bar.grid(  row=1, sticky='nsew', padx=4, pady=[0,20] )
        self.giantlife_name.grid(row=0, pady=[20,10] )
        self.giantlife_bar.grid( row=1, sticky='nsew', padx=4, pady=[0,20] )


    def _create_hero_colorbuttons(self):
        self.herocolorsframe.columnconfigure( 1, weight=1 )
        
        self.herocolors = FramedButtons( self.herocolorsframe, style='color.TFrame' )
        for i,color in enumerate( HEROCOLORS ):
            self.herocolors.add_button( style=self.herocolor_stylenames[i],
                                         command=lambda color=color:self.set_hero_pen(color) )
            self.herocolors.buttons[i].grid( padx=[5,5], pady=5 )
        self.herocolors.grid( row=0, column=1, sticky='nsew', padx=10, pady=10 )


    def _create_giant_colorbuttons(self):
        self.giantcolorsframe.columnconfigure( 1, weight=1 )
        
        self.giantcolors = FramedButtons( self.giantcolorsframe, style='color.TFrame' )
        for i,color in enumerate( GIANTCOLORS ):
            self.giantcolors.add_button( style=self.giantcolor_stylenames[i],
                                         command=lambda color=color:self.set_giant_pen(color) )
            self.giantcolors.buttons[i].grid( padx=[5,5], pady=5 )
        self.giantcolors.grid( row=0, column=1, sticky='nsew', padx=10, pady=10 )


    def _create_hero_buttons(self):
        self.heroattackbutton=ttk.Button(
            self.herobuttonsframe, style='battle.TButton',
            image=self.pic_heroattack, command=self.heroattack,
            )
        self.herodefendbutton=ttk.Button(
            self.herobuttonsframe, style='battle.TButton',
            image=self.pic_herodefend, command=self.herodefend,
            )
        self.herocrouchingattackbutton=ttk.Button(
            self.herobuttonsframe, style='battle.TButton',
            image=self.pic_herocrouchingattack,
            command=self.herocrouchingattack,
            )
        self.herocrouchingdefendbutton=ttk.Button(
            self.herobuttonsframe, style='battle.TButton',
            image=self.pic_herocrouchingdefend,
            command=self.herocrouchingdefend,
            )
        self.herokickingattackbutton=ttk.Button(
            self.herobuttonsframe, style='battle.TButton',
            image=self.pic_herokickingattack,
            command=self.herokickingattack,
            )
        self.herokickingdefendbutton=ttk.Button(
            self.herobuttonsframe, style='battle.TButton',
            image=self.pic_herokickingdefend,
            command=self.herokickingdefend,
            )

        self.heroattackbutton.grid(         row=0, column=1, sticky='nsew')
        self.herodefendbutton.grid(         row=0, column=0, sticky='nsew')
        self.herocrouchingattackbutton.grid(row=1, column=1, sticky='nsew')
        self.herocrouchingdefendbutton.grid(row=1, column=0, sticky='nsew')
        self.herokickingattackbutton.grid(  row=2, column=1, sticky='nsew')
        self.herokickingdefendbutton.grid(  row=2, column=0, sticky='nsew')

        self.herobuttons = ( self.heroattackbutton,
                             self.herodefendbutton,
                             self.herocrouchingattackbutton,
                             self.herocrouchingdefendbutton,
                             self.herokickingattackbutton,
                             self.herokickingdefendbutton,
                             )


    def _create_giant_buttons(self):
        self.giantattackbutton=ttk.Button(
            self.giantbuttonsframe, style='battle.TButton',
            image=self.pic_giantattack, command=self.giantattack,
            )
        self.giantdefendbutton=ttk.Button(
            self.giantbuttonsframe, style='battle.TButton',
            image=self.pic_giantdefend, command=self.giantdefend,
            )
        self.giantcrouchingattackbutton=ttk.Button(
            self.giantbuttonsframe, style='battle.TButton',
            image=self.pic_giantcrouchingattack, 
            command=self.giantcrouchingattack,
            )
        self.giantcrouchingdefendbutton=ttk.Button(
            self.giantbuttonsframe, style='battle.TButton',
            image=self.pic_giantcrouchingdefend,
            command=self.giantcrouchingdefend,
            )
        self.gianttornadoattackbutton=ttk.Button(
            self.giantbuttonsframe, style='battle.TButton',
            image=self.pic_gianttornadoattack,
            command=self.gianttornadoattack,
            )
        self.gianttornadodefendbutton=ttk.Button(
            self.giantbuttonsframe, style='battle.TButton',
            image=self.pic_gianttornadodefend,
            command=self.gianttornadodefend,
            )
        self.giantattackbutton.grid(          row=0, column=0, sticky='nsew')
        self.giantdefendbutton.grid(          row=0, column=1, sticky='nsew')
        self.giantcrouchingattackbutton.grid( row=1, column=0, sticky='nsew')
        self.giantcrouchingdefendbutton.grid( row=1, column=1, sticky='nsew')
        self.gianttornadoattackbutton.grid(   row=2, column=0, sticky='nsew')
        self.gianttornadodefendbutton.grid(   row=2, column=1, sticky='nsew')

        self.giantbuttons = ( self.giantattackbutton,
                              self.giantdefendbutton,
                              self.giantcrouchingattackbutton,
                              self.giantcrouchingdefendbutton,
                              self.gianttornadoattackbutton,
                              self.gianttornadodefendbutton,
                              )


    def _create_turtle_screen_and_pens(self):
        self.screen = tt.TurtleScreen( self.canvas )
        self.screen.mode( 'logo' )
        self.screen.bgpic( self.pic_background_zigzagsky )
        self.screen.bgcolor( GAMEGUI_BG )
        
        self.hero_pen = tt.RawTurtle( self.screen )
        self.hero_pen.ht()
        self.hero_pen.color( HERO_FG )
        self.hero_pen.speed( 0 )
        self.hero_pen.pensize( 12 )
        self.hero_pen.shape( 'triangle' )

        self.giant_pen = tt.RawTurtle( self.screen )
        self.giant_pen.ht()
        self.giant_pen.color( GIANT_FG )
        self.giant_pen.speed( 0 )
        self.giant_pen.pensize( 12 )
        self.giant_pen.shape( 'triangle' )


    def _create_endgame_window(self):
        self.endgamewindow = tk.Toplevel(self, background='#cde1e0')
        self.endgamewindow.transient( self ) #For short-lived pop-up windows. Appears in front of its parent and is iconified with parent window.
        self.endgamewindow.wm_attributes('-type', 'splash') #Removes title bar from window.
        self.endgamewindow.withdraw()
        self.endgame_pic_coders_win_onezero_lose = ttk.Label(
            self.endgamewindow, image=self.pic_endgame_coders_win_onezero_lose )
        self.endgame_pic_coders_lose_onezero_win = ttk.Label(
            self.endgamewindow, image=self.pic_endgame_coders_lose_onezero_win )
        self.endgame_replay = ttk.Button(
            self.endgamewindow, text='Re-Play', command=self.replay,
            style='endgame.TButton' )
        self.endgame_intropage = ttk.Button(
            self.endgamewindow, text='IntroPage', command=self.gotoIntroPage,
            style='endgame.TButton' )

        self.endgame_pic_coders_win_onezero_lose.grid(row=0, column=0, columnspan=2)
        self.endgame_pic_coders_lose_onezero_win.grid(row=1, column=0, columnspan=2)
        self.endgame_replay.grid(row=2, column=0)
        self.endgame_intropage.grid(row=2, column=1)
        

    def setButtonsState(self, buttons, disabled=False):
        if disabled:
            for button in buttons:
                button.state(['disabled'])   # Disable the button.
        elif not disabled:
            for button in buttons:
                button.state(['!disabled'])  # Enable the button.
        else:
            raise 'Exception in setButtonsState method: Invalid "disabled" value.'
            

    def runOnePlayer( self,player ):
        #print('\ndef runOnePlayer( self,player ):')
        #print('player = ', player)
        self.setButtonsState( self.herobuttons, disabled=True ) #Disabled
        self.setButtonsState( self.giantbuttons, disabled=True ) #Disabled
        self.screen.bgpic( self.pic_background_zigzagsky )
        self.hero_pen.clear()
        self.giant_pen.clear()
        self.setHeroGiantOrigins()
        self.giantstand( startup=True ) #Always show giant at start of game.
        self.herostand( startup=True ) #Always show giant at start of game.
        if player == 'Secret Coders':
            self.setButtonsState( self.herobuttons, disabled=False ) #Enabled
        elif player == 'Dr. One-Zero':
            self.setButtonsState( self.giantbuttons, disabled=False )#Enabled
        self.update_idletasks()
        

    def runTwoPlayers( self,player1,player2 ):
        #print('\ndef runTwoPlayers( self,player1,player2 ):')
        #if player1 == 'Secret Coders':
        #    self.setButtonsState(self.giantbuttons, disabled=True)
        #elif player1 == 'Dr. One-Zero':
        #    self.setButtonsState(self.herobuttons, disabled=True)
        self.screen.bgpic( self.pic_background_zigzagsky )
        self.hero_pen.clear()
        self.giant_pen.clear()
        self.giantstand() #Always show giant at start of game.
        self.update_idletasks()


    def getGiantAction( self ):
        #print('\ndef getGiantAction(self):')
        giant_actions = [ self.giantstand,
                          self.giantattack,
                          self.giantdefend,
                          self.giantcrouchingattack,
                          self.giantcrouchingdefend,
                          self.gianttornadoattack,
                          self.gianttornadodefend,
                        ]
        giant_action = random.choice( giant_actions )
        #print('giant_action = ', giant_action.__name__)
        return giant_action
        

    def getHeroAction( self ):
        #print('\ndef getHeroAction(self):')
        hero_reactions = [ self.herostand,
                           self.heroattack,
                           self.herodefend,
                           self.herocrouchingattack,
                           self.herocrouchingdefend,
                           self.herokickingattack,
                           self.herokickingdefend,
                        ]
        hero_reaction = random.choice( hero_reactions )
        #print('hero_reaction = ', hero_reaction.__name__)
        return hero_reaction


    def setHeroGiantOrigins( self,heroactionname=None,giantactionname=None):
        #print('def setHeroGiantOrigins( self,heroactionname=None,giantactionname=None):')

        if not heroactionname and not giantactionname:
            #print('Default Origin')
            self.heroorigin = (-379,-420)
            self.giantorigin = (379,-420)
            #self.heroorigin = (-390,-480) #debug
            #self.giantorigin = (325,-90) #debug
            
        else:
            if heroactionname in 'herostand':
                #print('herostand Default Origins')
                self.heroorigin = (-379,-420)
                self.giantorigin = (379,-420)                
                if giantactionname in 'giantcrouchingattack':
                    #print('herostand vs giantcrouchingattack')
                    self.giantorigin = (514,-420)
                elif giantactionname in 'giantcrouchingdefend':
                    #print('herostand vs giantcrouchingdefend')
                    self.giantorigin = (500,-420)
                elif giantactionname in 'gianttornadoattack':
                    #print('herostand vs gianttornadoattack')
                    self.giantorigin = (325,-90)
                elif giantactionname in 'gianttornadodefend':
                    #print('herostand vs gianttornadodefend')
                    self.giantorigin = (225,-350)

            elif heroactionname in 'heroattack':
                #print('heroattack Default Origins')
                self.heroorigin = (-379,-420)
                self.giantorigin = (379,-420)
                if giantactionname in 'giantattack':
                    #print('heroattack vs giantattack')
                    self.heroorigin = (-439,-420)
                    self.giantorigin = (439,-420)
                elif giantactionname in 'giantdefend':
                    #print('heroattack vs giantdefend')
                    self.heroorigin = (-399,-420)
                    self.giantorigin = (399,-420)
                elif giantactionname in 'giantcrouchingattack':
                    #print('heroattack vs giantcrouchingattack')
                    self.heroorigin = (-397,-420)
                    self.giantorigin = (397,-420)
                elif giantactionname in 'giantcrouchingdefend':
                    #print('heroattack vs giantcrouchingdefend')
                    self.giantorigin = (500,-420)
                elif giantactionname in 'gianttornadoattack':
                    #print('heroattack vs gianttornadoattack')
                    self.heroorigin = (-426,-420)
                    self.giantorigin = (400,-90)
                elif giantactionname in 'gianttornadodefend':
                    #print('heroattack vs gianttornadodefend')
                    self.giantorigin = (340,-350)
        
            elif heroactionname in 'herodefend':
                ##print('herodefend Default Origins')
                self.heroorigin = (-379,-420)
                self.giantorigin = (379,-420)
                if giantactionname in 'giantattack':
                    #print('herodefend vs giantattack')
                    self.heroorigin = (-399,-420)
                    self.giantorigin = (399,-420)
                elif giantactionname in 'giantcrouchingattack':
                    #print('herodefend vs giantcrouchingattack')
                    self.giantorigin = (405,-420)
                elif giantactionname in 'giantcrouchingdefend':
                    #print('herodefend vs giantcrouchingdefend')
                    self.giantorigin = (500,-420)
                elif giantactionname in 'gianttornadoattack':
                    #print('herodefend vs gianttornadoattack')
                    self.giantorigin = (366,-90)
                elif giantactionname in 'gianttornadodefend':
                    #print('herodefend vs gianttornadodefend')
                    self.giantorigin = (260,-350)
                    
            elif heroactionname in 'herocrouchingattack':
                #print('herocrouchingattack Default Origins')
                self.heroorigin = (-410,-420)
                self.giantorigin = (379,-420)
                if giantactionname in 'giantstand':
                    #print('herocrouchingattack vs giantstand')
                    self.heroorigin = (-439,-420)
                    self.giantorigin = (450,-420)
                elif giantactionname in 'giantcrouchingattack':
                    #print('herocrouchingattack vs giantcrouchingattack')
                    self.heroorigin = (-570,-420)
                    self.giantorigin = (570,-420)
                elif giantactionname in 'giantcrouchingdefend':
                    #print('herocrouchingattack vs giantcrouchingdefend')
                    self.heroorigin = (-505,-420)
                    self.giantorigin = (505,-420)
                elif giantactionname in 'gianttornadoattack':
                    #print('herocrouchingattack vs gianttornadoattack')
                    self.heroorigin = (-390,-480)
                    self.giantorigin = (325,-90)
                elif giantactionname in 'gianttornadodefend':
                    #print('herocrouchingattack vs gianttornadodefend')
                    self.heroorigin = (-500,-420)
                    self.giantorigin = (355,-350)

            elif heroactionname in 'herocrouchingdefend':
                #print('herocrouchingdefend Default Origins')
                self.heroorigin = (-500,-420)
                self.giantorigin = (379,-420)
                if giantactionname in 'giantcrouchingattack':
                    #print('herocrouchingdefend vs giantcrouchingattack')
                    self.giantorigin = (500,-420)
                elif giantactionname in 'giantcrouchingdefend':
                    #print('herocrouchingdefend vs giantcrouchingdefend')
                    self.giantorigin = (500,-420)
                elif giantactionname in 'gianttornadoattack':
                    #print('herocrouchingdefend vs gianttornadoattack')
                    self.heroorigin = (-500,-480)
                    self.giantorigin = (320,-90)
                elif giantactionname in 'gianttornadodefend':
                    #print('herocrouchingdefend vs gianttornadodefend')
                    self.giantorigin = (305,-350)

            elif heroactionname in 'herokickingattack':
                #print('herokickingattack Default Origins')
                self.heroorigin = (-470,-420)
                self.giantorigin = (440,-420)

                if giantactionname in 'giantstand':
                    #print('herokickingattack vs giantstand')
                    self.heroorigin = (-550,-420)
                    self.giantorigin = (425,-420)
                elif giantactionname in 'giantcrouchingattack':
                    #print('herokickingattack vs giantcrouchingattack')
                    self.heroorigin = (-570,-420)
                    self.giantorigin = (540,-420)
                elif giantactionname in 'giantcrouchingdefend':
                    #print('herokickingattack vs giantcrouchingdefend')
                    self.heroorigin = (-570,-420)
                    self.giantorigin = (540,-420)
                elif giantactionname in 'gianttornadoattack':
                    #print('herokickingattack vs gianttornadoattack')
                    self.heroorigin = (-500,-420)
                    self.giantorigin = (300,-90)
                elif giantactionname in 'gianttornadodefend':
                    #print('herokickingattack vs gianttornadodefend')
                    self.heroorigin = (-500,-420)
                    self.giantorigin = (325,-350)

            elif heroactionname in 'herokickingdefend':
                #print('herokickingdefend Default Origins')
                self.heroorigin = (-575,-420)
                self.giantorigin = (400,-420)
                if giantactionname in 'giantstand':
                    #print('herokickingdefend vs giantstand')
                    self.heroorigin = (-510,-420)
                elif giantactionname in 'giantattack':
                    #print('herokickingdefend vs giantattack')
                    self.heroorigin = (-555,-420)
                    self.giantorigin = (465,-420)
                elif giantactionname in 'giantdefend':
                    #print('herokickingdefend vs giantdefend')
                    self.heroorigin = (-538,-420)
                elif giantactionname in 'giantcrouchingattack':
                    #print('herokickingdefend vs giantcrouchingattack')
                    self.giantorigin = (575,-420)
                elif giantactionname in 'giantcrouchingdefend':
                    #print('herokickingdefend vs giantcrouchingdefend')
                    self.giantorigin = (535,-420)
                elif giantactionname in 'gianttornadoattack':
                    #print('herokickingdefend vs gianttornadoattack')
                    self.giantorigin = (390,-90)
                elif giantactionname in 'gianttornadodefend':
                    #print('herokickingdefend vs gianttornadodefend')
                    self.heroorigin = (-540,-420)
                    self.giantorigin = (320,-350)


    def setLifePoints( self,heroactionname,giantactionname  ):
        #print('\ndef setLifePoints( self ):')
        #1. Get players actions 
        hero_action = heroactionname
        giant_action = giantactionname
        krash1 = self.pic_background_krash1
        krash2 = self.pic_background_krash2 #Need krash2
        crash1 = self.sound_crash1
        crash2 = self.sound_crash2
        ouch1  = random.choice( self.sound_h_ouch )
        ouch2  = random.choice( self.sound_g_ouch )
        #explode= self.sound_explode

        def heroLoose():
            playsound(ouch1)
            self.hll()
            
        def giantLoose():
            playsound(ouch2)
            self.gll()
        
        def heroDefend():
            self.screen.bgpic(krash1)
            self.canvas.update_idletasks()
            playsound(crash1)
            
        def giantDefend():
            self.screen.bgpic(krash2)
            self.canvas.update_idletasks()
            playsound(crash2)
            
        #2. Deduct lifepoints according to rules
        if hero_action == 'herostand':
            if giant_action == 'giantattack':
                #print('herostand vs giantattack')
                heroLoose()
            elif giant_action == 'giantcrouchingattack':
                #print('herostand vs giantcrouchingattack')
                heroLoose()
            elif giant_action == 'gianttornadoattack':
                #print('herostand vs gianttornadoattack')
                heroLoose()
            elif giant_action == 'gianttornadodefend':
                #print('herostand vs gianttornadodefend')
                heroLoose()
                
        elif hero_action == 'heroattack':
            if giant_action == 'giantstand':
                #print('heroattack vs giantstand')
                giantLoose()
            elif giant_action == 'giantattack':
                #print('heroattack vs giantattack')
                if self.player1 == 'Secret Coders':
                    giantLoose()
                    heroLoose()
                else:
                    heroLoose()
                    giantLoose()
            elif giant_action == 'giantdefend':
                #print('heroattack vs giantdefend')
                giantDefend()
            elif giant_action == 'giantcrouchingattack':
                #print('heroattack vs giantcrouchingattack')
                heroLoose()
            elif giant_action == 'giantcrouchingdefend':
                #print('heroattack vs giantcrouchingdefend')
                giantDefend()
            elif giant_action == 'gianttornadoattack':
                #print('herostand vs gianttornadoattack')
                if self.player1 == 'Secret Coders':
                    giantLoose()
                    heroLoose()
                else:
                    heroLoose()
                    giantLoose()
            elif giant_action == 'gianttornadodefend':
                #print('herostand vs gianttornadodefend')
                giantDefend()

        elif hero_action == 'herodefend':
            if giant_action == 'giantattack':
                #print('herodefend vs giantattack')
                heroDefend()
            elif giant_action == 'giantcrouchingattack':
                #print('herodefend vs giantcrouchingattack')
                heroLoose()
            elif giant_action == 'gianttornadoattack':
                #print('herostand vs gianttornadoattack')
                if self.player1 == 'Secret Coders':
                    giantDefend()
                    heroDefend()
                else:
                    heroDefend()
                    giantDefend()
            elif giant_action == 'gianttornadodefend':
                #print('herostand vs gianttornadodefend')
                if self.player1 == 'Secret Coders':
                    giantDefend()
                    heroDefend()
                else:
                    heroDefend()
                    giantDefend()
                
        elif hero_action == 'herocrouchingattack':
            if giant_action == 'giantstand':
                #print('herocrouchingattack vs giantstand')
                giantLoose()
            elif giant_action == 'giantattack':
                #print('herocrouchingattack vs giantattack')
                giantLoose()
            elif giant_action == 'giantdefend':
                #print('herocrouchingattack vs giantdefend')
                giantLoose()
            elif giant_action == 'giantcrouchingattack':
                #print('herocrouchingattack vs giantcrouchingattack')
                if self.player1 == 'Secret Coders':
                    giantLoose()
                    heroLoose()
                else:
                    heroLoose()
                    giantLoose()
            elif giant_action == 'giantcrouchingdefend':
                #print('herocrouchingattack vs giantcrouchingattack')
                if self.player1 == 'Secret Coders':
                    giantDefend()
                    heroDefend()
                else:
                    heroDefend()
                    giantDefend() 
            elif giant_action == 'gianttornadoattack':
                #print('herocrouchingattack vs gianttornadoattack')
                heroLoose()
            elif giant_action == 'gianttornadodefend':
                #print('herocrouchingattack vs gianttornadodefend')
                heroDefend()

        elif hero_action == 'herocrouchingdefend':
            if giant_action == 'giantattack':
                #print('herocrouchingdefend vs giantattack')
                heroDefend()
            elif giant_action == 'giantcrouchingattack':
                #print('herocrouchingdefend vs giantcrouchingattack')
                heroDefend()
            elif giant_action == 'gianttornadoattack':
                #print('herostand vs gianttornadoattack')
                heroDefend()
            elif giant_action == 'gianttornadodefend':
                #print('herostand vs gianttornadodefend')
                heroLoose()
                
        elif hero_action == 'herokickingattack':
            if giant_action == 'giantstand':
                #print('heroattack vs giantstand')
                giantLoose()
            elif giant_action == 'giantattack':
                #print('heroattack vs giantattack')
                giantLoose()
            elif giant_action == 'giantdefend':
                #print('heroattack vs giantdefend')
                giantLoose()
            elif giant_action == 'giantcrouchingattack':
                #print('herostand vs giantcrouchingattack')
                giantLoose()
            elif giant_action == 'giantcrouchingdefend':
                #print('herocrouchingattack vs giantcrouchingattack')
                giantLoose()
            elif giant_action == 'gianttornadoattack':
                #print('herostand vs gianttornadoattack')
                heroLoose()
            elif giant_action == 'gianttornadodefend':
                #print('herostand vs gianttornadodefend')
                heroLoose()

        elif hero_action == 'herokickingdefend':
            if giant_action == 'giantstand':
                #print('heroattack vs giantstand')
                giantLoose()
            elif giant_action == 'giantattack':
                #print('heroattack vs giantattack')
                heroDefend()
            elif giant_action == 'giantdefend':
                #print('heroattack vs giantdefend')
                heroDefend()
                giantDefend()
            elif giant_action == 'giantcrouchingattack':
                #print('herostand vs giantcrouchingattack')
                heroDefend()
            elif giant_action == 'giantcrouchingdefend':
                #print('herocrouchingattack vs giantcrouchingdefend')
                giantLoose()
            elif giant_action == 'gianttornadoattack':
                #print('herostand vs gianttornadoattack')
                heroDefend()
            elif giant_action == 'gianttornadodefend':
                #print('herostand vs gianttornadodefend')
                heroDefend()
                giantDefend()

        else:
            #print('hero_action = ', hero_action)
            #print('giant_action = ', giant_action)
            raise Exception('###Outcome has not been specified.')

    def hll(self):
        currentlife = self.herolife_value.get()
        newlife = currentlife - LIFEPOINTS
        self.herolife_value.set(value=newlife)


    def gll(self):
        currentlife = self.giantlife_value.get()
        newlife = currentlife - LIFEPOINTS
        self.giantlife_value.set(value=newlife)


    def checkEndOfLife( self ):
        #Check for end of life
        if self.herolife_value.get() <= 0 and self.giantlife_value.get() > 0:
            self.heroshatter()
            return True
        elif self.herolife_value.get() > 0 and self.giantlife_value.get() <= 0:
            self.giantshatter()
            return True
        elif self.herolife_value.get() <= 0 and self.giantlife_value.get() <= 0:
            self.herogiantshatter()
            return True
        else:
            return False


    def shatter(self):
        #print('def shatter(self):')
        self.screen.bgpic( self.pic_background_shatter )
        self.canvas.update_idletasks()
        playsound( self.sound_explode )
        

    def heroshatter(self):
        #print('heroshatter')
        heroorigin = (-379,-420)
        HeroShatter( self.screen,self.hero_pen,heroorigin ).animate()
        self.shatter()
        self.after( 5000, lambda:self.showEndGameWindow('Secret Coders') )

        
    def giantshatter(self):
        #print('giantshatter')
        giantorigin = (379,-420)
        GiantShatter( self.screen,self.giant_pen,giantorigin ).animate()
        self.shatter()
        self.after( 5000, lambda:self.showEndGameWindow('Dr. One-Zero') )


    def herogiantshatter(self):
        #print('herogiantshatter')
        heroorigin = (-379,-420)
        giantorigin = (379,-420)
        HeroShatter( self.screen,self.hero_pen,heroorigin ).animate()
        GiantShatter( self.screen,self.giant_pen,giantorigin ).animate()
        self.shatter()
        self.after( 5000, lambda:self.showEndGameWindow('Dr. One-Zero' ))


    def replay(self):
        #print( '\ndef replay(self):' )
        self.endgamewindow.withdraw()
        self.herolife_value.set( value=100 )
        self.giantlife_value.set( value=100 )
        if self.nplayers.get() == 1:
            #print( 'run self.runOnePlayer()' )
            self.runOnePlayer( self.player1.get() )
        elif self.nplayers.get() == 2:
            #print( 'run self.twoplayer()' )
            self.runTwoPlayers( self.player1.get(), self.player2.get() )
        else:
            raise Exception( 'Method replay: Invalid self.nplayers values' )


    def reset( self ):
        #print( 'def reset(self):' )
        self.nplayers.set( value=1 )
        self.player1.set(  value=None )
        self.player2.set(  value=None )
        self.herolife_value.set(  value=100 )
        self.giantlife_value.set( value=100 )
        self.setButtonsState( self.herobuttons, disabled=False )
        self.setButtonsState( self.giantbuttons, disabled=False )
        self.screen.bgpic( self.pic_background_zigzagsky )
        self.hero_pen.clear()
        self.giant_pen.clear()
        

    def gotoIntroPage(self):
        #print('\ndef gotoIntroPage(self):')
        self.endgamewindow.withdraw()
        self.master._show_GUI("IntroGUI")
        self.reset()
        #print('self.master.__dir__ =', self.master.__dir__)
        #print('self.master.winfo_children() = ', self.master.winfo_children())

        
    def showEndGameWindow(self, shatter):
        #print('def showEndGameWindow(self):')
        #1.Position EndGameWindow relative to RootWindow 
        root = self.winfo_toplevel()
        root.update_idletasks()
        rootX = root.winfo_rootx() # int type
        rootY = root.winfo_rooty() # int type
        #print('rootX = ', rootX)
        #print('rootY = ', rootY)
        egwX = str( rootX+560 )
        egwY = str( rootY+5 )
        self.endgamewindow.geometry( '+{}+{}'.format(egwX,egwY) )

        canvas_height = self.canvas.winfo_height()
        canvas_width = self.canvas.winfo_width()
        #print('canvas_width={}, canvas_height={}'.format(canvas_width,canvas_height))

        #2. Show image based on which player has shattered.
        if shatter == 'Secret Coders':
            self.endgame_pic_coders_win_onezero_lose.grid_remove()
            self.endgame_pic_coders_lose_onezero_win.grid()
        elif shatter == 'Dr. One-Zero':
            self.endgame_pic_coders_win_onezero_lose.grid()
            self.endgame_pic_coders_lose_onezero_win.grid_remove()
        elif shatter == 'Both':
            self.endgame_pic_coders_win_onezero_lose.grid_remove()
            self.endgame_pic_coders_lose_onezero_win.grid_remove()
        else:
            raise Exception('Invalid "winner" arg value used.')
        #3. Show EndGameWindow
        self.endgamewindow.deiconify()
        self.endgamewindow.lift()


    ############################################################################
    #Commands
    ############################################################################
    def set_hero_pen( self, color ):
        self.hero_pen.color( color )
        self.style.configure( 'hero.Horizontal.TProgressbar', background=color )


    def set_giant_pen( self, color ):
        self.giant_pen.color( color )
        self.style.configure( 'giant.Horizontal.TProgressbar', background=color )


    @set_herobutton
    def herostand( self ):
        pen=self.hero_pen
        pen.pu()
        pen.home()
        pen.clear()
        self.hero_drawlegs()
        self.hero_drawtorsostand()
        self.hero_drawhead()

       
    @set_herobutton
    def heroattack( self ):
        pen=self.hero_pen
        pen.pu()
        pen.home()
        pen.clear()
        self.hero_drawlegs()
        self.hero_drawtorsopunch()
        self.hero_drawhead()


    @set_herobutton
    def herodefend( self ):
        pen=self.hero_pen
        pen.pu()
        pen.home()
        pen.clear()
        self.hero_drawlegs()
        self.hero_drawtorsoblock()
        self.hero_drawhead()


    @set_herobutton
    def herocrouchingattack( self ):
        pen=self.hero_pen
        pen.pu()
        pen.home()
        pen.clear()
        self.hero_drawcrouchinglegs( defend=False )
        self.hero_drawtorsopunch()
        self.hero_drawhead()


    @set_herobutton
    def herocrouchingdefend( self ):
        pen=self.hero_pen
        pen.pu()
        pen.home()
        pen.clear()
        self.hero_drawcrouchinglegs( defend=True  )
        self.hero_drawtorsoblock()
        self.hero_drawhead()


    @set_herobutton
    def herokickingattack( self ):
        pen=self.hero_pen
        pen.pu()
        pen.home()
        pen.clear()
        self.hero_drawkickinglegs()
        self.hero_drawtorsopunch()
        self.hero_drawhead()


    @set_herobutton
    def herokickingdefend( self ):
        pen=self.hero_pen
        pen.pu()
        pen.home()
        pen.clear()
        self.hero_drawkickinglegs()
        self.hero_drawtorsoblock()
        self.hero_drawhead()


    @set_giantbutton
    def giantstand( self ):
        pen=self.giant_pen
        pen.clear()
        self.giant_drawlegs()
        self.giant_drawtorsostand()
        self.giant_drawhead()


    @set_giantbutton
    def giantattack( self ):
        pen=self.giant_pen
        pen.clear()
        self.giant_drawlegs()
        self.giant_drawtorsopunchleft()
        self.giant_drawhead()


    @set_giantbutton
    def giantdefend( self ):
        pen=self.giant_pen
        pen.clear()
        self.giant_drawlegs()
        self.giant_drawtorsoblockleft()
        self.giant_drawhead()


    @set_giantbutton
    def giantcrouchingattack( self ):
        pen=self.giant_pen
        pen.clear()
        self.giant_drawcrouchinglegs()
        self.giant_drawtorsopunchleft()
        self.giant_drawhead()


    @set_giantbutton
    def giantcrouchingdefend( self ):
        pen=self.giant_pen
        pen.clear()
        self.giant_drawcrouchinglegs( position='defend' )
        self.giant_drawtorsoblockleft()
        self.giant_drawhead()


    @set_giantbutton
    def gianttornadoattack( self ):
        pen=self.giant_pen
        pen.clear()
        self.giant_drawtornadokicklegs()
        self.giant_drawtorsopunchleft()
        self.giant_drawhead()
        

    @set_giantbutton
    def gianttornadodefend( self ):
        pen=self.giant_pen
        pen.clear()
        self.giant_drawtornadokicklegs()
        self.giant_drawtorsoblockleft()
        self.giant_drawhead()
        

    #============================================
    #hero
    #============================================
    def hero_drawhead( self ):
        pen=self.hero_pen
        pen.pd()
        for _ in range(4): #head
            pen.fd(145)
            pen.rt(90)
        pen.pu()
        for _ in range(1): #spectacles
            pen.fd(50)
            pen.rt(90)
            pen.fd(50)
            pen.pd()
            pen.fd(45) # draw mouth
            pen.pu()
            pen.bk(35)
            pen.lt(90)
            pen.fd(50)
            pen.rt(90)
            pen.pd()
            pen.fd(25)
            pen.pu()
        pen.bk(65)
        pen.lt(90)
        pen.fd(20)
        pen.rt(90)
        for _ in range(2):
            pen.pd()
            for i in range(4):
                pen.fd(40)
                pen.rt(90)
            pen.pu()
            pen.fd(65)
        pen.bk(150)
        pen.lt(90)
        pen.bk(120)
        pen.pu()
        pen.goto( self.heroorigin )
        pen.pd()


    def hero_drawfingers( self ):
        pen=self.hero_pen
        for i in range(3):
            pen.fd(25)
            pen.rt(90)
            pen.fd(30)
            pen.bk(30)
            pen.lt(90)
        

    def hero_drawtorsostand( self ):
        pen=self.hero_pen
        pen.pd()
        #pen.begin_fill()
        pen.fd(200)
        pen.lt(90)
        pen.fd(25)
        pen.lt(90)
        pen.fd(195)
        pen.rt(90)
        self.hero_drawfingers()
        pen.rt(90)
        pen.fd(280)
        pen.rt(90)
        pen.fd(395)
        pen.rt(90)
        pen.fd(280)
        pen.rt(90)
        self.hero_drawfingers()
        pen.rt(90)
        pen.fd(195)
        pen.lt(90)
        pen.fd(25)
        pen.lt(90)
        pen.fd(200)
        pen.rt(90)
        pen.fd(195)
        pen.rt(90)
        #pen.end_fill()
        pen.pu()
        pen.fd(285)
        pen.rt(90)
        pen.fd(25)
        pen.lt(90)


    def hero_drawtorsopunch( self ):
        pen=self.hero_pen
        pen.pd()
        #pen.begin_fill()
        pen.fd(200)
        pen.lt(90)
        pen.fd(25)
        pen.lt(90)
        pen.fd(195)
        pen.rt(90)
        self.hero_drawfingers()
        pen.rt(90)
        pen.fd(280)
        pen.rt(90)
        pen.fd(515)
        pen.rt(90)
        self.hero_drawfingers()
        pen.rt(90)
        pen.fd(220)
        pen.lt(90)
        pen.fd(210)
        pen.rt(90)
        pen.fd(195)
        pen.rt(90)
        #pen.end_fill()
        pen.pu()
        pen.fd(285)
        pen.rt(90)
        pen.fd(25)
        pen.lt(90)


    def hero_drawtorsoblock( self ):
        pen=self.hero_pen
        pen.pd()
        #pen.begin_fill()
        pen.fd(200)
        pen.lt(90)
        pen.fd(25)
        pen.lt(90)
        pen.fd(195)
        pen.rt(90)
        self.hero_drawfingers()
        pen.rt(90)
        pen.fd(280)
        pen.rt(90)
        pen.fd(360)
        pen.lt(90)
        pen.fd(150)
        pen.rt(90)
        self.hero_drawfingers()
        pen.rt(90)
        pen.fd(225)
        pen.rt(90)
        pen.fd(140)
        pen.lt(90)
        pen.fd(210)
        pen.rt(90)
        pen.fd(195)
        pen.rt(90)
        #pen.end_fill()
        pen.pu()
        pen.fd(285)
        pen.rt(90)
        pen.fd(25)
        pen.lt(90)


    def hero_drawlegs( self ):
        pen=self.hero_pen
        pen.pu()
        pen.goto( self.heroorigin )
        pen.pd()
        #pen.begin_fill()
        pen.rt(45)
        pen.fd(25)
        pen.lt(45)
        pen.fd(220)
        pen.rt(90)
        pen.fd(195)
        pen.rt(90)
        pen.fd(220)
        pen.lt(45)
        pen.fd(25)
        pen.rt(135)
        pen.fd(85)
        pen.rt(90)
        pen.fd(170)
        pen.lt(90)
        pen.fd(60)
        pen.lt(90)
        pen.fd(170)
        pen.rt(90)
        pen.fd(85)
        pen.rt(90)
        #pen.end_fill()
        pen.pu() #goto body
        pen.fd(238)
        pen.rt(90)
        pen.fd(18)
        pen.lt(90)


    def hero_drawcrouchinglegs( self, defend=True ):
        pen=self.hero_pen
        pen.pu()
        pen.goto( self.heroorigin )
        pen.pd() #drawcrouchinglegs
        #pen.begin_fill()
        pen.rt(45)
        pen.fd(25)
        pen.lt(45)
        pen.fd(140)
        pen.rt(90)
        pen.fd(395)
        pen.rt(90)
        pen.fd(140)
        pen.lt(45)
        pen.fd(25)
        pen.rt(135)
        pen.fd(85)
        pen.rt(90)
        pen.fd(100)
        pen.lt(90)
        pen.fd(260)
        pen.lt(90)
        pen.fd(100)
        pen.rt(90)
        pen.fd(85)
        pen.rt(90)
        #pen.end_fill()
        pen.pu() #goto body
        if defend:
            x=100
        else:
            x=152
        pen.fd(158)
        pen.rt(90)
        pen.fd(x)
        pen.lt(90)


    def hero_drawkickinglegs( self ):
        pen=self.hero_pen
        pen.pu()
        pen.goto( self.heroorigin )
        pen.pd()
        pen.fd(85)
        pen.rt(135)
        pen.fd(25)
        pen.lt(45)
        pen.fd(635)
        pen.lt(45)
        pen.fd(25)
        pen.rt(135)
        pen.fd(85)
        pen.rt(90)
        pen.fd(669)
        pen.rt(90)
        pen.pu()
        pen.fd(68)
        pen.rt(90)
        pen.fd(237)
        pen.lt(90)
        
    #============================================
    #giant
    #============================================
    def giant_drawhead( self ):
        pen=self.giant_pen
        pen.pd()
        for i in range(4): #head
            pen.fd(140)
            pen.lt(90)
        pen.fd(50)
        pen.lt(45)
        d2=sqrt(2*(140/6)**2)
        for i in range(3): #mouth
            pen.fd(d2)
            pen.lt(90)
            pen.fd(d2)
            pen.rt(90)
        pen.pu()
        pen.rt(45)
        pen.fd(50)
        pen.rt(90)
        pen.fd(25)
        pen.pd()
        pen.fd(90)         #eye
        pen.pu()
        pen.fd(25)
        pen.lt(90)
        pen.bk(100)
        pen.pu()
        pen.goto( self.giantorigin )
        pen.pd()


    def giant_drawfingers( self ):
        pen=self.giant_pen
        d2=sqrt(((75/6)**2)*2)
        pen.lt(45)
        for i in range(3):
            pen.fd(d2)
            pen.rt(90)
            pen.fd(d2)
            pen.lt(90)
        pen.lt(45)


    def giant_drawtorsostand( self ):
        pen=self.giant_pen
        pen.pd()
        #pen.begin_fill()
        pen.fd(200)
        pen.rt(90)
        pen.fd(25)
        pen.rt(90)
        pen.fd(195)
        pen.lt(90)
        self.giant_drawfingers()
        pen.fd(280)
        pen.lt(90)
        pen.fd(395)
        pen.lt(90)
        pen.fd(280)
        pen.lt(90)
        self.giant_drawfingers()
        pen.fd(195)
        pen.rt(90)
        pen.fd(25)
        pen.rt(90)
        pen.fd(200)
        pen.lt(90)
        pen.fd(195)
        pen.lt(90)
        #pen.end_fill()
        pen.pu()#goto draw head position
        pen.fd(285)
        pen.lt(90)
        pen.fd(30)
        pen.rt(90)


    def giant_drawtorsopunchleft( self ):
        pen=self.giant_pen
        pen.pd()
        #pen.begin_fill()
        pen.fd(200)#start
        pen.rt(90)
        pen.fd(25)
        pen.rt(90)
        pen.fd(195)
        pen.lt(90)
        self.giant_drawfingers()
        pen.fd(280)
        pen.lt(90)
        pen.fd(515)
        pen.lt(90)
        self.giant_drawfingers()
        pen.fd(220)
        pen.rt(90)
        pen.fd(210)
        pen.lt(90)
        pen.fd(195)
        pen.lt(90)
        #pen.end_fill()
        pen.pu() #goto draw head position
        pen.fd(285)
        pen.lt(90)
        pen.fd(25)
        pen.rt(90)


    def giant_drawtorsoblockleft( self ):
        pen=self.giant_pen
        pen.pd()
        #pen.begin_fill()
        pen.fd(200)
        pen.rt(90)
        pen.fd(25)
        pen.rt(90)
        pen.fd(195)
        pen.lt(90)
        self.giant_drawfingers()
        pen.fd(280)
        pen.lt(90)
        pen.fd(360)
        pen.rt(90)
        pen.fd(150)
        pen.lt(90)
        self.giant_drawfingers()
        pen.fd(225)
        pen.lt(90)
        pen.fd(140)
        pen.rt(90)
        pen.fd(210)
        pen.lt(90)
        pen.fd(195)
        pen.lt(90)
        #pen.end_fill()
        pen.pu() #goto head
        pen.fd(285)
        pen.lt(90)
        pen.fd(25)
        pen.rt(90)
        

    def giant_drawlegs( self ):
        pen=self.giant_pen
        pen.pu()
        pen.goto( self.giantorigin )
        pen.pd()
        pen.lt(45)
        pen.fd(25)
        pen.rt(45)
        pen.fd(220)
        pen.lt(90)
        pen.fd(195)
        pen.lt(90)
        pen.fd(220)
        pen.rt(45)
        pen.fd(25)
        pen.lt(135)
        pen.fd(85)
        pen.lt(90)
        pen.fd(170)
        pen.rt(90)
        pen.fd(60)
        pen.rt(90)
        pen.fd(170)
        pen.lt(90)
        pen.fd(85)
        pen.lt(90)
        pen.pu() #goto body
        pen.fd(238)
        pen.lt(90)
        pen.fd(18)
        pen.rt(90)
        

    def giant_drawcrouchinglegs( self, position='attack' ):
        pen=self.giant_pen
        pen.pu()
        pen.goto( self.giantorigin )
        pen.pd()   #draw leg
        pen.lt(45) 
        pen.fd(25)
        pen.rt(45)
        pen.fd(140)
        pen.lt(90)
        pen.fd(395)
        pen.lt(90)
        pen.fd(140)
        pen.rt(45)
        pen.fd(25)
        pen.lt(135)
        pen.fd(85)
        pen.lt(90)
        pen.fd(100)
        pen.rt(90)
        pen.fd(260)
        pen.rt(90)
        pen.fd(100)
        pen.lt(90)
        pen.fd(85)
        pen.lt(90)
        pen.pu() #goto body
        if position is 'defend':
            x=100
        else:
            x=153
        pen.fd(158)
        pen.lt(90)
        pen.fd(x)
        pen.rt(90)    


    def giant_drawtornadokicklegs( self ):
        #print('def giant_drawtornadokicklegs( self ):')
        pen=self.giant_pen
        pen.pu()
        pen.goto( self.giantorigin )
        pen.pd()
        pen.fd(25)
        pen.rt(45)
        pen.fd(160) #
        pen.lt(135)
        pen.fd(475) #+60
        pen.rt(45)
        pen.fd(25)
        pen.lt(135)
        pen.fd(85)
        pen.lt(90)
        pen.fd(330) #+60
        pen.rt(135)
        pen.fd(15) #
        pen.lt(90)
        pen.fd(85)
        pen.pu() #goto body
        pen.lt(135)
        pen.fd(140)
        pen.rt(90)
        #pen.fd(20)
        pen.fd(60)
        pen.lt(90)    
        

def main():
    window = tk.Tk()
    #window.withdraw() #hide window
    window.title('Secret Coders 6 : Monsters & Modules')
    #window.geometry('1169x990+0+0') #fit battleground image size only
    #window.geometry('1545x1020+0+0')
    window.geometry('1910x990+0+24')
    app = GameGUI(window)
    app.grid(row=0, column=0)
    window.rowconfigure(0, weight=1)
    window.columnconfigure(0, weight=1)

    window.mainloop()


def stylename_elements_options(stylename):
    '''Function to expose the options of every element associated to a widget
       stylename.'''
    try:
        # Get widget elements
        style = ttk.Style()
        layout = str(style.layout(stylename))
        print('Stylename = {}'.format(stylename))
        print('Layout    = {}'.format(layout))
        elements=[]
        for n, x in enumerate(layout):
            if x=='(':
                element=""
                for y in layout[n+2:]:
                    if y != ',':
                        element=element+str(y)
                    else:
                        elements.append(element[:-1])
                        break
        print('\nElement(s) = {}\n'.format(elements))

        # Get options of widget elements
        for element in elements:
            print('{0:30} options: {1}'.format(
                element, style.element_options(element)))

    except tk.TclError:
        print('_tkinter.TclError: "{0}" in function'
              'widget_elements_options({0}) is not a regonised stylename.'
              .format(stylename))



if __name__ == '__main__':
    main()
    stylename_elements_options('Horizontal.TProgressbar')
    

    

    


