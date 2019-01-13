import pygame
from pygame.locals import *
from numpy import loadtxt
import time
import random

import fromArduino


#Constants for the game
WIDTH, HEIGHT = (64, 64)
WALL_COLOR = pygame.Color(198, 137, 137, 255) # BLUE

#yellow,blue,green
COLOR = [pygame.Color(255, 255, 0, 255), pygame.Color(66, 191, 244,255), pygame.Color(157, 191, 89,100), pygame.Color(255, 0, 0, 255)] 
DOWN = (0,1)
RIGHT = (0.5,0)
LEFT = (-0.5,0)

coinRow=1

img=pygame.image.load('win.jpg')
img1=pygame.image.load('lose.png')


#Draws a rectangle for the wall
def draw_wall(screen, pos):
	pixels = pixels_from_points(pos)
	pygame.draw.rect(screen, WALL_COLOR, [pixels, (WIDTH, HEIGHT)])

#Draws a circle for the player
def draw_man(screen, pos,randColor): 
	pixels = pixels_from_points(pos)
	pygame.draw.ellipse(screen, COLOR[randColor], [pixels, (WIDTH, HEIGHT)])
	pygame.draw.polygon(screen,pygame.Color(130,91,67,255),[(pixels[0]+1, pixels[1]), (pixels[0]-1, pixels[1]),(pixels[0]-4, pixels[1]-30)],2)
	pygame.draw.ellipse(screen, pygame.Color(90,99,114,255), [pixels, (WIDTH/2, HEIGHT/2)],4)
	pygame.draw.ellipse(screen, pygame.Color(90,99,114,255), [(pixels[0]+30,pixels[1]),(WIDTH/2, HEIGHT/2)],4)

#Draws a rcircle for the coin
def draw_coin(screen, pos, randColor):
	pixels = pixels_from_points(pos)
	pygame.draw.ellipse(screen, COLOR[randColor], [pixels, (WIDTH*0.75, HEIGHT*0.75)])

def draw_coinShadow(screen, pos, randColor):
	pixels = pixels_from_points(pos)
	pygame.draw.ellipse(screen, COLOR[randColor], [pixels, (WIDTH*0.75-pos[1]*2, HEIGHT*0.75-pos[1]*2)])

def draw_Star(screen,pos):
	pixels=pixels_from_points(pos)
	pygame.draw.line(screen, pygame.Color(229,203,98,255),[pixels[0]-4, pixels[1]-33],[pixels[0]-4, pixels[1]-27],2)
	pygame.draw.line(screen, pygame.Color(229,203,98,255),[pixels[0]-8, pixels[1]-31],[pixels[0]+2, pixels[1]-26],2)
	pygame.draw.line(screen, pygame.Color(229,203,98,255),[pixels[0]+2, pixels[1]-31],[pixels[0]-8, pixels[1]-26],2)

#Uitlity functions
def add_to_pos(pos, pos2):
	return (pos[0]+pos2[0], pos[1]+pos2[1])
def pixels_from_points(pos):
	return (pos[0]*WIDTH, pos[1]*HEIGHT)




#Initializing pygame
pygame.init()
screen = pygame.display.set_mode((640,640), 0, 32)
background = pygame.surface.Surface((640,640)).convert()

pygame.display.set_caption('Baux')

pygame.mixer.music.load("bgmusic.mp3")
pygame.mixer.music.play(loops=5, start=0.0)


pygame.font.init() 
screen.fill(WALL_COLOR)
myfont=pygame.font.SysFont("system", 30)




#Initializing variables
man_position = (4,9)
#print(pixels_from_points((4,9)))
background.fill((0,0,0))

coinTimer=0
coinPos=[]
coinColor=[]
man_color=random.randint(0,3)

colorScore=[0]*4
life=30
lastColor=-1

for i in range(5):
	coinPos.append((random.randint(0,30), coinRow))
	coinColor.append(random.randint(0,3))



def UpdateScore(man_position, coinPos,man_color, lastColor):
	global life
	global colorScore
	#print("life ", life)
	man_x=int(man_position[0])
	color=-1
	scoreFlag=False
	for i in range(5):
		if coinPos[i][1]==9:
			if coinPos[i][0]==man_x: 
				color=coinColor[i]
				
				scoreFlag=True
			else:
				life=life-1
			coinPos[i]=(-1,-1)
	if scoreFlag and man_color != color:
		life=life-1
		
		colorScore=[0]*4
		return color
		
	if scoreFlag and (lastColor==color or lastColor==-1):
		for i in range(4):
			if i==color:
				colorScore[color]=colorScore[color]+1
			else:
				colorScore[i]=0
		#print(color, colorScore[color])
	return color

# Main game loop 
while True:
	coinTimer=coinTimer+1
	v=fromArduino.func()


	for event in pygame.event.get():
		if event.type == QUIT:
			exit()

	screen.blit(background, (0,0))

	
	
	for col in range(10):		
		draw_wall(screen, (col,0))
			
	

	#Draw the player
	draw_man(screen, man_position,man_color)
	if coinTimer%150==0:
		man_color=random.randint(0,3)

	move_direction=(0,0)
	key=pygame.key.get_pressed()
	if (key[pygame.K_LEFT] or v[0]=='L'):
		move_direction=LEFT
	elif (key[pygame.K_RIGHT] or v[0]=='R'):
		move_direction=RIGHT

	#Update player position based on movement.

	temp_position = add_to_pos(man_position, move_direction)
	if temp_position[0]<0: temp_position=(9,9)
	if temp_position[0]>9: temp_position=(0,9)
	man_position=temp_position

	

	for i in range(5):
		validPos=-1<coinPos[i][0]<10 and -1<coinPos[i][1]<10 
	
			
		if validPos and coinPos[i][0]==int(man_position[0]) and (key[pygame.K_d] or v[1]=="D"):
			draw_Star(screen,man_position)
			#add sound effect
			pygame.mixer.Channel(1).play(pygame.mixer.Sound('beep-03.wav'), maxtime=100)			
			coinPos[i]=(-1,-1)


		if validPos and coinPos[i][0]==int(man_position[0]) and (key[pygame.K_a] or v[1]=="A"):
			while coinPos[i][1]<9:
				draw_coinShadow(screen, coinPos[i], coinColor[i])
				coinPos[i]=add_to_pos(coinPos[i], DOWN)
			
			pygame.mixer.Channel(1).play(pygame.mixer.Sound('beep-02.wav'), maxtime=100)
			
			continue

	
		if validPos:
			draw_coin(screen, coinPos[i], coinColor[i])
			
			if coinTimer % 4==0:
				coinPos[i]=add_to_pos(coinPos[i],DOWN)
		else:
			if coinTimer % 4==0:	
				coinPos[i]=(random.randint(0,30),coinRow)
				coinColor[i]=random.randint(0,3)


	lastColor=UpdateScore(man_position, coinPos,man_color, lastColor)
	endFlag=None
	for i in colorScore:
		if i>=3:
			endFlag=1
			
	if life<=0:
		endFlag=0
	if endFlag==1:
		screen.blit(img,(0,0))
		pygame.display.flip()
		time.sleep(2)
		break
	elif endFlag==0:
		screen.blit(img1,(0,0))
		pygame.display.flip()
		time.sleep(2)
		break
		
	#Update the display

	scoretextR=myfont.render("R:"+str(colorScore[3]), 1, (255,0,0))
	scoretextG=myfont.render("G:"+str(colorScore[2]), 1, (33, 140, 69))
	scoretextY=myfont.render("Y:"+str(colorScore[0]), 1, (209, 192, 66))
	scoretextB=myfont.render("B:"+str(colorScore[1]), 1, (120, 200, 232))
	lifetext=myfont.render("life:"+str(life), 1, (140, 33, 81))

	screen.blit(scoretextR, (5,20))
	screen.blit(scoretextG, (55,20))
	screen.blit(scoretextY, (105,20))
	screen.blit(scoretextB, (155,20))
	screen.blit(lifetext, (500,20))
	pygame.display.update()

	time.sleep(0.1)