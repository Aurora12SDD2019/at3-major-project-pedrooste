""" Racing to the end of the universe!
A simple car game involving pygame. You control a car on a road in which you have to dodge oncomming cars, this will get harder as the game progresses.
"""

__author__ = "Pedro Oste"
__license__ = "GPL"
__version__ = "1.0.2"
__email__ = "Pedro.oste@education.nsw.com.au"
__status__ = "Alpha"

#dependencies
import pygame as P # accesses pygame files
import sys  # to communicate with windows
import random as R #import the random function
from mods import * #imports modules from mods file
from Highscores import * #imports the class from highscores file

# pygame setup - only runs once
P.init()  # starts the game engine
clock = P.time.Clock()  # creates clock to limit frames per second
loopRate = 60  # sets max speed of main loop
SCREENSIZE = SCREENWIDTH, SCREENHEIGHT = 800, 600  # sets size of screen/window
screen = P.display.set_mode(SCREENSIZE)  # creates window and game screen
P.display.set_caption("Racing to the end of the universe!") #sets the game window caption
play = True #controls the game loop

# set variables for some colours if you want them RGB (0-255)
white = (255, 255, 255)
black = (0, 0, 0)
red = (216, 0, 0)
lightRed = (255, 0, 0)
yellow = (234, 226, 0)
lightYellow = (255,255,0)
green = (0, 206, 44)
lightGreen = (0, 249, 54)
blue = (5, 0, 165)
lightBlue = (8, 0, 255)
grey = (92, 98, 112)

#creates objects to be used later on in button class
playB = button(green,lightGreen,150,50,"PLAY",34,black,"play")
highscoreB = button(red,lightRed,200,50,"HIGHSCORES",34,black,"highscore")
instructionsB = button(blue,lightBlue,200,50,"INSTRUCTIONS",34,black,"instructions")
introB = button(red,lightRed,150,50,"BACK",34,black,"intro")
mainMenuB = button(red,lightRed,200,50,"MAIN MENU",34,black,'mainMenu')
saveB = button(blue,lightBlue,200,50,"SAVE",34,black,'save')
todayB = button(blue,lightBlue,150,50,"TODAYS",34,black,'today')
overallB = button(blue,lightBlue,150,50,"OVERALL",34,black,'overall')

#creates objects to be used later on in arrowButton class
leftB = arrowButton(yellow,lightYellow,100,50,"left")
rightB = arrowButton(yellow,lightYellow,100,50,"right")

#creates objects to be used later in player class
mcar = player(red,green,50,50) #main player car

#creates the enemy cars to be used later on
Ecar0 = Ecar(white,5,-50,50,50)
Ecar1 = Ecar(black,5,-225,50,100)
Ecar2 = Ecar(lightBlue,5,-300,50,50)
Ecar3 = Ecar(blue,5,-370,50,50)
Ecar4 = Ecar(yellow,5,-440,50,50)
Ecar5 = Ecar(lightRed,5,-510,50,50)
Ecar6 = Ecar(red,5,-580,50,50)

#creates two objects of Highscores which will be refered to acess methods ass well as printing scores
HST = highscore('Todays Highscores')
HS = highscore('Highscores')


#creating a dictionary that referes to each of the enemy car objects, this is to make it easier to call them later
enemyCarDict = {
    0 : Ecar0,
    1 : Ecar1,
    2 : Ecar2,
    3 : Ecar3,
    4 : Ecar4,
    5 : Ecar5,
    6 : Ecar6,
    }
#creates a dictionary that refers to which playScreen to display (this is referenced later within the class
dispatch = {
        'intro' : 'introscreen',
        'play' : 'playGame',
        'instructions' : 'instructionScreen',
        'crash' : 'crashScreen',
        'highscore' : 'highscoreScreen',
            }

class game():
    """Game loop! contians all of the different screens in different methods....

    Attributes:
            #creates initial variables that will be used
        self.carX = 375 :x cordinate for car
        self.playScreen = "intro" :intialises what screen to start on
        self.score = 0 :initialises score because theres no headstarts here
        self.name = '' :name of the persons highscore
        """
        
    def __init__(self):
        '''creates initial variables that will be used'''
        self.carX = 375 
        self.playScreen = "intro" 
        self.score = 0 
        self.name = ''
        self.saved = False
        self.today = False
        

        
    def introscreen(self):
        """Displays the intro screen
        Made up of a background, buttons and text

        """
        screen.fill(white) #fills the screen with a background colour
        rTxt(screen,"Racing to the end of the universe",400,50,48,black)
        #draws the play, quit and instruction button
        self.playScreen = playB.draw(screen,50,500, self.playScreen) 
        self.playScreen =highscoreB.draw(screen,550,500, self.playScreen)
        self.playScreen =instructionsB.draw(screen,275,500, self.playScreen)
        
    def playGame(self):
        """Displays the game screen
        this will then reference to other classes

        """
        screen.fill(grey) #fills the screen with a background colour , has to be placed first
        #while these lines are inconvient now, a class will be made to draw and update the background once graphics are introduced
        P.draw.line(screen,white,[100,0],[100,600],5)
        P.draw.line(screen,white,[700,0],[700,600],5)
        
        oldCarX = self.carX #creates a temporary variable which will be checked later on to see if the x postion has been changed
        #draws left and right buttons
        self.carX = leftB.draw(screen,50,500,self.carX)
        self.carX = rightB.draw(screen,650,500,self.carX)
        
        if oldCarX == self.carX: #if the x postion has been changed then movement will be true. If movement is true then the rectangle will be draw a different colour
            movement = False
        else:
            movement = True
        
        difficulty = checkScore(self.score) #checks the difficulty in order to determine how many cars to deply
        
        for i in range (0,difficulty): #deploys cars according to how hard the difficutly is
            self.score = enemyCarDict[i].draw(screen,self.score)
            
        
        mcar.draw(screen,self.carX,movement) #draws the main player rectangle car
        



        rTxt(screen,("Score: "+str(self.score)),100,50,48,black)    
        self.playScreen = introB.draw(screen,600,50,self.playScreen) #draws the back button which only will be used to go back to the intro screen
        
        for i in range (0,difficulty): #checks all the cars that are depolyed
                crash = enemyCarDict[i].checkHit(self.carX) #checks if the car hits the enemy car
                if crash == True:
                    self.playScreen = "crash" #sends to crash screen
            
        
        if self.carX>600+50 or self.carX<100: #creates a boundry that the car must stay in, however these numbers will be changed when graphics are implemented (based off drawn lines)
            self.playScreen = "crash"

    def instructionScreen(self):
        """Displays the instructions screen
        this will then reference to other classes

        """
        screen.fill(black) #fills the screen with a background colour
        rTxt(screen,"Instructions",400,50,48,white)
        self.playScreen = introB.draw(screen,600,50, self.playScreen) #draws the back button for the intro screen
    
    def highscoreScreen(self):
        """Displays the highscore screen
        this will then reference to other classes
        """
        screen.fill(white) #fills the screen with a background colour
        self.playScreen = introB.draw(screen,600,50, self.playScreen) #draws the back button for the intro screen

            
        if self.today == True:
            press = todayB.draw(screen,600,500, self.playScreen)
            rTxt(screen,"Overall Highscores",400,50,48,black)
            HS.printHighscore(screen,black)
            
        if self.today == False:
            press = overallB.draw(screen,600,500, self.playScreen)
            rTxt(screen,"Todays Highscores",400,50,48,black)
            HST.printHighscore(screen,black)

        if press == True:
            self.today = False
        if press == False:
            self.today = True
        
    def crashScreen(self):
        """Displays the crash screen when a boundry is met
        this will reference to other classes and modules to display a screen
        """
        save = False #states whether the name is saved or not  
        
        P.draw.rect(screen,white,(100,50,600,500)) #draws background screen
        
        
        rTxt(screen,"You crashed!",400,100,48,black) #displays text saying you crashed
        rTxt(screen,("Score: "+str(self.score)),400,200,48,black) #displays your score
        
        if self.saved == False:
            rTxt(screen,"Name: ",200,275,48,black) #displays text
            P.draw.rect(screen,black,(300,250,300,50),5) #border for name input
            save = saveB.draw(screen,450,450,self.playScreen) #draws the save button
            
            
            for event in P.event.get(): #gets any events from the user
                if event.type == P.KEYDOWN: #checks if the event is a key press
                    if event.key == P.K_BACKSPACE: #If the event is a backspace it will take away a character from the string
                        self.name = self.name[0:-1]
                    elif event.key == P.K_TAB:
                        pass #cant put a tab within the name as this is what seperates variables
                    else:
                        if len(self.name) < 10: #limit of characters is 10
                            self.name += event.unicode #adds the letter or symbol to the name
                        

            rTxt(screen,self.name,400,275,48,black) #draws the name
        
        self.playScreen = mainMenuB.draw(screen,150,450,self.playScreen) #draws a main menu button
        if self.playScreen == "intro": #if the palyer wants to go to the main menu, positions must be reset
            self.carX = 375 #car reset positon
            self.score = 0 # resets the score
            self.name = '' #resets the name
            self.saved = False #resets the saved variable
            for i in range (0,6): #becasue difficulty is not passed we will reset all of the cars, this is okay because it is done rarely 
                enemyCarDict[i].resetCars() #calls class method to reset the value of the coordinates for each object
                
        
        
        if save == True:
            self.name = HS.appendFile(self.name,self.score)
            if self.name == '':
                self.saved = False
            else:
                self.saved = True
                print("score was saved")
            
            
    def gameloop(self):
        ''' determines what screen to display based on playscreen'''

        getattr(self, dispatch[self.playScreen])() #gets the key from the dictionary


#this varaible has to be created after the game class has been interprited
game = game()


# game loop - runs loopRate times a second!
while play:  # game loop - note:  everything in this loop is indented one tab
    
    game.gameloop()
    
    for event in P.event.get():  # get user interaction events
        if event.type == P.QUIT:  # tests if window's X (close) has been clicked
            play = False  # causes exit of game loop


        
    # your code ends here #
    P.display.flip()  # makes any changes visible on the screen
    clock.tick(loopRate)  # limits game to frame per second, FPS value

# out of game loop #
print("Thanks for playing")  # notifies user the game has ended
P.quit()   # stops the game engine
sys.exit()  # close operating system window



