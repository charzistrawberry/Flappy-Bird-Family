import string 
import math 
import decimal
import random
import itertools
import time
import os 
from cmu_112_graphics import *
import random
from PIL import Image, ImageTk

import sys
print(f'"{sys.executable}" -m pip install pillow')
print(f'"{sys.executable}" -m pip install requests')
################################################################################
#got my images (except for background and ghost) from https://github.com/sourabhv/FlapPyBird/blob/master/assets/sprites/0.png
#got my background image from https://github.com/akhil-code/flappy-bird-neuro-evolution/issues/1
#got ghost image from https://www.cleanpng.com/png-pac-man-world-3-ghosts-clip-art-pac-man-ghost-png-105782/download-png.html 
#animation graphics from cmu_112_graphics
#@https://diderot-production.s3.amazonaws.com/media/courses_public/CMU%3APittsburgh%2C%20PA%3A15112%3ASummer-2%3A2019-20/Notes/ch%3A%3A%3Aadditional-animation-framework-features/chapter_attachments/5439b23e-d6a0-11ea-9a6c-0ab634db4e5d_cmu_112_graphics.py

class HelpMode(Mode):
    def appStarted(self):
        self.backgroundDay = self.loadImage('background-day.png')
        self.backgroundW, self.backgroundH = self.backgroundDay.size
        self.backgroundDay = self.scaleImage(self.backgroundDay,850/self.backgroundH)
        self.x = self.width/2
        self.y = self.height/2
        self.w = 600
        self.h = 400
    def tog(self):
        self.setActiveMode("start")
    def redrawAll(self,canvas):
        canvas.create_image(self.width/2,self.height/2,
                            image = ImageTk.PhotoImage(self.backgroundDay))

        canvas.create_rectangle(self.x-self.w/2,self.y-self.h/2,
                                self.x+self.w/2,self.y+self.h/2,
                                fill = "sandybrown")
        
        line1 = "Click the spacebar repeatedly to flap the bird's wings."
        line2 = "When you do this, the bird will fly up but will fall if you're not flapping it."
        line3 = "Try to avoid hitting the pipes and the ghosts as you flap."
        line4 = "Each time you pass a pipe, your score increases by 1."
        line5 = "Each time you grab an egg from the ghost, your score increases by 5."
        line6 = "REMEMBER TO NOT RAGE QUIT!"
        canvas.create_text(self.x, self.y-40, text = line1, font = "Times 15")
        canvas.create_text(self.x, self.y-20, text = line2, font = "Times 15")
        canvas.create_text(self.x, self.y, text = line3, font = "Times 15")
        canvas.create_text(self.x, self.y+ 20, text = line4, font = "Times 15")
        canvas.create_text(self.x, self.y+ 40, text = line5, font = "Times 15")
        canvas.create_text(self.x, self.y+ 60, text = line6, font = "Times 15")


        #back button
        canvas.create_rectangle(0,0, 150,100, fill = "PaleVioletRed1",onClick = self.tog)
        canvas.create_text(75,50,text = "Go Back", font = "Times 20")
class StartMode(Mode):
    def appStarted(self):
        self.backgroundDay = self.loadImage('background-day.png')
        self.backgroundW, self.backgroundH = self.backgroundDay.size
        self.backgroundDay = self.scaleImage(self.backgroundDay,850/self.backgroundH)


        self.logo = self.loadImage('flappyBirdLogo.png')
        self.logoW,self.logoH = self.logo.size
        self.logo = self.scaleImage(self.logo, 500/self.logoW)
        self.logoW,self.logoH = self.logo.size
        self.logoX = self.width/5 *2
        self.logoY = self.height/6

        self.pipe = self.loadImage('pipe.png')
        self.pipeW,self.pipeH = self.pipe.size
        self.pipe = self.scaleImage(self.pipe, 490/self.pipeH)
        self.pipe = self.pipe.resize((80,800))
        self.pipeW,self.pipeH = self.pipe.size
      
        

        self.yellowBird = self.loadImage('yellowbird-midflap.png')
        self.redBird = self.loadImage('redbird-midflap.png')
        self.blueBird = self.loadImage('bluebird-midflap.png')
        self.birdW,self.birdH = self.yellowBird.size
        self.yellowBird = self.scaleImage(self.yellowBird,50/self.birdW)
        self.redBird = self.scaleImage(self.redBird,50/self.birdW)
        self.blueBird = self.scaleImage(self.blueBird,50/self.birdW)
        self.birdW,self.birdH = self.yellowBird.size

        self.colorChoices = [self.yellowBird,self.redBird,self.blueBird]
        self.colorIndex = 0
        self.color = self.yellowBird

        self.birdX = self.width/6
        self.birdY = self.height/2

    def changeColorRight(self):
        self.colorIndex += 1
        self.color = self.colorChoices[self.colorIndex%len(self.colorChoices)]
    
    def changeColorLeft(self):
        self.colorIndex -=1
        self.color = self.colorChoices[self.colorIndex%len(self.colorChoices)]

    def keyPressed(self,event):
        if event.key == "Space":
            if self.color == self.yellowBird:
                self.setActiveMode(PlayMode("yellow"))
            elif self.color == self.blueBird:
                self.setActiveMode(PlayMode("blue"))
            else:
                self.setActiveMode(PlayMode("red"))
    def tog(self):
        self.setActiveMode("help")
    def redrawAll(self,canvas):

        #creates backgrouned
        canvas.create_image(self.width/2,self.height/2,
                            image = ImageTk.PhotoImage(self.backgroundDay))

        #creates bird
        canvas.create_image(self.birdX,self.birdY,
                            image = ImageTk.PhotoImage(self.color))
        
        #right button
        rightX = self.birdX + 70
        rightY = self.birdY
        rightW = 70
        rightH = 30
        canvas.create_rectangle(rightX - rightW/2, rightY - rightH/2,
                                rightX + rightW/2, rightY + rightH/2,
                                fill = "light goldenrod", onClick = self.changeColorRight)
        canvas.create_text(rightX,rightY,text = ">", font = "Times 20")

        #left button 
        leftX = self.birdX - 70
        leftY = self.birdY
        leftW = 70
        leftH = 30
        canvas.create_rectangle(leftX - leftW/2, leftY - leftH/2,
                                leftX + leftW/2, leftY + leftH/2,
                                fill = "light goldenrod", onClick = self.changeColorLeft)
        canvas.create_text(leftX,leftY,text = "<", font = "Times 20")

        #logo 
        canvas.create_image(self.logoX, self.logoY, 
                            image = ImageTk.PhotoImage(self.logo))

        #creates pipes1
        x0,y0 = self.width/10*6,350 
        canvas.create_image(x0,y0, anchor="n",image = ImageTk.PhotoImage(self.pipe))
        x1,y1 = x0, 210
        canvas.create_image(x1,y1, anchor = "s",image = ImageTk.PhotoImage(self.pipe.rotate(180)))
        
        
        #cretaes pipes2
        x2,y2 = self.width/12*9, self.height - 200
        canvas.create_image(x2,y2, anchor = "n", image = ImageTk.PhotoImage(self.pipe))
        x3,y3 = x2, 450
        canvas.create_image(x3,y3, anchor = "s",image = ImageTk.PhotoImage(self.pipe.rotate(180)))

        #creates pipes3
        x4,y4 = self.width/14*13, 450
        canvas.create_image(x4,y4, anchor = "n", image = ImageTk.PhotoImage(self.pipe))
        x5,y5 = x4, 300
        canvas.create_image(x5,y5,anchor = "s", image = ImageTk.PhotoImage(self.pipe.rotate(180)))

        #text
        xT= self.width/5*2
        yT = self.height/5*2
        wT = 300
        hT = 100
        canvas.create_rectangle(xT-wT/2, yT-hT/2, xT+wT/2, yT+hT/2, fill = "gray89")
        canvas.create_text(xT,yT,text="Press the Spacebar to Start", font = "Times 20")

        tX = self.width/5*2
        tY = self.height/5*3
        tW = 300
        tH = 100
        canvas.create_rectangle(tX-tW/2, tY-tH/2, tX+tW/2, tY+tH/2, fill = 'gray89',onClick = self.tog)
        canvas.create_text(tX,tY, text="Help", font = "Times 20")


class GameOverMode(Mode):
    def __init__(self,pipes,ghosts,eggs,score, *initialState, name = "gameOver", **kwargs):
        self.pipes = pipes 
        self.ghosts = ghosts
        self.score = score
        
        super().__init__(name = name)

    def appStarted(self):
        self.backgroundDay = self.loadImage('background-day.png')
        self.backgroundW, self.backgroundH = self.backgroundDay.size
        self.backgroundDay = self.scaleImage(self.backgroundDay,850/self.backgroundH)

        self.blueBird = self.loadImage('bluebird-midflap.png')
        self.redBird = self.loadImage('redbird-midflap.png')
        self.yellowBird = self.loadImage('yellowbird-midflap.png')
        self.birdW,self.birdH = self.yellowBird.size
        self.blueBird = self.scaleImage(self.blueBird,50/self.birdW)
        self.redBird = self.scaleImage(self.redBird, 50/self.birdW)
        self.yellowBird = self.scaleImage(self.yellowBird, 50/self.birdW)

        
        self.cX = self.width/2
        self.cY = self.height/3
        self.cW = 300
        self.cH = 100
        self.dX = self.width/2
        self.dY = self.height/3*2
        self.dW,self.dH = self.cW,self.cH

        self.color = "orange"

    def toggle(self):
        self.setActiveMode("start")
    
    def redrawAll(self,canvas):
        #creates backgrouned
        canvas.create_image(self.width/2,self.height/2,
                            image = ImageTk.PhotoImage(self.backgroundDay))
        
        for pipe in self.pipes:
            pipe.draw(canvas)
        
        for ghost in self.ghosts:
            ghost.draw(canvas)

        canvas.create_rectangle(self.cX-self.cW/2,self.cY-self.cH/2,
                                self.cX+self.cW/2,self.cY+self.cH/2, fill = "lavender blush")
        
        canvas.create_text(self.cX, self.cY - 20, text = "Score:", font = "Times 16")
        canvas.create_text(self.cX, self.cY+10, text = str(self.score), font = "Times 16")

        canvas.create_image(self.width/2 - 80,self.height/2,
                            image = ImageTk.PhotoImage(self.blueBird))
        canvas.create_image(self.width/2,self.height/2,
                            image = ImageTk.PhotoImage(self.yellowBird))
        canvas.create_image(self.width/2 + 80,self.height/2,
                            image = ImageTk.PhotoImage(self.redBird))
        

        canvas.create_rectangle(self.dX - self.dW/2, self.dY-self.dH/2,
                                self.dX + self.dW/2, self.dY+self.dH/2,
                                fill = "lavender blush", onClick = self.toggle)
        canvas.create_text(self.dX,self.dY,text = "Click to Restart", font = "Times 16")
class Bird():
    """
    This is where the bird attributes are. The bird's position will start 
    on the left side middle. The bird's size will be measured to make sure 
    the pipes are big enough to fit the bird
    """
    def __init__(self,app,sprites):
        """
        self.yellowBird = self.loadImage('yellowbird-midflap.png')
        self.redBird = self.loadImage('redbird-midflap.png')
        self.blueBird = self.loadImage('bluebird-midflap.png')
        self.birdW,self.birdH = self.yellowBird.size
        self.yellowBird = self.scaleImage(self.yellowBird,50/self.birdW)
        self.redBird = self.scaleImage(self.redBird,50/self.birdW)
        self.blueBird = self.scaleImage(self.blueBird,50/self.birdW)
        self.birdW,self.birdH = self.yellowBird.size
        """
        self.app = app
        self.sprites = sprites
        self.spriteIndex = 0
        self.birdX = self.app.width/7
        self.birdY = self.app.height/2
        self.birdH = 10
        self.birdW = 10
        #bird height will be used to determine the gap of the pipes
    def changeImage(self):
        self.spriteIndex = (self.spriteIndex +1) % len(self.sprites)

    def move(self,velocity):
        """ moves the bird by changing its y coordinate"""
        #if it has not hit a border or collided with a pipe it will continue to move
        self.birdY += velocity

    def draw(self,canvas):
        """draws the bird"""
        currSprite = self.sprites[self.spriteIndex]
        canvas.create_image(self.birdX,self.birdY, image = ImageTk.PhotoImage(currSprite))

class Pipe():
    def __init__(self,app,pHeight,gap,image):
        """
        Since the bird can only move up and down, the only thing that matters 
        to measure the pipe is the height of them. All pipes have the same
        width so it will not need to be implemented. Pipe also takes in a gap 
        to help determine where the bottom pipe will be placed 
        """

        self.app = app
        self.color = "green"
        self.gap = gap
        self.image = image
        #the first pipe will be on the right side but the height will be randomized
        self.pipeX = self.app.width/20 * 19
        self.pipeY = pHeight
        self.pipeW = 70

    def hitsPipe(self,bird):
        """
        checks if the bird has hit a pipe. if the x coordinate of the bird 
        is greater than the x coordinate of the pipe, we should also check if 
        it is within the perimeters of the pipe. If the conditions are true,
        the game is over and the bird completely drops
        """
        
        #checks if it is within the width bounds of the pipe
        if (bird.birdX + bird.birdW/2 > self.pipeX - self.pipeW/2 and
            bird.birdX - bird.birdW/2 < self.pipeX + self.pipeW/2):
            if (bird.birdY - bird.birdH/2 < self.pipeY or
                bird.birdY + bird.birdH/2 > self.pipeY + self.gap):
                return True
        return False     
        #returns true if it has hit a border
    
    def passesPipe(self,bird):
        if bird.birdX - bird.birdW/2 > self.pipeX + self.pipeW/2:
            return True
        return False
    
    """
    def move(self,xP):
        self.pipeX = xP
    """

    def draw(self,canvas):
        """Draws the pipes"""
        #top pipe 
        x0 = self.pipeX
        y0 = self.pipeY
         
        canvas.create_image(x0,y0,anchor = "s",image = ImageTk.PhotoImage(self.image.rotate(180)))

        #bottom pipe
        x1 = self.pipeX
        y1 = self.pipeY + self.gap
        canvas.create_image(x1,y1,anchor = "n",image = ImageTk.PhotoImage(self.image))

class Ghost():
    def __init__(self,app,ghostImage):
        self.app = app
        self.topBound = self.app.height/7
        self.bottomBound = self.app.height/7*6
        self.ghostImage = ghostImage
        self.ghostW,self.ghostH = self.ghostImage.size
        self.ghostX = self.app.width/20 * 19
        self.ghostStart = [self.topBound + self.ghostH/2 +1 , self.bottomBound-self.ghostH/2-1]
        self.ghostY = random.choice(self.ghostStart)
        #self.ghostY = self.topBound + self.ghostH/2 +1 
        self.velocity = 10
        
        
    
    def move(self):
        if (self.ghostY + self.ghostH/2 < self.bottomBound and 
            self.ghostY - self.ghostH/2 > self.topBound):
            self.ghostY += self.velocity    
        else: 
            self.velocity *= -1
            self.ghostY += self.velocity
          
        
    def hitsGhost(self,bird):
        
        distance = ((self.ghostX - bird.birdX)**2 + (self.ghostY - bird.birdY)**2)**0.5
        return bird.birdW/2 + self.ghostW/2 > distance

    def draw(self,canvas):
        canvas.create_image(self.ghostX,self.ghostY,
                            image = ImageTk.PhotoImage(self.ghostImage))

class Egg():
    def __init__(self,app):
        self.app = app
        self.topBound = self.app.height/7
        self.bottomBound = self.app.height/7*6
        self.eggX = self.app.width/20 * 19
        self.eggY = (self.topBound + self.bottomBound)/2
        self.eggW = 10
        self.eggH = 10
        self.eColor = "light goldenrod"
    
    def gotEgg(self,bird):
    
        distance = ((self.eggX - bird.birdX)**2 + (self.eggY - bird.birdY)**2)**0.5
        if bird.birdW/2+20 + self.eggW/2 > distance:
            return True
        return False
    

    def draw(self,canvas):
        canvas.create_oval(self.eggX - 10, self.eggY - 10,
                            self.eggX + 10, self.eggY + 10,
                            fill = self.eColor)      

class PlayMode(Mode):
    def __init__(self,color, *initialState, name = "play", **kwargs):
        self.color = color
        
        super().__init__(name = name)
    def appStarted(self):
        """
        has a bird and has a list of the pipes and ghosts. The pipes
        and ghost lists will hold indivual sets of pipes and ghosts
        """
        self.backgroundDay = self.loadImage('background-day.png')
        self.backgroundW, self.backgroundH = self.backgroundDay.size
        self.backgroundDay = self.scaleImage(self.backgroundDay,850/self.backgroundH)

        self.zero = self.loadImage('0.png')
        self.one = self.loadImage('1.png')
        self.two = self.loadImage('2.png')
        self.three = self.loadImage('3.png')
        self.four = self.loadImage('4.png')
        self.five = self.loadImage('5.png')
        self.six = self.loadImage('6.png')
        self.seven = self.loadImage('7.png')
        self.eight = self.loadImage('8.png')
        self.nine = self.loadImage('9.png')
        self.numbers = [self.zero,self.one,self.two,self.three,self.four,self.five,self.six,self.seven,self.eight,self.nine]
      

        self.blueBirdUp = self.loadImage('bluebird-upflap.png')
        self.blueBirdMid = self.loadImage('bluebird-midflap.png')
        self.blueBirdDown = self.loadImage('bluebird-downflap.png')
        self.redBirdUp = self.loadImage('redbird-upflap.png')
        self.redBirdMid = self.loadImage('redbird-midflap.png')
        self.redBirdDown = self.loadImage('redbird-downflap.png')
        self.yellowBirdUp = self.loadImage('yellowbird-upflap.png')
        self.yellowBirdMid = self.loadImage('yellowbird-midflap.png')
        self.yellowBirdDown = self.loadImage('yellowbird-downflap.png')

        self.birdW,self.birdH = self.yellowBirdMid.size
        self.blueBirdUp = self.scaleImage(self.blueBirdUp,50/self.birdW)
        self.blueBirdMid = self.scaleImage(self.blueBirdMid,50/self.birdW)
        self.blueBirdDown = self.scaleImage(self.blueBirdDown, 50/self.birdW)
        self.redBirdUp = self.scaleImage(self.redBirdUp,50/self.birdW)
        self.redBirdMid = self.scaleImage(self.redBirdMid, 50/self.birdW)
        self.redBirdDown = self.scaleImage(self.redBirdDown, 50/self.birdW)
        self.yellowBirdUp = self.scaleImage(self.yellowBirdUp, 50/self.birdW)
        self.yellowBirdMid = self.scaleImage(self.yellowBirdMid, 50/self.birdW)
        self.yellowBirdDown = self.scaleImage(self.yellowBirdDown, 50/self.birdW)
        self.birdW,self.birdH = self.yellowBirdMid.size


        self.blue = [self.blueBirdUp,self.blueBirdMid,self.blueBirdDown]
        self.red = [self.redBirdUp, self.redBirdMid, self.redBirdDown]
        self.yellow = [self.yellowBirdUp, self.yellowBirdMid, self.yellowBirdDown]
        
        self.pipe = self.loadImage('pipe.png')
        self.pipeW,self.pipeH = self.pipe.size
        self.pipe = self.scaleImage(self.pipe, 490/self.pipeH)
        self.pipe = self.pipe.resize((80,800))
        self.pipeW,self.pipeH = self.pipe.size
        

        self.ghostImage = self.loadImage('ghost.png')
        self.ghostW,self.ghostH = self.ghostImage.size
        self.ghostImage = self.scaleImage(self.ghostImage,40/self.ghostH)
        
        if self.color == "blue":
            self.bird = Bird(self,self.blue)
        elif self.color == "red":
            self.bird = Bird(self,self.red)
        elif self.color == "yellow":
            self.bird = Bird(self,self.yellow)

        self.pipes = []
        self.countedPipes =set()
        self.ghosts = []
        self.countedGhosts = set()
        self.eggs = []
        self.countedEggs = set()
        self.time = 0
        self.score = 0
        self.scrollX = -20
        #since the pipes do not move up and down, the pipes will inly move left
        #this will give the impression that the bird is moving right
    
    def modeActivated(self):
        self.appStarted()

    def gameOver(self,pipes,ghosts,eggs,score):
        self.setActiveMode(GameOverMode(pipes,ghosts,eggs,score))

    def hitsBorders(self):
        """
        This checks if the bird flew out of the screen either above or 
        below. If it has flew off the screen, it will automaticaly be dropped. 
        This can also be used to check if it has died yet 
        """
        if self.bird.birdY < self.bird.birdH or self.bird.birdY > self.height - self.bird.birdH:
            return True
        return False

    def keyPressed(self,event):
        """
        The only key that we will use is the spacebar. The spacebar is 
        the only thing that will allow the bird to flap up
        """
        if event.key == "Space":
            self.hasStarted = True
            #since the bird can only go up, the y coordinate will change negatively
            upVelocity = -80
            self.bird.move(upVelocity)
          

    def spawnGhost(self):
        num = random.randrange(1,5)
        if num == 1:
            return True
        return False

    def level(self,level):
        if level == "easy": 
            if not self.spawnGhost():
                gap = self.bird.birdH + 160
                pHeight = random.randrange(self.height//7*3, self.height//7*4)
                self.pipes.append(Pipe(self,pHeight,gap,self.pipe))
            else: 
                self.ghosts.append(Ghost(self,self.ghostImage))
                self.eggs.append(Egg(self))
                
            if level == "medium":
                if not self.spawnGhost():
                    gap = self.bird.birdH + 20
                    pHeight = random.randrange(self.height//7*2, self.height//7*5)
                    self.pipes.append(Pipe(self,pHeight,gap,self.pipe))
                    
                else:
                    self.ghosts.append(Ghost(self,self.ghostImage))
                    self.eggs.append(Egg(self))

            if level == "hard":
                if not self.spawnGhost():
                    gap = self.bird.birdH + 50
                    pHeight = random.randrange(gap, self.height - gap)
                    self.pipes.append(Pipe(self,pHeight,gap,self.pipe))
                   
                else: 
                    self.ghosts.append(Ghost(self, self.ghostImage))
                    self.eggs.append(Egg(self))
    
    def scrollPipes(self):
        for pipe in self.pipes:
            pipe.pipeX += self.scrollX 
            
            if pipe.passesPipe(self.bird) and pipe not in self.countedPipes:
                self.score += 1
                self.countedPipes.add(pipe)

            if pipe.hitsPipe(self.bird):
                self.gameOver(self.pipes,self.ghosts,self.eggs,self.score)
            
            #this will pop the pipe after it leaves the screen
            if pipe.pipeX + pipe.pipeW/2 < 0:
                self.pipes.pop(0)

    def scrollGhosts(self):
        for ghost in self.ghosts:
            ghost.ghostX += self.scrollX
            ghost.move()
            if ghost.hitsGhost(self.bird):
                self.gameOver(self.pipes,self.ghosts,self.eggs,self.score)
            
            if ghost.ghostX + ghost.ghostW/2 < 0:
                self.ghosts.pop(0)

    def scrollEggs(self):
        for egg in self.eggs:
            egg.eggX += self.scrollX
            if egg.gotEgg(self.bird):
                self.score+=5
                self.eggs.remove(egg)  
            
            if egg.eggX + egg.eggW/2 <0:
                self.eggs.pop(0)

    
    def timerFired(self):
        """
         in each timerFired, the bird will move down. However, the up velocity 
         will be greater than the down to allow it to move
        """        
        self.time += self.timerDelay
        minute = 60000
    
       
        if self.time % 1500 == 0:
            if self.timerDelay < minute: 
                self.level("easy") 
            elif self.timerDelay < minute*5:
                self.level("medium")       
            else:
                self.level("hard")

        self.scrollPipes()
        self.scrollGhosts()  
        self.scrollEggs()
    
        #this will basically drop the ball
    
        downVelocity = 25 
        self.bird.move(downVelocity)  
        self.bird.changeImage()
        if self.hitsBorders():
            self.gameOver(self.pipes,self.ghosts,self.eggs,self.score)

            
        
    def redrawAll(self,canvas):
        """
        Draws the pipes and the bird
        """
        canvas.create_image(self.width/2,self.height/2,
                            image = ImageTk.PhotoImage(self.backgroundDay))
        for pipe in self.pipes: 
            pipe.draw(canvas)
        
        for egg in self.eggs:
            egg.draw(canvas)
        
        for ghost in self.ghosts:
            ghost.draw(canvas)

        canvas.create_text(self.width/2,30, text = self.score, font = "Times 40", fill = "white")
        self.bird.draw(canvas)


class FlappyBirdFamily(ModalApp):
    def appStarted(self):
        self.addMode(StartMode(name = "start"))
        self.addMode(HelpMode(name = "help"))
        self.setActiveMode("start")

FlappyBirdFamily(width=1536,height = 801)