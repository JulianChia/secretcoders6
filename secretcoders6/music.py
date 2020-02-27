#!/usr/bin/python3
# -*- coding: utf-8 -*-

from pygame import mixer
import time

class MusicPlayer(object):

    def __init__(self, *args, **kwargs):

        # MusicPlayer's Atrributes
        self.intromusic = './sound/IntroGUI.ogg'  # IntroGUI Audio file
        self.gamemusic = './sound/GameGUI.ogg'    # GameGUI Audio file
        self.player = None                        # Music player

        # Call this method
        self._set_musicplayer()

    
    def _set_musicplayer( self ):
        '''Initialise pygame mixer.'''
        print( '\ndef load_audiofile( self, audiofile ):' )
        player = mixer
        player.init()
        player.music.set_volume( .20 )
        self.player = player; print('self.player ', self.player)


    def play_intro( self, loops=0, start=0.0 ):
        '''Play Intro track from start location.'''
        print('\ndef play_intro():')
        self.player.music.load( self.intromusic )
        self.player.music.play( loops, start ); print( 'Play Intro Music Started' )


    def play_game( self, loops=0, start=0.0 ):
        '''Play Game track from start location.'''
        print('\ndef play_game():')
        self.player.music.load( self.gamemusic )
        self.player.music.play( loops, start ); print( 'Play Game Music Started' )


    def stop( self ):
        '''stop the playing of a track.'''
        print('\ndef stop():')
        if self.player.music.get_busy():
            self.player.music.stop(); print('Play stopped.')


    def fadeout( self, millisecond=2000 ):
        '''fadeout and stop the playing of a track.'''
        print('\ndef fadeout():')
        if self.player.music.get_busy():
            self.player.music.fadeout( millisecond ); print('Play faded out')


    def quit( self ):
        '''Quit MusicPlayer.'''
        print('\ndef quit():')
        self.stop()         #stop playing track 
        self.player.quit(); print('Quitted pygame.mixer.') 

        # Note: After initialzing pygame.mixer, it will preoccupy an entire CPU core.
        #       To quit Music Player, ensure pygame.mixer is quitted too else pygame.mixer 
        #       will still be running in the background.


if __name__ == "__main__":
    app = MusicPlayer()  #Initialize an instance of MusicPlayer object
    app.play_intro()
    i = 0
    while True:
        i += 1; print( i )
        time.sleep(1)
        if not app.player.music.get_busy():
            print( 'Play Ended' )
            break
        if i == 10:
            app.fadeout()
            break

    app.play_game()
    i = 0
    while True:
        i += 1; print( i )
        time.sleep(1)
        if not app.player.music.get_busy():
            print( 'Play Ended' )
            break
        if i == 10:
            app.stop()
            break
    app.quit()
            
