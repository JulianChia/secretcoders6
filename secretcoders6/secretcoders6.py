#!/usr/bin/python3
# -*- coding: utf-8 -*-

""" Main Program to play SecretCoders vs Dr.One-Zero

IntroGUI - Intro GUI of game
GameGUI  - Game GUI of game 

Authors : Julian Chia, Samuel Chia, Elizabeth Chia
Created : 8th Dec 2018
Modified: 24th Jan 2018

"""

import tkinter as tk
import tkinter.ttk as ttk
import tkinter.messagebox as tkMessageBox

import IntroPage_v4 as intro
import secretcodergame_v4 as game
from music import MusicPlayer


class App(ttk.Frame):

    def __init__( self,master=None,musicplayer=None,*args,**kw ):
        print('\nApp(ttk.Frame).__init__')
        # Class attributes
        self.master = master
        self.musicplayer = musicplayer
        self.guis = None  #Dictionary of GUIs

        # Run Class methods
        self._create_self()
        self._create_GUIs()
        self._show_GUI("IntroGUI")

        #show class App's master window
        self.master.deiconify()
        

    def _create_self(self):
        # Create 'self', which is a ttk.Frame widget
        super().__init__( self.master )
        self.grid( row=0,column=0,sticky='nsew' )
        
        self.rowconfigure(   0, weight=1)
        self.columnconfigure(0, weight=1)


    def _create_GUIs(self):
        '''Creates a dictionary of instances to GUI classes

        intro.IntroGUI() - Introduces game.
        game.GameGUI()   - Plays game
        '''
        print('\ndef _create_GUIs(self):')
        self.guis = {}
        for G in ( intro.IntroGUI, game.GameGUI ):
            gui_name = G.__name__
            gui = G(self)
            #print('\n',gui_name, gui.__dict__)
            self.guis[gui_name] = gui
            gui.grid( row=0, column=0, sticky="nsew" )
            

    def _show_GUI(self, gui_name):
        '''Show the desired gui. '''
        print('\ndef _show_GUI(self, gui_name)')

        #1. Bring to foreground the desired gui.
        gui = self.guis[gui_name]
        gui.tkraise()

        #2. Define geometry for current gui.
        if gui_name == 'IntroGUI':
            print('IntroGUI')
            window_geometry = GEOMETRY_INTROGUI
            self.musicplayer.fadeout( 2000 )
            self.musicplayer.play_intro( loops=-1 )
        elif gui_name == 'GameGUI':
            print('GameGUI')
            window_geometry = GEOMETRY_GAMEGUI
            self.musicplayer.fadeout( 2000 )
            self.musicplayer.play_game( loops=-1 )
        else:
            raise 'Error in method "_show_GUI": Invalid "gui_name" value used.'
        
        #3. Always want window to resize to fit new gui.
        top = gui.winfo_toplevel()
        top.geometry(window_geometry)


    def update_GameGUI(self, nplayers, player1, player2):
        ''
        print()
        print('def update_GameGUI(self, nplayers, player1, player2):')
        print( 'nplayers =',nplayers )
        print( 'player1  =',player1 )
        print( 'player2  =',player2 )
        #Update GameGUI attributes
        gui = self.guis['GameGUI']
        gui.nplayers.set(nplayers)
        gui.player1.set(player1)
        gui.player2.set(player2)
        #Choose 1 or 2 players mode
        if nplayers == 1:
            gui.runOnePlayer( player1 )
        elif nplayers == 2:
            gui.runTwoPlayers( player1,player2 )
        else:
            raise 'Error in method "update_GameGUI": Invalid "nplayers" value used.'
        #Show GameGUI
        self._show_GUI('GameGUI')


    def ask_quit( self ):
        '''Confirmation to quit application.'''
        if tkMessageBox.askokcancel( "Quit","Exit Secret Coders vs Dr. One-Zero" ):
            self.musicplayer.quit() #Quit MusicPlayer 
            self.master.destroy()   #Destroy the Tk Window instance.
            # Note: After initialzing pygame.mixer, it will preoccupy an entire CPU core.
            #       Before destroying the Tk Window, ensure pygame.mixer is quitted too else
            #       pygame.mixer will still be running in the background despite destroying the 
            #       Tk Window instance.


GEOMETRY_INTROGUI = '777x500+0+24'
GEOMETRY_GAMEGUI = '1910x990+0+24'


def main():

    #Create and setup Tk window
    root = tk.Tk()
    root.withdraw()
    root.geometry( GEOMETRY_INTROGUI )
    root.title('Secret Coders vs Dr. One-Zero')
    root.resizable(width=False,height=False) #Fix Tk() window size
    root.columnconfigure( 0,weight=1 )
    root.rowconfigure(    0,weight=1 )

    #Create and setup game application GUIs
    musicplayer = MusicPlayer()
    app = App( root, musicplayer )
    #print('\n',root.__dict__)
    #print('\n',app.__dict__)

    #Activate Tk window mainloop to track GUI events
    root.protocol("WM_DELETE_WINDOW", app.ask_quit) #Tell Tk window instance what to do before it is destroyed.
    root.mainloop()
    
    

if __name__ == "__main__":
    main()
