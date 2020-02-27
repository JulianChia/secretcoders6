#!/usr/bin/python3
# -*- coding: utf-8 -*-

import tkinter as tk
import tkinter.ttk as ttk

INTROGUI_BG = 'light green'


class IntroGUI(ttk.Frame):

    def __init__( self,master=None,*args,**kw ):

        print('IntroGUI(ttk.Frame).__init__')
        # Class attributes
        self.master = master                                # masterWidget
        self.a = None                                       # mainWidgets
        self.b = None
        self.c = None
        self.d = None
        self.aPic = None                                    # subWidgets
        self.aLabel= None
        self.bLabel = None
        self.bRadiobutton1 = None
        self.bRadiobutton2 = None
        self.cLabel1 = None
        self.cLabel2 = None
        self.cRadiobutton1 = None
        self.cRadiobutton2 = None
        self.cRadiobutton3 = None
        self.cRadiobutton4 = None
        self.dButton = None
        self.nplayers = tk.IntVar( value='nplayers' )       #variables
        self.player1 = tk.StringVar( value='character' )
        self.player2 = tk.StringVar( value='character' )
        self.pic_secretcoders6=tk.PhotoImage( file='./image/secretcoders6_cover.gif' )

        # Run Class Methods
        self._set_style()
        self._set_master()
        self._create_self()
        self._create_mainWidgets()
        self._create_subWidgets()
        self._show_subWidgets()
        

    def _set_style(self):
        istyle = ttk.Style()
        istyle.configure( '.',font=('Liberation Serif',18,'normal') )
        istyle.configure( 'IntroGUI.TFrame',background=INTROGUI_BG )
        istyle.configure( 'IntroGUI.TFrame',background=INTROGUI_BG )
        #istyle.configure( 'IntroGUI.TFrame',background='pink' ) #Uncomment for debugging

        istyle.configure( 'a.TFrame',background=INTROGUI_BG )
        istyle.configure( 'b.TFrame',background='yellow' )
        istyle.configure( 'c.TFrame',background='cyan' )
        istyle.configure( 'd.TFrame',background='red' )
        
        istyle.configure( 'a.TLabel',background=INTROGUI_BG,font=('Liberation Serif',28,'bold') )
        istyle.configure( 'b.TLabel',background='yellow',font=('Liberation Serif',18,'bold') )
        istyle.configure( 'c.TLabel',background='cyan',font=('Liberation Serif',18,'bold') )

        istyle.configure( 'b.TRadiobutton',background='yellow' )
        istyle.configure( 'c.TRadiobutton',background='cyan' )

        istyle.configure( 'd.TButton',background='red',borderwidth=10)
        

    '''def _set_style(self):
        istyle = ttk.Style()
        istyle.configure( '.',font=('Times New Roman',18,'normal') )
        istyle.configure( 'IntroGUI.TFrame',background='#97B9AC' )
        #istyle.configure( 'IntroGUI.TFrame',background='pink' ) #Uncomment for debugging

        istyle.configure( 'a.TFrame',background='#97B9AC' )
        istyle.configure( 'b.TFrame',background='#97B9AC' )
        istyle.configure( 'c.TFrame',background='#97B9AC' )
        istyle.configure( 'd.TFrame',background='#97B9AC' )
        
        istyle.configure( 'a.TLabel',background='#97B9AC',font=('Times New Roman',28,'bold') )
        istyle.configure( 'b.TLabel',background='#97B9AC',font=('Times New Roman',18,'bold') )
        istyle.configure( 'c.TLabel',background='#97B9AC',font=('Times New Roman',18,'bold') )

        istyle.configure( 'b.TRadiobutton',background='#97B9AC' )
        istyle.configure( 'c.TRadiobutton',background='#97B9AC' )

        istyle.configure( 'd.TButton',background='#97B9AC',borderwidth=10)'''

        
    def _set_master(self):
        self.master.columnconfigure( 0,weight=1 )
        self.master.rowconfigure(    0,weight=1 )


    def _create_self(self):
        super().__init__( self.master,style='IntroGUI.TFrame',
                          width=800,height=500 )
        self.grid( row=0,column=0,sticky='nsew' )


    def _create_mainWidgets(self):
        self.a = ttk.Frame( self,style='a.TFrame',width=100,height=220 )
        self.b = ttk.Frame( self,style='b.TFrame',width=200,height=60 )
        self.c = ttk.Frame( self,style='c.TFrame',width=200,height=60 )
        self.d = ttk.Frame( self,style='d.TFrame',width=200,height=60 )

        self.a.grid( row=0,column=0,sticky='nsew' )
        self.b.grid( row=1,column=0,sticky='nsew',pady=[30,20] )
        self.c.grid( row=2,column=0,sticky='nsew',pady=[20,20] )
        self.d.grid( row=3,column=0,sticky='nsew',pady=[20,0] )


    def _create_subWidgets(self):
        #a widgets
        #myword='''Take part in this epic battle between the\n
      #Secret Coders and Dr. One-Zero.'''
        myword='    Secret Coders  Vs  Dr. One-Zero    '

        self.aPic   = ttk.Label( self.a, image=self.pic_secretcoders6 )
        self.aLabel = ttk.Label( self.a, text=myword,style='a.TLabel' )

        #b widgets
        self.bLabel = ttk.Label( self.b,text='How many players?',style='b.TLabel' )
        self.bRadiobutton1 = ttk.Radiobutton( self.b,text='1 Player', value=1,variable=self.nplayers,style='b.TRadiobutton',command=self._chooseNPlayers )
        self.bRadiobutton2 = ttk.Radiobutton( self.b,text='2 Players',value=2,variable=self.nplayers,style='b.TRadiobutton',command=self._chooseNPlayers )

        #c widgets
        self.cLabel1 = ttk.Label( self.c, text='Player 1 character?', style='c.TLabel' )
        self.cLabel2 = ttk.Label( self.c, text='Player 2 character?', style='c.TLabel' )
        self.cRadiobutton1 = ttk.Radiobutton( self.c,text='Secret Coders',value='Secret Coders',variable=self.player1,style='c.TRadiobutton',command=self._setPlayer2 )
        self.cRadiobutton2 = ttk.Radiobutton( self.c,text='Dr. One-Zero' ,value='Dr. One-Zero',variable=self.player1,style='c.TRadiobutton',command=self._setPlayer2 )
        self.cRadiobutton3 = ttk.Radiobutton( self.c,text='Secret Coders',value='Secret Coders',variable=self.player2,style='c.TRadiobutton',command=self._setPlayer1 )
        self.cRadiobutton4 = ttk.Radiobutton( self.c,text='Dr. One-Zero' ,value='Dr. One-Zero',variable=self.player2,style='c.TRadiobutton',command=self._setPlayer1 )

        #d widgets
        self.dButton = ttk.Button( self.d,text='START BATTLE',style='d.TButton',command=self._startbattle )


    def _show_subWidgets(self):
        #a widgets
        self.aPic.grid(   row=0,column=0)
        self.aLabel.grid( row=0,column=1, padx=20)

        #b widgets
        self.bLabel.grid( row=0,column=0,columnspan=2 )
        self.bRadiobutton1.grid( row=1,column=0 )
        self.bRadiobutton2.grid( row=1,column=1 )
        self.b.columnconfigure( 0,weight=1 )
        self.b.columnconfigure( 1,weight=1 )

        #d widgets
        self.dButton.grid( row=0,column=0,pady=5 )
        self.d.columnconfigure( 0,weight=1 )
        self.dButton.grid_remove()
        

    #Commands
    def _chooseNPlayers(self):
        if self.nplayers.get() == 1:
            self._show_1PlayerWidgets()
        elif self.nplayers.get() == 2:
            self._show_2PlayersWidgets()


    def _show_1PlayerWidgets(self):
        '''Show subWidgets in c mainWidget for 1Player mode'''
        # 1. Hide 'START BATTLE' Button
        self.dButton.grid_remove()
        # 2. Forget previous settings for c widgets
        self._clear_cWidgetsSettings()
        # 3. Give new grid settings for c widgets
        self.cLabel1.grid( row=0,column=0,columnspan=4 )
        self.cRadiobutton1.grid( row=1,column=0,columnspan=2 )
        self.cRadiobutton2.grid( row=1,column=2,columnspan=2 )
        self.c.columnconfigure( 0,weight=1 )
        self.c.columnconfigure( 2,weight=1 )


    def _show_2PlayersWidgets(self):
        '''Show subWidgets in c mainWidget for 2Players mode'''
        # 1. Hide 'START BATTLE' Button
        self.dButton.grid_remove()
        # 2. Forget previous settings for c widgets
        self._clear_cWidgetsSettings()
        # 3. Give new grid settings for c widgets
        self.cLabel1.grid( row=0,column=0,columnspan=2 )
        self.cLabel2.grid( row=0,column=2,columnspan=2 )
        self.cRadiobutton1.grid( row=1,column=0 )
        self.cRadiobutton2.grid( row=1,column=1 )
        self.cRadiobutton3.grid( row=1,column=2 )
        self.cRadiobutton4.grid( row=1,column=3 )
        self.c.columnconfigure( 0,weight=1 )
        self.c.columnconfigure( 1,weight=1 )
        self.c.columnconfigure( 2,weight=1 )
        self.c.columnconfigure( 3,weight=1 )


    def _clear_cWidgetsSettings(self):
        #Forget Grid Settings
        self.cLabel1.grid_forget()
        self.cLabel2.grid_forget()
        self.cRadiobutton1.grid_forget()
        self.cRadiobutton2.grid_forget()
        self.cRadiobutton3.grid_forget()
        self.cRadiobutton4.grid_forget()
        #Reset Control Variables with zero values
        self.player1.set(0)
        self.player2.set(0)


    def _setPlayer2(self):
        '''Set control variable for all radiobuttons widgets for 2Players mode.'''
        if self.nplayers.get() == 1:
            self.player2.set(None)
        elif self.nplayers.get() == 2:
            if self.player1.get() == 'Secret Coders':
                self.player2.set('Dr. One-Zero')
            elif self.player1.get() == 'Dr. One-Zero':
                self.player2.set('Secret Coders')
        self.dButton.grid()

            
    def _setPlayer1(self):
        '''Set control variable of all radiobuttons widgets for 1Player mode.'''
        if self.player2.get() == 'Secret Coders':
            self.player1.set('Dr. One-Zero')
        elif self.player2.get() == 'Dr. One-Zero':
            self.player1.set('Secret Coders')
        self.dButton.grid()


    def _startbattle(self):
        print('\ndef _startbattle(self):')
        print( 'self.nplayers =',self.nplayers.get() )
        print( 'self.player1  =',self.player1.get() )
        print( 'self.player2  =',self.player2.get() )
        #return self.nplayers.get(),self.player1.get(),self.player2.get()
        self.dButton.state(['disabled'])   # Disable the button.
        self.master.update_GameGUI(
            self.nplayers.get(),self.player1.get(),self.player2.get() )
        self.dButton.state(['!disabled'])   # Disable the button.


def main():
    root = tk.Tk()
    intropage = IntroGUI(root)
    root.update_idletasks()
    print('root geometry = ', root.geometry())
    root.mainloop()
    
    

if __name__ == "__main__":
    main()
