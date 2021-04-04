#! python3

import copy
import tkinter, math, time, keyboard, random
from dataclasses import dataclass, field

# to install PIL, install package 'pillow' instead
from PIL import Image, ImageTk
from enum import IntEnum
from typing import List  # aby som mohol mat v dataclasse zoznam
from pygame import mixer  # zvuk

import aiLogic



okno = tkinter.Tk()
okno.title('Bomberman')

okno.focus_force()  # aby sa stalo aktivnym oknom (a bralo keyboard input)

sirka = 64 * 15 + 276  # playable area je 13*11 ale s krajmi je 15*13 + scoreboard
vyska = 64 * 13  # 64*64

platno = tkinter.Canvas(width=sirka, height=vyska)
platno.grid(column=0, row=0)
background = tkinter.PhotoImage(file='other_textures/bg64.png')
crateImg = tkinter.PhotoImage(file='other_textures/crate64.png')


wallImg = Image.open('other_textures/wall2.png')
wallImg = wallImg.resize((64, 64), Image.ANTIALIAS)
wallImg = ImageTk.PhotoImage(wallImg)

colors = ['color2', 'color3', 'color4', 'color5', 'color6']
player1color = 'color1'
player2color = random.choice(colors)  # random farby pre vsetky AI
colors.pop(colors.index(player2color))
player3color = random.choice(colors)
colors.pop(colors.index(player3color))
player4color = random.choice(colors)
colors.pop(colors.index(player4color))

subor = open('sound/settings.txt', 'r')
for i in subor:
	i.strip()
	if i == 'on':
		sound_settings = True
	elif i == 'off':
		sound_settings = False
	else:
		sound_settings = False
subor.close()

mixer.init()
mixer.music.load('sound/Decktonic_-_Night_Drive_(Strong Suit Remix).wav')
if sound_settings:
	mixer.music.play(-1)

bomb_place_sound = mixer.Sound('sound/bomb_place.wav')
explosion_sound = mixer.Sound('sound/explosion.wav')
death_sound = mixer.Sound('sound/death.wav')
victory_sound = mixer.Sound('sound/victory.wav')


playerSprites = []
for i in range(10):
	playerImg = Image.open(f'bomberman_sprites/{player1color}/tile00{i}.png')
	playerImg = playerImg.resize((44, 87), Image.ANTIALIAS)
	playerImg = ImageTk.PhotoImage(playerImg)
	playerSprites.append(playerImg)
for i in range(10, 16):
	playerImg = Image.open(f'bomberman_sprites/{player1color}/tile0{i}.png')
	playerImg = playerImg.resize((44, 87), Image.ANTIALIAS)
	playerImg = ImageTk.PhotoImage(playerImg)
	playerSprites.append(playerImg)

ai1Sprites = []
for i in range(10):
	playerImg = Image.open(f'bomberman_sprites/{player2color}/tile00{i}.png')
	playerImg = playerImg.resize((44, 87), Image.ANTIALIAS)
	playerImg = ImageTk.PhotoImage(playerImg)
	ai1Sprites.append(playerImg)
for i in range(10, 16):
	playerImg = Image.open(f'bomberman_sprites/{player2color}/tile0{i}.png')
	playerImg = playerImg.resize((44, 87), Image.ANTIALIAS)
	playerImg = ImageTk.PhotoImage(playerImg)
	ai1Sprites.append(playerImg)

ai2Sprites = []
for i in range(10):
	playerImg = Image.open(f'bomberman_sprites/{player3color}/tile00{i}.png')
	playerImg = playerImg.resize((44, 87), Image.ANTIALIAS)
	playerImg = ImageTk.PhotoImage(playerImg)
	ai2Sprites.append(playerImg)
for i in range(10, 16):
	playerImg = Image.open(f'bomberman_sprites/{player3color}/tile0{i}.png')
	playerImg = playerImg.resize((44, 87), Image.ANTIALIAS)
	playerImg = ImageTk.PhotoImage(playerImg)
	ai2Sprites.append(playerImg)

ai3Sprites = []
for i in range(10):
	playerImg = Image.open(f'bomberman_sprites/{player4color}/tile00{i}.png')
	playerImg = playerImg.resize((44, 87), Image.ANTIALIAS)
	playerImg = ImageTk.PhotoImage(playerImg)
	ai3Sprites.append(playerImg)
for i in range(10, 16):
	playerImg = Image.open(f'bomberman_sprites/{player4color}/tile0{i}.png')
	playerImg = playerImg.resize((44, 87), Image.ANTIALIAS)
	playerImg = ImageTk.PhotoImage(playerImg)
	ai3Sprites.append(playerImg)

bombSprites = []
for i in range(8):
	bombImg = Image.open(f'bomb_sprites/tile00{i}.png')
	bombImg = bombImg.resize((48, 48), Image.ANTIALIAS)
	bombImg = ImageTk.PhotoImage(bombImg)
	bombSprites.append(bombImg)

explosionSpritesUp = []
explosionSpritesLeft = []
explosionSpritesDown = []
explosionSpritesRight = []

for i in range(10):
	expImg = Image.open(f'explosion_sprites/tile00{i}.png')
	expImg = ImageTk.PhotoImage(expImg)
	explosionSpritesRight.append(expImg)

	expImg = Image.open(f'explosion_sprites/tile00{i}.png')
	expImg = expImg.rotate(90)
	expImg = ImageTk.PhotoImage(expImg)
	explosionSpritesUp.append(expImg)

	expImg = Image.open(f'explosion_sprites/tile00{i}.png')
	expImg = expImg.rotate(180)
	expImg = ImageTk.PhotoImage(expImg)
	explosionSpritesLeft.append(expImg)

	expImg = Image.open(f'explosion_sprites/tile00{i}.png')
	expImg = expImg.rotate(-90)
	expImg = ImageTk.PhotoImage(expImg)
	explosionSpritesDown.append(expImg)

for i in range(10, 21):
	expImg = Image.open(f'explosion_sprites/tile0{i}.png')
	expImg = ImageTk.PhotoImage(expImg)
	explosionSpritesRight.append(expImg)

	expImg = Image.open(f'explosion_sprites/tile0{i}.png')
	expImg = expImg.rotate(90)
	expImg = ImageTk.PhotoImage(expImg)
	explosionSpritesUp.append(expImg)

	expImg = Image.open(f'explosion_sprites/tile0{i}.png')
	expImg = expImg.rotate(180)
	expImg = ImageTk.PhotoImage(expImg)
	explosionSpritesLeft.append(expImg)

	expImg = Image.open(f'explosion_sprites/tile0{i}.png')
	expImg = expImg.rotate(-90)
	expImg = ImageTk.PhotoImage(expImg)
	explosionSpritesDown.append(expImg)

amountUpImg = Image.open('other_textures/amount/plus.png')
amountUpImg = ImageTk.PhotoImage(amountUpImg)
amountFullImg = Image.open('other_textures/amount/full.png')
amountFullImg = ImageTk.PhotoImage(amountFullImg)
amountDownImg = Image.open('other_textures/amount/down.png')
amountDownImg = amountDownImg.resize((32, 32), Image.ANTIALIAS)
amountDownImg = ImageTk.PhotoImage(amountDownImg)

rangeUpImg = Image.open('other_textures/range/plus.png')
rangeUpImg = ImageTk.PhotoImage(rangeUpImg)
rangeFullImg = Image.open('other_textures/range/full.png')
rangeFullImg = ImageTk.PhotoImage(rangeFullImg)
rangeDownImg = Image.open('other_textures/range/down.png')
rangeDownImg = rangeDownImg.resize((32, 32), Image.ANTIALIAS)
rangeDownImg = ImageTk.PhotoImage(rangeDownImg)

speedUpImg = Image.open('other_textures/speed/plus.png')
speedUpImg = ImageTk.PhotoImage(speedUpImg)
#rangeFullImg = Image.open('other_textures/range/full.png')
#rangeFullImg = ImageTk.PhotoImage(rangeFullImg)
speedDownImg = Image.open('other_textures/speed/down.png')
speedDownImg = ImageTk.PhotoImage(speedDownImg)

vestImg = Image.open('other_textures/vest.png')
vestImg = ImageTk.PhotoImage(vestImg)

piercingImg = Image.open('other_textures/pierceBomb.png')
piercingImg = ImageTk.PhotoImage(piercingImg)



dead = Image.open(f'other_textures/dead.png')
dead = dead.resize((130, 130), Image.ANTIALIAS)
dead = ImageTk.PhotoImage(dead)


class Policko(IntEnum):
	krabica = 0
	stena = 1
	volne = 2
	bomba = 3

	expStred = 10
	expDoleStred = 11
	expDoleKoniec = 12
	expHoreStred = 13
	expHoreKoniec = 14
	expVpravoStred = 15
	expVpravoKoniec = 16
	expVlavoStred = 17
	expVlavoKoniec = 18

@dataclass
class ai1_stats:

	moving = False
	vestStartTime: float = 0
	startX: int = 0  # zaciatok pohybu o 1 policko
	startY: int = 0
	movingDirection: str = 'up'
	placeBomb = False  # ci ma polozit bombu
	bombPlaced: int = 0  # pocet uz polozenych bomb
	bombAmount: int = 1  # max pocet polozenych bomb
	bombRange: int = 0
	speedRegulator: int = 0
	animCounter: int = 0
	path: str = 'none'
	lastPath = 'none'  # aby sa animacia zmenila hned co zmeni smer
	bombRangeFull: str = 'no'
	playerSpeed: int = 2
	vest: str = 'no'
	piercing: str = 'no'
	name: str = 'ai1'
	job: str = 'none'
	dead: bool = False
	coords: List[str] = field(default_factory=list)
	board_objects: List[str] = field(default_factory=list)

	current_target_powerup_list: List[str] = field(default_factory=list)  # cely zoznam co A* vypluje
	current_listXY: List[str] = field(default_factory=list)  # X, Y suradnice podla kt. sa orientuje v zozname^
a = ai1_stats()
ai1_stats = a

@dataclass
class ai2_stats:

	moving = False
	vestStartTime: float = 0
	startX: int = 0  # zaciatok pohybu o 1 policko
	startY: int = 0
	movingDirection: str = 'up'
	placeBomb = False  # ci ma polozit bombu
	bombPlaced: int = 0  # pocet uz polozenych bomb
	bombAmount: int = 1  # max pocet polozenych bomb
	bombRange: int = 0
	speedRegulator: int = 0
	animCounter: int = 0
	path: str = 'none'
	lastPath = 'none'  # aby sa animacia zmenila hned co zmeni smer
	bombRangeFull: str = 'no'
	playerSpeed: int = 2
	vest: str = 'no'
	piercing: str = 'no'
	name: str = 'ai2'
	job: str = 'none'
	dead: bool = False
	coords: List[str] = field(default_factory=list)
	board_objects: List[str] = field(default_factory=list)

	current_target_powerup_list: List[str] = field(default_factory=list)  # cely zoznam co A* vypluje
	current_listXY: List[str] = field(default_factory=list)  # X, Y suradnice podla kt. sa orientuje v zozname^
a = ai2_stats()
ai2_stats = a

@dataclass
class ai3_stats:

	moving = False
	vestStartTime: float = 0
	startX: int = 0  # zaciatok pohybu o 1 policko
	startY: int = 0
	movingDirection: str = 'up'
	placeBomb = False  # ci ma polozit bombu
	bombPlaced: int = 0  # pocet uz polozenych bomb
	bombAmount: int = 1  # max pocet polozenych bomb
	bombRange: int = 0
	speedRegulator: int = 0
	animCounter: int = 0
	path: str = 'none'
	lastPath = 'none'  # aby sa animacia zmenila hned co zmeni smer
	bombRangeFull: str = 'no'
	playerSpeed: int = 2
	vest: str = 'no'
	piercing: str = 'no'
	name: str = 'ai3'
	job: str = 'none'
	dead: bool = False
	coords: List[str] = field(default_factory=list)
	board_objects: List[str] = field(default_factory=list)

	current_target_powerup_list: List[str] = field(default_factory=list)  # cely zoznam co A* vypluje
	current_listXY: List[str] = field(default_factory=list)  # X, Y suradnice podla kt. sa orientuje v zozname^
a = ai3_stats()
ai3_stats = a


@dataclass
class PlayerPowerups:
	vestStartTime: float = 0
	bombAmount: int = 1
	bombRange: int = 0
	bombRangeFull: str = 'no'
	playerSpeed: int = 2
	vest: str = 'no'
	piercing: str = 'no'
	coords: List[str] = field(default_factory=list)
	name: str = 'player1'
	job: str = 'none'
	dead: bool = False
	board_objects: List[str] = field(default_factory=list)
a = PlayerPowerups()
PlayerPowerups = a

def createClass():
	@dataclass
	class Tile:

		obj: []  # tkinter objekt
		powerupObj: []
		bombParent: str
		bombRange: int  # bomb info
		bombRangeFull: str = 'no'  # bomb info
		rotation: str = 'up'  # exp rotation
		tileName: str = ''
		powerup = ''
		walkable: str = 'yes'  # aby sa dalo zist z bomby, ale naspat na nu vojst ne
		bolTuCrate: str = 'no'  # pri classic vybuchoch, exp rozbija max 1 krabicu
		piercingBomb: str = 'no'  # bomb info
		aiSeen: str = 'no'  # pathfinding
		cislo: int = 0  # viz. class Policko
		expCislo = 0  # nwm ci sa vobec pouziva
		frame: int = 0  # exp frame
	return Tile


def playerAnim(counter):
	global playerAnimCounter
	global player_animSpeedRegulator
	if playerRotation == 'up':
		if player_animSpeedRegulator == 10:

			if counter >= 4:
				counter = 0
			platno.itemconfig(player, image=playerSprites[counter])
			playerAnimCounter = counter + 1
			platno.update()
			player_animSpeedRegulator = 0
		else:
			player_animSpeedRegulator += 1
	if playerRotation == 'down':
		if player_animSpeedRegulator == 10:
			if (counter < 8) or (counter > 11):
				counter = 8
			platno.itemconfig(player, image=playerSprites[counter])
			playerAnimCounter = counter + 1
			platno.update()
			player_animSpeedRegulator = 0
		else:
			player_animSpeedRegulator += 1
	if playerRotation == 'right':
		if player_animSpeedRegulator == 10:
			if (counter < 4) or (counter > 7):
				counter = 4
			platno.itemconfig(player, image=playerSprites[counter])
			playerAnimCounter = counter + 1
			platno.update()
			player_animSpeedRegulator = 0
		else:
			player_animSpeedRegulator += 1
	if playerRotation == 'left':
		if player_animSpeedRegulator == 10:
			if (counter < 12) or (counter > 15):
				counter = 12
			platno.itemconfig(player, image=playerSprites[counter])
			playerAnimCounter = counter + 1
			platno.update()
			player_animSpeedRegulator = 0
		else:
			player_animSpeedRegulator += 1


def placeBomb(event):  # AI bude mat svoju funkciu na davanie bomb lebo toto je event??
	global playerPlacedBombs

	if playerPlacedBombs < PlayerPowerups.bombAmount:
		x = math.floor(platno.coords(player)[0] / 64)
		y = math.floor((platno.coords(player)[1] + 20) / 64)
		if obstaclesMatrix[y][x].cislo != Policko.bomba:
			if sound_settings:
				mixer.Sound.play(bomb_place_sound)

			bomba = platno.create_image(x * 64 + 32, y * 64 + 32, image=bombSprites[0])
			obstaclesMatrix[y][x].obj = bomba
			obstaclesMatrix[y][x].cislo = Policko.bomba
			obstaclesMatrix[y][x].bombRange = PlayerPowerups.bombRange
			obstaclesMatrix[y][x].bombRangeFull = PlayerPowerups.bombRangeFull
			obstaclesMatrix[y][x].bombParent = 'player1'
			platno.tag_raise(player)
			playerPlacedBombs += 1
			bombTimerBomb.append(bomba)
			bombTimerTime.append(time.time())

			if PlayerPowerups.piercing == 'yes':
				obstaclesMatrix[y][x].piercingBomb = 'yes'

			unwalkableBomb.append(math.floor((platno.coords(player)[0]) / 64))
			unwalkableBomb.append(math.floor((platno.coords(player)[1]) / 64))


def animBombs():
	global bombAnimCounter
	if bombAnimCounter > 7:
		bombAnimCounter = 0
	for i in range(13):
		for e in range(15):
			if obstaclesMatrix[i][e].cislo == Policko.bomba:
				platno.itemconfig(obstaclesMatrix[i][e].obj, image=bombSprites[bombAnimCounter])
	bombAnimCounter += 1
	platno.update()


def checkBombs():
	global bombTimerBomb, playerPlacedBombs, bombTimerTime
	cas = time.time()
	for f in range(len(bombTimerTime)):
		if cas - bombTimerTime[f] > 2:
			if bombTimerTime[f] != 0:
				if (obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)]
									[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombRangeFull == 'yes'):  # full ma full classic bez aj s piercingom

					if (obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)]
					[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'player1'):
						playerPlacedBombs += -1
					elif obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)] \
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'ai1':
						ai1_stats.bombPlaced += -1
					elif obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)] \
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'ai2':
						ai2_stats.bombPlaced += -1
					elif obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)] \
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'ai3':
						ai3_stats.bombPlaced += -1

					explosionFull_only_or_also_Piercing(bombTimerBomb[f])
				elif (obstaclesMatrix[math.floor(platno.coords(bombTimerBomb[f])[1] / 64)]
									[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].piercingBomb == 'yes'):  # piercing classic

					if (obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)]
					[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'player1'):
						playerPlacedBombs += -1
					elif obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)] \
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'ai1':
						ai1_stats.bombPlaced += -1
					elif obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)] \
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'ai2':
						ai2_stats.bombPlaced += -1
					elif obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)] \
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'ai3':
						ai3_stats.bombPlaced += -1

					explosionPiercing_only(bombTimerBomb[f])
				else:  # classic

					if (obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)]
					[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'player1'):
						playerPlacedBombs += -1
					elif obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)] \
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'ai1':
						ai1_stats.bombPlaced += -1
					elif obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)] \
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'ai2':
						ai2_stats.bombPlaced += -1
					elif obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)] \
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent == 'ai3':
						ai3_stats.bombPlaced += -1

					explosionClassic(bombTimerBomb[f])



				platno.delete(bombTimerBomb[f])
				platno.update()
				bombTimerTime[f] = 0


def expPlacementJudge(y, x, baseTileExp):
	global obstaclesMatrix
	if (x > 13) or (x < 0):
		return False
	if (y > 11) or (y < 0):
		return False
	if baseTileExp == 'yes':
		return True
	if (obstaclesMatrix[y][x].cislo == Policko.stena) or \
		(obstaclesMatrix[y][x].cislo == Policko.bomba):
		return False  # viac moznosti na to co ma vybuch zastavit
	else:
		return True


def createExp(x, y, position, smer):
	global obstaclesMatrix, obstaclesMatrix, unwalkableBomb # menim x a y



	if obstaclesMatrix[y][x].cislo == Policko.krabica:
		platno.delete(obstaclesMatrix[y][x].obj)

	if obstaclesMatrix[y][x].cislo != Policko.bomba:
		if position != Policko.expStred:
			exp = platno.create_image(x * 64 + 32, y * 64 + 32, image=explosionSpritesUp[7])
			try:
				platno.delete(obstaclesMatrix[y][x].obj)
			except:
				pass
			obstaclesMatrix[y][x].obj = exp
			obstaclesMatrix[y][x].expCislo = position
			obstaclesMatrix[y][x].rotation = smer
			obstaclesMatrix[y][x].tileName = 'explosion'
	if position == Policko.expStred:
		exp = platno.create_image(x * 64 + 32, y * 64 + 32, image=explosionSpritesUp[7])
		try:
			platno.delete(obstaclesMatrix[y][x].obj)
		except:
			pass
		obstaclesMatrix[y][x].obj = exp
		obstaclesMatrix[y][x].expCislo = position
		obstaclesMatrix[y][x].cislo = Policko.volne
		obstaclesMatrix[y][x].rotation = smer
		obstaclesMatrix[y][x].tileName = 'explosion'

	obstaclesMatrix[y][x].walkable = 'yes'


def explosionClassic(bomba):
	global obstaclesMatrix
	x = 0
	y = 0
	if len(platno.coords(bomba)) > 0:
		y = math.floor(platno.coords(bomba)[0] / 64)
		x = math.floor(platno.coords(bomba)[1] / 64)
	else:
		print('non existing bomb')
	if sound_settings:
		mixer.Sound.play(explosion_sound)

	if expPlacementJudge(x, y, 'yes'):  # stred
		createExp(y, x, Policko.expStred, 'up')


	if expPlacementJudge(x + 1, y, 'no'):  #                  dole, prve
		if obstaclesMatrix[x + 1][y].cislo == Policko.krabica:
			obstaclesMatrix[x + 1][y].bolTuCrate = 'yes'
		createExp(y, x + 1, Policko.expDoleKoniec, 'down')

	if obstaclesMatrix[x][y].bombRange >= 1:
		if (0 < x + 2 < 11) and (0 < y <= 13):
			if obstaclesMatrix[x + 2][y].cislo == Policko.krabica:
				obstaclesMatrix[x + 2][y].bolTuCrate = 'yes'
		if (expPlacementJudge(x + 1, y, 'no'))\
				and (obstaclesMatrix[x + 1][y].bolTuCrate != 'yes'):
			if expPlacementJudge(x + 2, y, 'no'):
				createExp(y, x + 2, Policko.expDoleKoniec, 'down')  #  dole, druhe
				obstaclesMatrix[x + 1][y].expCislo = Policko.expDoleStred

	if obstaclesMatrix[x][y].bombRange >= 2:
		if (0 < x + 3 < 11) and (0 < y <= 13):
			if obstaclesMatrix[x + 3][y].cislo == Policko.krabica:
				obstaclesMatrix[x + 3][y].bolTuCrate = 'yes'
		if (expPlacementJudge(x + 2, y, 'no'))\
				and (obstaclesMatrix[x + 2][y].bolTuCrate != 'yes') and (expPlacementJudge(x + 1, y, 'no')) \
				and (obstaclesMatrix[x + 1][y].bolTuCrate != 'yes'):
			if expPlacementJudge(x + 3, y, 'no'):
				createExp(y, x + 3, Policko.expDoleKoniec, 'down')  # dole, tretie
				obstaclesMatrix[x + 2][y].expCislo = Policko.expDoleStred

	if obstaclesMatrix[x][y].bombRange >= 3:
		if (expPlacementJudge(x + 3, y, 'no'))\
				and (obstaclesMatrix[x + 3][y].bolTuCrate != 'yes') and (expPlacementJudge(x + 2, y, 'no')) \
				and (obstaclesMatrix[x + 2][y].bolTuCrate != 'yes') and (expPlacementJudge(x + 1, y, 'no')) \
				and (obstaclesMatrix[x + 1][y].bolTuCrate != 'yes'):
			if expPlacementJudge(x + 4, y, 'no'):
				createExp(y, x + 4, Policko.expDoleKoniec, 'down')  # dole, stvrte
				obstaclesMatrix[x + 3][y].expCislo = Policko.expDoleStred
	obstaclesMatrix[x + 1][y].bolTuCrate = 'no'
	if (0 < x + 2 < 11) and (0 < y <= 13):
		obstaclesMatrix[x + 2][y].bolTuCrate = 'no'
	if (0 < x + 3 < 11) and (0 < y <= 13):
		obstaclesMatrix[x + 3][y].bolTuCrate = 'no'

	if expPlacementJudge(x - 1, y, 'no'):  #                 hore, prve
		#print(f'hore {obstaclesMatrix[x][y - 1].cislo}')
		if obstaclesMatrix[x - 1][y].cislo == Policko.krabica:
			obstaclesMatrix[x - 1][y].bolTuCrate = 'yes'
		createExp(y, x - 1, Policko.expHoreKoniec, 'up')

	if (obstaclesMatrix[x][y].bombRange >= 1)\
			and (expPlacementJudge(x - 1, y, 'no')) and (obstaclesMatrix[x - 1][y].bolTuCrate != 'yes'):
		if expPlacementJudge(x - 2, y, 'no'):  #             hore, druhe
			if (0 < x - 2 < 11) and (0 < y <= 13):
				if obstaclesMatrix[x - 2][y].cislo == Policko.krabica:
					obstaclesMatrix[x - 2][y].bolTuCrate = 'yes'
			createExp(y, x - 2, Policko.expHoreKoniec, 'up')
			obstaclesMatrix[x - 1][y].expCislo = Policko.expHoreStred

	if (obstaclesMatrix[x][y].bombRange >= 2)\
			and (expPlacementJudge(x - 2, y, 'no')) and (obstaclesMatrix[x - 2][y].bolTuCrate != 'yes')\
			and (expPlacementJudge(x - 1, y, 'no')) and (obstaclesMatrix[x - 1][y].bolTuCrate != 'yes'):
		if (0 < x - 3 < 11) and (0 < y <= 13):
			if obstaclesMatrix[x - 3][y].cislo == Policko.krabica:
				obstaclesMatrix[x - 3][y].bolTuCrate = 'yes'
		if expPlacementJudge(x - 3, y, 'no'):#               hore, tretie
			createExp(y, x - 3, Policko.expHoreKoniec, 'up')
			obstaclesMatrix[x - 2][y].expCislo = Policko.expHoreStred

	if (obstaclesMatrix[x][y].bombRange >= 3)\
			and (expPlacementJudge(x - 3, y, 'no')) and (obstaclesMatrix[x - 3][y].bolTuCrate != 'yes')\
			and (expPlacementJudge(x - 2, y, 'no')) and (obstaclesMatrix[x - 2][y].bolTuCrate != 'yes') \
			and (expPlacementJudge(x - 1, y, 'no')) and (obstaclesMatrix[x - 1][y].bolTuCrate != 'yes'):
		if expPlacementJudge(x - 4, y, 'no'):#               hore, stvrte
			createExp(y, x - 4, Policko.expHoreKoniec, 'up')
			obstaclesMatrix[x - 3][y].expCislo = Policko.expHoreStred
	obstaclesMatrix[x - 1][y].bolTuCrate = 'no'
	if (0 < x - 2 < 11) and (0 < y <= 13):
		obstaclesMatrix[x - 2][y].bolTuCrate = 'no'
	if (0 < x - 3 < 11) and (0 < y <= 13):
		obstaclesMatrix[x - 3][y].bolTuCrate = 'no'

	if expPlacementJudge(x, y + 1, 'no'):  #                 vpravo, prve
		if obstaclesMatrix[x][y + 1].cislo == Policko.krabica:
			obstaclesMatrix[x][y + 1].bolTuCrate = 'yes'
		createExp(y + 1, x, Policko.expVpravoKoniec, 'right')

	if (obstaclesMatrix[x][y].bombRange >= 1)\
			and (expPlacementJudge(x, y + 1, 'no')) and (obstaclesMatrix[x][y + 1].bolTuCrate != 'yes'):
		if (0 < x <= 11) and (0 < y + 2 < 13):
			if obstaclesMatrix[x][y + 2].cislo == Policko.krabica:
				obstaclesMatrix[x][y + 2].bolTuCrate = 'yes'
		if expPlacementJudge(x, y + 2, 'no'):  #             vpravo, druhe
			createExp(y + 2, x, Policko.expVpravoKoniec, 'right')
			obstaclesMatrix[x][y + 1].expCislo = Policko.expVpravoStred

	if (obstaclesMatrix[x][y].bombRange >= 2)\
			and (expPlacementJudge(x, y + 2, 'no')) and (obstaclesMatrix[x][y + 2].bolTuCrate != 'yes')\
			and (expPlacementJudge(x, y + 1, 'no')) and (obstaclesMatrix[x][y + 1].bolTuCrate != 'yes'):
		if (0 < x <= 11) and (0 < y + 3 < 13):
			if obstaclesMatrix[x][y + 3].cislo == Policko.krabica:
				obstaclesMatrix[x][y + 3].bolTuCrate = 'yes'
		if expPlacementJudge(x, y + 3, 'no'):  #             vpravo, tretie
			createExp(y + 3, x, Policko.expVpravoKoniec, 'right')
			obstaclesMatrix[x][y + 2].expCislo = Policko.expVpravoStred

	if (obstaclesMatrix[x][y].bombRange >= 3)\
			and (expPlacementJudge(x, y + 3, 'no')) and (obstaclesMatrix[x][y + 3].bolTuCrate != 'yes')\
			and (expPlacementJudge(x, y + 2, 'no')) and (obstaclesMatrix[x][y + 2].bolTuCrate != 'yes') \
			and (expPlacementJudge(x, y + 1, 'no')) and (obstaclesMatrix[x][y + 1].bolTuCrate != 'yes'):
		if expPlacementJudge(x, y + 4, 'no'):  #             vpravo, stvrte
			createExp(y + 4, x, Policko.expVpravoKoniec, 'right')
			obstaclesMatrix[x][y + 3].expCislo = Policko.expVpravoStred
	obstaclesMatrix[x][y + 1].bolTuCrate = 'no'
	if (0 < x <= 11) and (0 < y + 2 < 13):
		obstaclesMatrix[x][y + 2].bolTuCrate = 'no'
	if (0 < x <= 11) and (0 < y + 3 < 13):
		obstaclesMatrix[x][y + 3].bolTuCrate = 'no'

	if expPlacementJudge(x, y - 1, 'no'):  #                 vlavo, prve
		if obstaclesMatrix[x][y - 1].cislo == Policko.krabica:
			obstaclesMatrix[x][y - 1].bolTuCrate = 'yes'
		createExp(y - 1, x, Policko.expVlavoKoniec, 'left')

	if (obstaclesMatrix[x][y].bombRange >= 1)\
			and (expPlacementJudge(x, y - 1, 'no')) and (obstaclesMatrix[x][y - 1].bolTuCrate != 'yes'):
		if expPlacementJudge(x, y - 2, 'no'):
			if (0 < x <= 11) and (0 < y - 2 < 13):
				if obstaclesMatrix[x][y - 2].cislo == Policko.krabica:
					obstaclesMatrix[x][y - 2].bolTuCrate = 'yes'
			createExp(y - 2, x, Policko.expVlavoKoniec, 'left')  #      vlavo, druhe
			obstaclesMatrix[x][y - 1].expCislo = Policko.expVlavoStred

	if (obstaclesMatrix[x][y].bombRange >= 2)\
			and (expPlacementJudge(x, y - 2, 'no')) and (obstaclesMatrix[x][y - 2].bolTuCrate != 'yes')\
			and (expPlacementJudge(x, y - 1, 'no')) and (obstaclesMatrix[x][y - 1].bolTuCrate != 'yes'):
		if (0 < x <= 11) and (0 < y - 3 < 13):
			if obstaclesMatrix[x][y - 3].cislo == Policko.krabica:
				obstaclesMatrix[x][y - 3].bolTuCrate = 'yes'
		if expPlacementJudge(x, y - 3, 'no'):
			createExp(y - 3, x, Policko.expVlavoKoniec, 'left')  #         vlavo, tretie
			obstaclesMatrix[x][y - 2].expCislo = Policko.expVlavoStred

	if (obstaclesMatrix[x][y].bombRange >= 3)\
			and (expPlacementJudge(x, y - 3, 'no')) and (obstaclesMatrix[x][y - 3].bolTuCrate != 'yes')\
			and (expPlacementJudge(x, y - 2, 'no')) and (obstaclesMatrix[x][y - 2].bolTuCrate != 'yes') \
			and (expPlacementJudge(x, y - 1, 'no')) and (obstaclesMatrix[x][y - 1].bolTuCrate != 'yes'):
		if expPlacementJudge(x, y - 4, 'no'):
			createExp(y - 4, x, Policko.expVlavoKoniec, 'left')  #         vlavo, stvrte
			obstaclesMatrix[x][y - 3].expCislo = Policko.expVlavoStred
	obstaclesMatrix[x][y - 1].bolTuCrate = 'no'
	if (0 < x <= 11) and (0 < y - 2 < 13):
		obstaclesMatrix[x][y - 2].bolTuCrate = 'no'
	if (0 < x <= 11) and (0 < y - 3 < 13):
		obstaclesMatrix[x][y - 3].bolTuCrate = 'no'


def explosionPiercing_only(bomba):
	global obstaclesMatrix
	x = 0
	y = 0
	if len(platno.coords(bomba)) > 0:
		y = math.floor(platno.coords(bomba)[0] / 64)
		x = math.floor(platno.coords(bomba)[1] / 64)
	else:
		print('non existing bomb')

	if expPlacementJudge(x, y, 'yes'):  # stred
		createExp(y, x, Policko.expStred, 'up')

	if expPlacementJudge(x + 1, y, 'no'):  #                  dole, prve
		createExp(y, x + 1, Policko.expDoleKoniec, 'down')

	if obstaclesMatrix[x][y].bombRange >= 1\
			and expPlacementJudge(x + 1, y, 'no'):
		if expPlacementJudge(x + 2, y, 'no'):
				createExp(y, x + 2, Policko.expDoleKoniec, 'down')  #  dole, druhe
				obstaclesMatrix[x + 1][y].expCislo = Policko.expDoleStred

	if obstaclesMatrix[x][y].bombRange >= 2\
			and expPlacementJudge(x + 1, y, 'no')\
			and expPlacementJudge(x + 2, y, 'no'):
		if expPlacementJudge(x + 3, y, 'no'):
					createExp(y, x + 3, Policko.expDoleKoniec, 'down')  # dole, tretie
					obstaclesMatrix[x + 2][y].expCislo = Policko.expDoleStred

	if obstaclesMatrix[x][y].bombRange >= 3\
			and expPlacementJudge(x + 3, y, 'no')\
			and expPlacementJudge(x + 2, y, 'no')\
			and expPlacementJudge(x + 1, y, 'no'):
		if expPlacementJudge(x + 4, y, 'no'):
			createExp(y, x + 4, Policko.expDoleKoniec, 'down')  # dole, stvrte
			obstaclesMatrix[x + 3][y].expCislo = Policko.expDoleStred

	if expPlacementJudge(x - 1, y, 'no'):  #                 hore, prve
		createExp(y, x - 1, Policko.expHoreKoniec, 'up')

	if (obstaclesMatrix[x][y].bombRange >= 1) \
			and (expPlacementJudge(x - 1, y, 'no')):
		if expPlacementJudge(x - 2, y, 'no'):  #             hore, druhe
			createExp(y, x - 2, Policko.expHoreKoniec, 'up')
			obstaclesMatrix[x - 1][y].expCislo = Policko.expHoreStred

	if (obstaclesMatrix[x][y].bombRange >= 2) \
			and (expPlacementJudge(x - 2, y, 'no'))\
			and (expPlacementJudge(x - 1, y, 'no')):
		if expPlacementJudge(x - 3, y, 'no'):#               hore, tretie
			createExp(y, x - 3, Policko.expHoreKoniec, 'up')
			obstaclesMatrix[x - 2][y].expCislo = Policko.expHoreStred

	if (obstaclesMatrix[x][y].bombRange >= 3) \
			and (expPlacementJudge(x - 3, y, 'no'))\
			and (expPlacementJudge(x - 2, y, 'no'))\
			and (expPlacementJudge(x - 1, y, 'no')):
		if expPlacementJudge(x - 4, y, 'no'):#               hore, stvrte
			createExp(y, x - 4, Policko.expHoreKoniec, 'up')
			obstaclesMatrix[x - 3][y].expCislo = Policko.expHoreStred

	if expPlacementJudge(x, y + 1, 'no'):  #                 vpravo, prve
		createExp(y + 1, x, Policko.expVpravoKoniec, 'right')

	if (obstaclesMatrix[x][y].bombRange >= 1) \
			and (expPlacementJudge(x, y + 1, 'no')):
		if expPlacementJudge(x, y + 2, 'no'):  #             vpravo, druhe
			createExp(y + 2, x, Policko.expVpravoKoniec, 'right')
			obstaclesMatrix[x][y + 1].expCislo = Policko.expVpravoStred

	if (obstaclesMatrix[x][y].bombRange >= 2) \
			and (expPlacementJudge(x, y + 2, 'no'))\
			and (expPlacementJudge(x, y + 1, 'no')):
		if expPlacementJudge(x, y + 3, 'no'):  #             vpravo, tretie
			createExp(y + 3, x, Policko.expVpravoKoniec, 'right')
			obstaclesMatrix[x][y + 2].expCislo = Policko.expVpravoStred

	if (obstaclesMatrix[x][y].bombRange >= 3) \
			and (expPlacementJudge(x, y + 3, 'no'))\
			and (expPlacementJudge(x, y + 2, 'no'))\
			and (expPlacementJudge(x, y + 1, 'no')):
		if expPlacementJudge(x, y + 4, 'no'):  #             vpravo, stvrte
			createExp(y + 4, x, Policko.expVpravoKoniec, 'right')
			obstaclesMatrix[x][y + 3].expCislo = Policko.expVpravoStred

	if expPlacementJudge(x, y - 1, 'no'):  #                 vlavo, prve
		createExp(y - 1, x, Policko.expVlavoKoniec, 'left')

	if (obstaclesMatrix[x][y].bombRange >= 1)\
			and (expPlacementJudge(x, y - 1, 'no')):
		if expPlacementJudge(x, y - 2, 'no'):
			createExp(y - 2, x, Policko.expVlavoKoniec, 'left')  #      vlavo, druhe
			obstaclesMatrix[x][y - 1].expCislo = Policko.expVlavoStred

	if (obstaclesMatrix[x][y].bombRange >= 2)\
			and (expPlacementJudge(x, y - 2, 'no'))\
			and (expPlacementJudge(x, y - 1, 'no')):
		if expPlacementJudge(x, y - 3, 'no'):
			createExp(y - 3, x, Policko.expVlavoKoniec, 'left')  #         vlavo, tretie
			obstaclesMatrix[x][y - 2].expCislo = Policko.expVlavoStred

	if (obstaclesMatrix[x][y].bombRange >= 3)\
			and (expPlacementJudge(x, y - 3, 'no'))\
			and (expPlacementJudge(x, y - 2, 'no'))\
			and (expPlacementJudge(x, y - 1, 'no')):
		if expPlacementJudge(x, y - 4, 'no'):
			createExp(y - 4, x, Policko.expVlavoKoniec, 'left')  #         vlavo, stvrte
			obstaclesMatrix[x][y - 3].expCislo = Policko.expVlavoStred


def explosionFull_only_or_also_Piercing(bomba):
	global obstaclesMatrix
	x = 0
	y = 0
	if len(platno.coords(bomba)) > 0:
		y = math.floor(platno.coords(bomba)[0] / 64)
		x = math.floor(platno.coords(bomba)[1] / 64)
	else:
		print('non existing bomb')

	if expPlacementJudge(x, y, 'yes'):  # stred
		createExp(y, x, Policko.expStred, 'up')

	# zbytocne 2x skoro to iste, da sa to dat aj do jedneho...
	if obstaclesMatrix[x][y].piercingBomb == 'yes':
		k = 1
		while True:  # dole
			if expPlacementJudge(x + k, y, 'no'):
				createExp(y, x + k, Policko.expDoleKoniec, 'down')
				if k > 1:
					obstaclesMatrix[x + k - 1][y].expCislo = Policko.expDoleStred
				k += 1
			else:
				break
		k = 1
		while True:  # hore
			if expPlacementJudge(x - k, y, 'no'):
				createExp(y, x - k, Policko.expHoreKoniec, 'up')
				if k > 1:
					obstaclesMatrix[x - k + 1][y].expCislo = Policko.expHoreStred
				k += 1
			else:
				break
		k = 1
		while True:  # vpravo
			if expPlacementJudge(x, y + k, 'no'):
				createExp(y + k, x, Policko.expVpravoKoniec, 'right')
				if k > 1:
					obstaclesMatrix[x][y + k - 1].expCislo = Policko.expVpravoStred
				k += 1
			else:
				break
		k = 1
		while True:  # vlavo
			if expPlacementJudge(x, y - k, 'no'):
				createExp(y - k, x, Policko.expVlavoKoniec, 'left')
				if k > 1:
					obstaclesMatrix[x][y - k + 1].expCislo = Policko.expVlavoStred
				k += 1
			else:
				break
	if obstaclesMatrix[x][y].piercingBomb == 'no':
		k = 1
		crateBraker = 'ok'
		while True:  # dole
			if expPlacementJudge(x + k, y, 'no'):
				if obstaclesMatrix[x + k][y].cislo == 0:
					crateBraker = 'non ok'
				createExp(y, x + k, Policko.expDoleKoniec, 'down')
				if k > 1:
					obstaclesMatrix[x + k - 1][y].expCislo = Policko.expDoleStred
				k += 1
				if crateBraker != 'ok':
					break
			else:
				break
		k = 1
		crateBraker = 'ok'
		while True:  # hore
			if expPlacementJudge(x - k, y, 'no'):
				if obstaclesMatrix[x - k][y].cislo == 0:
					crateBraker = 'non ok'
				createExp(y, x - k, Policko.expHoreKoniec, 'up')
				if k > 1:
					obstaclesMatrix[x - k + 1][y].expCislo = Policko.expHoreStred
				k += 1
				if crateBraker != 'ok':
					break
			else:
				break
		k = 1
		crateBraker = 'ok'
		while True:  # vpravo
			if expPlacementJudge(x, y + k, 'no'):
				if obstaclesMatrix[x][y + k].cislo == 0:
					crateBraker = 'non ok'
				createExp(y + k, x, Policko.expVpravoKoniec, 'right')
				if k > 1:
					obstaclesMatrix[x][y + k - 1].expCislo = Policko.expVpravoStred
				k += 1
				if crateBraker != 'ok':
					break
			else:
				break
		k = 1
		crateBraker = 'ok'
		while True:  # vlavo
			if expPlacementJudge(x, y - k, 'no'):
				if obstaclesMatrix[x][y - k].cislo == 0:
					crateBraker = 'non ok'
				createExp(y - k, x, Policko.expVlavoKoniec, 'left')
				if k > 1:
					obstaclesMatrix[x][y - k + 1].expCislo = Policko.expVlavoStred
				k += 1
				if crateBraker != 'ok':
					break
			else:
				break


def animExplosions(x, y):  # animuje vybuchy
	if obstaclesMatrix[x][y].expCislo == Policko.expStred:
		if obstaclesMatrix[x][y].frame <= 6:
			platno.itemconfig(obstaclesMatrix[x][y].obj, image=explosionSpritesUp[(0 + obstaclesMatrix[x][y].frame)])

			obstaclesMatrix[x][y].frame += 1
		else:
			platno.delete(obstaclesMatrix[x][y].obj)
			obstaclesMatrix[x][y].cislo = Policko.volne
			obstaclesMatrix[x][y].expCislo = 0
			obstaclesMatrix[x][y].frame = 0
			obstaclesMatrix[x][y].tileName = ''

	elif (obstaclesMatrix[x][y].expCislo == Policko.expHoreStred) or (obstaclesMatrix[x][y].expCislo == Policko.expDoleStred) or \
			(obstaclesMatrix[x][y].expCislo == Policko.expVlavoStred) or (obstaclesMatrix[x][y].expCislo == Policko.expVpravoStred):
		if obstaclesMatrix[x][y].frame <= 6:
			if obstaclesMatrix[x][y].rotation == 'up':
				platno.itemconfig(obstaclesMatrix[x][y].obj, image=explosionSpritesUp[(7 + obstaclesMatrix[x][y].frame)])
			elif obstaclesMatrix[x][y].rotation == 'down':
				platno.itemconfig(obstaclesMatrix[x][y].obj, image=explosionSpritesDown[(7 + obstaclesMatrix[x][y].frame)])
			elif obstaclesMatrix[x][y].rotation == 'left':
				platno.itemconfig(obstaclesMatrix[x][y].obj, image=explosionSpritesLeft[(7 + obstaclesMatrix[x][y].frame)])
			elif obstaclesMatrix[x][y].rotation == 'right':
				platno.itemconfig(obstaclesMatrix[x][y].obj, image=explosionSpritesRight[(7 + obstaclesMatrix[x][y].frame)])

			obstaclesMatrix[x][y].frame += 1
		else:
			platno.delete(obstaclesMatrix[x][y].obj)
			obstaclesMatrix[x][y].cislo = Policko.volne
			obstaclesMatrix[x][y].expCislo = 0
			obstaclesMatrix[x][y].frame = 0
			obstaclesMatrix[x][y].tileName = ''

	elif (obstaclesMatrix[x][y].expCislo == Policko.expHoreKoniec) or (obstaclesMatrix[x][y].expCislo == Policko.expVlavoKoniec) or \
			(obstaclesMatrix[x][y].expCislo == Policko.expVpravoKoniec) or (obstaclesMatrix[x][y].expCislo == Policko.expDoleKoniec):

		if obstaclesMatrix[x][y].frame <= 6:
			if obstaclesMatrix[x][y].rotation == 'up':
				platno.itemconfig(obstaclesMatrix[x][y].obj, image=explosionSpritesUp[(14 + obstaclesMatrix[x][y].frame)])
			elif obstaclesMatrix[x][y].rotation == 'down':
				platno.itemconfig(obstaclesMatrix[x][y].obj, image=explosionSpritesDown[(14 + obstaclesMatrix[x][y].frame)])
			elif obstaclesMatrix[x][y].rotation == 'left':
				platno.itemconfig(obstaclesMatrix[x][y].obj, image=explosionSpritesLeft[(14 + obstaclesMatrix[x][y].frame)])
			elif obstaclesMatrix[x][y].rotation == 'right':
				platno.itemconfig(obstaclesMatrix[x][y].obj, image=explosionSpritesRight[(14 + obstaclesMatrix[x][y].frame)])

			obstaclesMatrix[x][y].frame += 1
		else:
			platno.delete(obstaclesMatrix[x][y].obj)
			obstaclesMatrix[x][y].cislo = Policko.volne
			obstaclesMatrix[x][y].expCislo = 0
			obstaclesMatrix[x][y].frame = 0
			obstaclesMatrix[x][y].tileName = ''

	platno.update()


def moveRight():
	x = math.floor((platno.coords(player)[0] + 24) / 64)
	y = platno.coords(player)[1]

	y1 = math.floor((y + 28) / 64)  # krajny pravy horny a dolny bod(nie celeho ale tam kde chodi)
	y2 = math.floor((y + 5) / 64)

	if (obstaclesMatrix[y1][x].cislo - 1 <= 0) or (obstaclesMatrix[y2][x].cislo - 1 <= 0) or \
			(obstaclesMatrix[y2][x].walkable == 'no') or (obstaclesMatrix[y1][x].walkable == 'no'):
		pass
	else:
		platno.coords(player, (platno.coords(player)[0]) + 3, platno.coords(player)[1])
		platno.update()


def moveLeft():
	x = math.floor((platno.coords(player)[0] - 24) / 64)
	y = platno.coords(player)[1]

	y1 = math.floor((y + 28) / 64)
	y2 = math.floor((y + 5) / 64)
	if (obstaclesMatrix[y1][x].cislo - 1 <= 0) or (obstaclesMatrix[y2][x].cislo - 1 <= 0) or \
			(obstaclesMatrix[y1][x].walkable == 'no') or (obstaclesMatrix[y2][x].walkable == 'no'):
		pass
	else:
		platno.coords(player, (platno.coords(player)[0]) - 3, platno.coords(player)[1])
		platno.update()


def moveDown():
	x = platno.coords(player)[0]
	y = math.floor((platno.coords(player)[1] + 33) / 64)

	x1 = math.floor((x + 20) / 64)
	x2 = math.floor((x - 20) / 64)

	if (obstaclesMatrix[y][x1].cislo - 1 <= 0) or (obstaclesMatrix[y][x2].cislo - 1 <= 0) or \
			(obstaclesMatrix[y][x1].walkable == 'no') or (obstaclesMatrix[y][x2].walkable == 'no'):
		pass
	else:
		platno.coords(player, (platno.coords(player)[0]), platno.coords(player)[1] + 3)
		platno.update()


def moveUp():
	x = platno.coords(player)[0]
	y = math.floor((platno.coords(player)[1] - 5) / 64)
	x1 = math.floor((x + 20) / 64)
	x2 = math.floor((x - 20) / 64)
	if (obstaclesMatrix[y][x1].cislo - 1 <= 0) or (obstaclesMatrix[y][x2].cislo - 1 <= 0) or \
			(obstaclesMatrix[y][x1].walkable == 'no') or (obstaclesMatrix[y][x2].walkable == 'no'):
		pass
	else:
		platno.coords(player, (platno.coords(player)[0]), platno.coords(player)[1] - 3)
		platno.update()


def powerup(name, obj):
	platno.delete(obj)

	if name == 'amountUpImg':
		if PlayerPowerups.bombAmount < 5:
			PlayerPowerups.bombAmount += 1
	if name == 'amountDownImg':
		if PlayerPowerups.bombAmount >= 2:
			PlayerPowerups.bombAmount += -1
	if name == 'amountFullImg':
		PlayerPowerups.bombAmount = 5

	if name == 'speedUpImg':
		if PlayerPowerups.playerSpeed < 5:
			PlayerPowerups.playerSpeed += 1
	if name == 'speedDownImg':
		if PlayerPowerups.playerSpeed > 0:
			PlayerPowerups.playerSpeed += -1

	if name == 'rangeUpImg':
		if PlayerPowerups.bombRange < 4:
			PlayerPowerups.bombRange += 1
	if name == 'rangeDownImg':
		if PlayerPowerups.bombRange > 1:
			if PlayerPowerups.bombRangeFull == 'yes':
				PlayerPowerups.bombRangeFull = 'no'
			else:
				PlayerPowerups.bombRange += -1

	if name == 'rangeFullImg':
		PlayerPowerups.bombRangeFull = 'yes'

	if name == 'vestImg':
		PlayerPowerups.vest = 'yes'
		PlayerPowerups.vestStartTime = time.time()

	if name == 'piercingImg':
		PlayerPowerups.piercing = 'yes'
	update_powerup_board(PlayerPowerups)


def ai_place_bomb(stats, aiObj):
	if stats.placeBomb == True:
		stats.placeBomb = False
		aiX = stats.coords[1]
		aiY = stats.coords[0]
		bomba = platno.create_image(aiX * 64 + 32, aiY * 64 + 32, image=bombSprites[0])
		obstaclesMatrix[aiY][aiX].obj = bomba
		obstaclesMatrix[aiY][aiX].cislo = Policko.bomba
		obstaclesMatrix[aiY][aiX].bombRange = stats.bombRange
		obstaclesMatrix[aiY][aiX].bombRangeFull = stats.bombRangeFull
		obstaclesMatrix[aiY][aiX].bombParent = stats.name
		platno.tag_raise(aiObj)
		stats.bombPlaced += 1
		bombTimerBomb.append(bomba)
		bombTimerTime.append(time.time())

		if stats.piercing == 'yes':
			obstaclesMatrix[aiY][aiX].piercingBomb = 'yes'

		unwalkableBomb.append(aiX)
		unwalkableBomb.append(aiY)

		if sound_settings:
			mixer.Sound.play(bomb_place_sound)


def ai_move(aiObj, stats, sprites):
	if stats.moving == False:
		stats.startX = platno.coords(aiObj)[0]
		stats.startY = platno.coords(aiObj)[1]
		stats.moving = True
	elif stats.moving == True:
		if (abs(platno.coords(aiObj)[0] - stats.startX) >= 64) or (abs(platno.coords(aiObj)[1] - stats.startY) >= 64):  # ak uz presiel 1 block
			stats.moving = False
			platno.coords(aiObj, math.floor(platno.coords(aiObj)[0] / 64) * 64 + 32, math.floor(platno.coords(aiObj)[1] / 64) * 64 + 16 )
			  # ^snap to grid, lebo nechodi pekne po stvorcekoch

			stats.path = 'none'

		else:
			if stats.path == 'up':  # sem pridat aj animacie
				platno.coords(aiObj, platno.coords(aiObj)[0], platno.coords(aiObj)[1] - 3)
				ai_anim(aiObj, stats, sprites)
			elif stats.path == 'down':
				platno.coords(aiObj, platno.coords(aiObj)[0], platno.coords(aiObj)[1] + 3)
				ai_anim(aiObj, stats, sprites)
			elif stats.path == 'right':
				platno.coords(aiObj, platno.coords(aiObj)[0] + 3, platno.coords(aiObj)[1])
				ai_anim(aiObj, stats, sprites)
			elif stats.path == 'left':
				platno.coords(aiObj, platno.coords(aiObj)[0] - 3, platno.coords(aiObj)[1])
				ai_anim(aiObj, stats, sprites)
			platno.update()


def ai_anim(aiObj, stats, sprites):
	if stats.path == 'up':
		if stats.speedRegulator == 10:
			if stats.animCounter >= 4:
				stats.animCounter = 0
			platno.itemconfig(aiObj, image=sprites[stats.animCounter])
			stats.animCounter += 1
			stats.speedRegulator = 0
			platno.update()

	if stats.path == 'down':
		if stats.speedRegulator == 10:
			if (stats.animCounter < 8) or (stats.animCounter > 11):
				stats.animCounter = 8
			platno.itemconfig(aiObj, image=sprites[stats.animCounter])
			stats.animCounter += 1
			stats.speedRegulator = 0
			platno.update()

	if stats.path == 'right':
		if stats.speedRegulator == 10:
			if (stats.animCounter < 4) or (stats.animCounter > 7):
				stats.animCounter = 4
			platno.itemconfig(aiObj, image=sprites[stats.animCounter])
			stats.animCounter += 1
			stats.speedRegulator = 0
			platno.update()

	if stats.path == 'left':
		if stats.speedRegulator == 10:
			if (stats.animCounter < 12) or (stats.animCounter > 15):
				stats.animCounter = 12
			platno.itemconfig(aiObj, image=sprites[stats.animCounter])
			stats.animCounter += 1
			stats.speedRegulator = 0
			platno.update()

	stats.speedRegulator += 1


def ai_powerup(aiObj, stats, powerupName, powerupObjj):
	platno.delete(powerupObjj)
	if stats.name == 'ai1':
		ai_stats = ai1_stats
	elif stats.name == 'ai2':
		ai_stats = ai2_stats
	elif stats.name == 'ai3':
		ai_stats = ai3_stats

	ai_stats.current_target_powerupXY = [None]

	if powerupName == 'amountUpImg':
		if ai_stats.bombAmount < 5:
			ai_stats.bombAmount += 1
	if powerupName == 'amountDownImg':
		if ai_stats.bombAmount >= 2:
			ai_stats.bombAmount += -1
	if powerupName == 'amountFullImg':
		ai_stats.bombAmount = 5

	if powerupName == 'speedUpImg':
		if ai_stats.playerSpeed < 5:
			ai_stats.playerSpeed += 1
	if powerupName == 'speedDownImg':
		if ai_stats.playerSpeed > 0:
			ai_stats.playerSpeed += -1

	if powerupName == 'rangeUpImg':
		if ai_stats.bombRange < 4:
			ai_stats.bombRange += 1
	if powerupName == 'rangeDownImg':
		if ai_stats.bombRange > 1:
			if ai_stats.bombRangeFull == 'yes':
				ai_stats.bombRangeFull = 'no'
			else:
				ai_stats.bombRange += -1

	if powerupName == 'rangeFullImg':
		ai_stats.bombRangeFull = 'yes'

	if powerupName == 'vestImg':
		#ai_stats.vest = 'yes'  # buguju sa ked maju vestu
		ai_stats.vestStartTime = time.time()

	if powerupName == 'piercingImg':
		ai_stats.piercing = 'yes'

	update_powerup_board(stats)


def cisloDebug(event):
	x = math.floor(event.x / 64)
	y = math.floor(event.y / 64)
	#print(obstaclesMatrix[y][x].cislo, end=' ')
	#print(obstaclesMatrix[y][x].aiSeen)
	print(event.x, event.y)


def update_stats_coords(stats, Obj):
	stats.coords = [math.floor((platno.coords(Obj)[1]) / 64), math.floor((platno.coords(Obj)[0]) / 64)]
	#print(stats.coords)


def update_powerup_board(stats):
	offset = 0
	if stats.name == 'player1':
		offset = 0
	elif stats.name == 'ai1':
		offset = 128
	elif stats.name == 'ai2':
		offset = 128 * 2
	elif stats.name == 'ai3':
		offset = 128 * 3

	for i in stats.board_objects:
		platno.delete(i)

	#bomb amount
	for i in range(stats.bombAmount):
		a = platno.create_image(1086 + i * 15, 68 + offset, image=amountUpImg)
		stats.board_objects.append(a)
	#bomb range
	for i in range(stats.bombRange + 1):
		a = platno.create_image(1086 + i * 15, 100 + offset, image=rangeUpImg)
		stats.board_objects.append(a)
	#speed
	for i in range(stats.playerSpeed):
		a = platno.create_image(1207, 31 + offset + i * 15, image=speedUpImg)
		stats.board_objects.append(a)
	# vest
	if stats.vest == 'yes':
		a = platno.create_image(1170, 31 + offset, image=vestImg)
		stats.board_objects.append(a)
	#piercing
	if stats.piercing == 'yes':
		a = platno.create_image(1170, 65 + offset, image=piercingImg)
		stats.board_objects.append(a)
	#full range
	if stats.bombRangeFull == 'yes':
		a = platno.create_image(1170, 100 + offset, image=rangeFullImg)
		stats.board_objects.append(a)


def died(name):
	if name == 'ai1':
		mugShiet1 = platno.create_image(64 * 14 + 132, 128 * 2 - 47, image=dead)
		platno.update()
	if name == 'ai2':
		mugShiet2 = platno.create_image(64 * 14 + 132, 128 * 3 - 47, image=dead)
		platno.update()
	if name == 'ai3':
		mugShiet3 = platno.create_image(64 * 14 + 132, 128 * 4 - 47, image=dead)
		platno.update()





obstaclesMatrix = [  # 1 = obstacle, 0 = crate, 2 = free, 3 = bomba
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # walls
	[1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],  # free
	[1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1],  # kazda druha pevna
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # free
	[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # free
	[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # free
	[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # free
	[1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1],
	[1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],  # free
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]  # walls
]  # vsetko podstatne
reeeeeeferenceMatrix = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # walls
	[1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],  # free
	[1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1],  # kazda druha pevna
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # free
	[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # free
	[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # fre
	[1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],  # free
	[1, 2, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 2, 1],
	[1, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 2, 1],  # free
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
]  # z toho sa robi obstacles

for i in range(13):  # kreslenie podlahy, krabic, power-up-ov, stavanie hracej plochy vseobecne
	premenna = 0
	for e in range(15):

		obstaclesMatrix[i][e] = createClass()
		obstaclesMatrix[i][e].cislo = reeeeeeferenceMatrix[i][e]
		if int(reeeeeeferenceMatrix[i][e]) % 2 == 0:
			platno.create_image(premenna * 64 + 32, i * 64 + 32, image=background)

		if int(reeeeeeferenceMatrix[i][e]) == 1:
			platno.create_image(premenna * 64 + 32, i * 64 + 32, image=wallImg)

		if int(reeeeeeferenceMatrix[i][e]) == 0:
			if random.randint(1, 100) < 30:
				chosen = random.choices(
				[['amountUpImg', amountUpImg], ['amountDownImg', amountDownImg], ['amountFullImg', amountFullImg],
				 ['rangeUpImg', rangeUpImg], ['rangeDownImg', rangeDownImg], ['rangeFullImg', rangeFullImg], ['speedUpImg', speedUpImg],
				 ['speedDownImg', speedDownImg], ['piercingImg', piercingImg], ['vestImg', vestImg]], weights=(15, 4, 3, 14, 4, 2, 14, 4, 3, 3), k=1)

				obstaclesMatrix[i][e].powerup = chosen[0][0]
				obstaclesMatrix[i][e].powerupObj = chosen[0][1]

			if obstaclesMatrix[i][e].powerup != '':
				powerupLocal = platno.create_image(premenna * 64 + 32, i * 64 + 32, image=obstaclesMatrix[i][e].powerupObj)
				obstaclesMatrix[i][e].powerupObj = powerupLocal

			crateReference = platno.create_image(premenna * 64 + 32, i * 64 + 32, image=crateImg)
			obstaclesMatrix[i][e].obj = crateReference
			obstaclesMatrix[i][e].cislo = Policko.krabica
			obstaclesMatrix[i][e].tileName = 'crate'

		platno.update()
		premenna += 1

  # hraci a ich staty, zoznam init
player = platno.create_image(150, 80, image=playerSprites[0])
ai1 = platno.create_image(14 * 64 - 32, 80, image=ai1Sprites[0])
ai2 = platno.create_image(14 * 64 - 32, 80 + 64 * 10, image=ai2Sprites[0])
ai3 = platno.create_image(2 * 64 - 32, 80 + 64 * 10, image=ai3Sprites[0])

playersZoznam = []
playersZoznam.append([player, PlayerPowerups])
playersZoznam.append([ai1, ai1_stats])
playersZoznam.append([ai2, ai2_stats])
playersZoznam.append([ai3, ai3_stats])

update_stats_coords(ai1_stats, ai1)
update_stats_coords(ai2_stats, ai2)
update_stats_coords(ai3_stats, ai3)
  # koniec init hracov


  # -------------tabulka a ten zbytok init
scoreImg = Image.open('other_textures/banner.png')
scoreImg = ImageTk.PhotoImage(scoreImg)
zelezo = Image.open('other_textures/metal.jpg')
zelezo = ImageTk.PhotoImage(zelezo)
zelezoZ = []
for i in range(3):
	zeeelezo = platno.create_image(64 * 15 + 138, (297 / 2) + 297 * i, image=zelezo)  # to na com su pomocky
	zelezoZ.append(zeeelezo)
divider = Image.open('other_textures/divider.png')
divider = ImageTk.PhotoImage(divider)
divajder = platno.create_image(64 * 15 + 10, 64 * 13 / 2, image=divider)  # pas medzi hracou plochou a statmi
controls = Image.open('other_textures/controls.png')
controls = ImageTk.PhotoImage(controls)
controlsss = platno.create_image(64 * 15 + 145, 650, image=controls)


for i in range(1, 5):
	platno.create_image(64 * 15 + 138, 128 * i - 62, image=scoreImg)
	if i == 1:  # ak si zmenil meno, tu treba pridat moznost po menu zeby si napisal meno a dal farbu
		platno.create_text(64 * 14 + 145, 128 * i - 103, text='Player', font='ArcadeClassic', fill='white')
		fotka1 = Image.open(f'bomberman_sprites/{player1color}/tile010.png')
		fotka1 = fotka1.crop([0, 0, 70, 84])
		fotka1 = ImageTk.PhotoImage(fotka1)
		mugshot1 = platno.create_image(64 * 14 + 132, 128 * i - 47, image=fotka1)
	elif i == 2:  # ak si zmenil meno, tu treba pridat moznost po menu zeby si napisal meno a dal farbu
		platno.create_text(64 * 14 + 127, 128 * i - 103, text='AI 1', font='ArcadeClassic', fill='white')
		fotka2 = Image.open(f'bomberman_sprites/{player2color}/tile010.png')
		fotka2 = fotka2.crop([0, 0, 70, 84])
		fotka2 = ImageTk.PhotoImage(fotka2)
		mugshot2 = platno.create_image(64 * 14 + 132, 128 * i - 47, image=fotka2)
	elif i == 3:  # ak si zmenil meno, tu treba pridat moznost po menu zeby si napisal meno a dal farbu
		platno.create_text(64 * 14 + 127, 128 * i - 103, text='AI 2', font='ArcadeClassic', fill='white')
		fotka3 = Image.open(f'bomberman_sprites/{player3color}/tile010.png')
		fotka3 = fotka3.crop([0, 0, 70, 84])
		fotka3 = ImageTk.PhotoImage(fotka3)
		mugshot3 = platno.create_image(64 * 14 + 132, 128 * i - 47, image=fotka3)
	elif i == 4:  # ak si zmenil meno, tu treba pridat moznost po menu zeby si napisal meno a dal farbu
		platno.create_text(64 * 14 + 127, 128 * i - 103, text='AI 3', font='ArcadeClassic', fill='white')
		fotka4 = Image.open(f'bomberman_sprites/{player4color}/tile010.png')
		fotka4 = fotka4.crop([0, 0, 70, 84])
		fotka4 = ImageTk.PhotoImage(fotka4)
		mugshot4 = platno.create_image(64 * 14 + 132, 128 * i - 47, image=fotka4)
  # ------tabulka init koniec

platno.update()
update_powerup_board(PlayerPowerups)
update_powerup_board(ai1_stats)
update_powerup_board(ai2_stats)
update_powerup_board(ai3_stats)

t0 = time.time()  # cas na animaciu hraca
ai1_anim_time = time.time()
ai2_anim_time = time.time()
ai3_anim_time = time.time()

ai1_anim_counter = 0
ai2_anim_counter = 0
ai3_anim_counter = 0

playerRotation = 'up'
oldRotation = 'up'
playerAnimCounter = 0
player_animSpeedRegulator = 0
ai1_animSpeedRegulator = 0
ai2_animSpeedRegulator = 0
ai3_animSpeedRegulator = 0


playerPlacedBombs = 0
bombAnimCounter = 0
bombTimerBomb = []
bombTimerTime = []

tExplosion = time.time()
tBombs = time.time()

explosionImgTracking = []
unwalkableBomb = []

platno.bind_all('<space>', placeBomb)
platno.bind_all('<Button-1>', cisloDebug)


# mainloop

gamestate = 'playing'
strafecounter = 0  # player strafe movement
while gamestate == 'playing':
	if keyboard.is_pressed('a') and keyboard.is_pressed('w'):  # user input, najskor strafing
		playerRotation = 'left'
		if time.time() - t0 > 0.01 - (PlayerPowerups.playerSpeed - 2) * 0.002:  # hore, dolava
			if strafecounter % 2 == 0:
				moveLeft()
				strafecounter += 1
			else:
				moveUp()
				strafecounter += 1
			t0 = time.time()
			playerAnim(playerAnimCounter)
	elif keyboard.is_pressed('a') and keyboard.is_pressed('s'):  # dole, dolava
		playerRotation = 'left'
		if time.time() - t0 > 0.01 - (PlayerPowerups.playerSpeed - 2) * 0.002:
			if strafecounter % 2 == 0:
				moveLeft()
				strafecounter += 1
			else:
				moveDown()
				strafecounter += 1
			t0 = time.time()
			playerAnim(playerAnimCounter)
	elif keyboard.is_pressed('d') and keyboard.is_pressed('s'):  # dole, doprava
		playerRotation = 'right'
		if time.time() - t0 > 0.01 - (PlayerPowerups.playerSpeed - 2) * 0.002:
			if strafecounter % 2 == 0:
				moveRight()
				strafecounter += 1
			else:
				moveDown()
				strafecounter += 1
			t0 = time.time()
			playerAnim(playerAnimCounter)
	elif keyboard.is_pressed('w') and keyboard.is_pressed('d'):  # hore, doprava
		playerRotation = 'right'
		if time.time() - t0 > 0.01 - (PlayerPowerups.playerSpeed - 2) * 0.002:
			if strafecounter % 2 == 0:
				moveRight()
				strafecounter += 1
			else:
				moveUp()
				strafecounter += 1
			t0 = time.time()
			playerAnim(playerAnimCounter)

	elif keyboard.is_pressed('a'):
		oldRotation = playerRotation
		playerRotation = 'left'
		if time.time() - t0 > 0.01 - (PlayerPowerups.playerSpeed - 2) * 0.002:
			if oldRotation != playerRotation:
				player_animSpeedRegulator = 10
			moveLeft()
			t0 = time.time()
			playerAnim(playerAnimCounter)
	elif keyboard.is_pressed('s'):
		oldRotation = playerRotation
		playerRotation = 'down'
		if time.time() - t0 > 0.01 - (PlayerPowerups.playerSpeed - 2) * 0.002:
			if oldRotation != playerRotation:
				player_animSpeedRegulator = 10
			moveDown()
			t0 = time.time()
			playerAnim(playerAnimCounter)
	elif keyboard.is_pressed('d'):
		oldRotation = playerRotation
		playerRotation = 'right'
		if time.time() - t0 > 0.01 - (PlayerPowerups.playerSpeed - 2) * 0.002:
			if oldRotation != playerRotation:
				player_animSpeedRegulator = 10
			moveRight()
			t0 = time.time()
			playerAnim(playerAnimCounter)
	elif keyboard.is_pressed('w'):
		oldRotation = playerRotation
		if time.time() - t0 > 0.01 - (PlayerPowerups.playerSpeed - 2) * 0.002:
			playerRotation = 'up'
			if oldRotation != playerRotation:
				player_animSpeedRegulator = 10
			moveUp()
			t0 = time.time()
			playerAnim(playerAnimCounter)
	if keyboard.is_pressed('Escape'):
		exit()

	if (playerPlacedBombs != 0) or (ai1_stats.bombPlaced != 0) or\
		(ai2_stats.bombPlaced != 0) or (ai3_stats.bombPlaced != 0):
		if time.time() - tBombs > 0.1:  # bomb anim speed regulator
			animBombs()
			tBombs = time.time()

	checkBombs()

	if time.time() - tExplosion > 0.1:
		for i in range(15):
			for e in range(13):
				if int(obstaclesMatrix[e][i].expCislo) - 10 >= 0:  # zmenit na 1 podmienku
					if obstaclesMatrix[e][i].expCislo > 9:
						animExplosions(e, i)
						tExplosion = time.time()

	if len(unwalkableBomb) != 0:
		if (unwalkableBomb[0] != (math.floor((platno.coords(player)[0]) / 64))) \
				or (unwalkableBomb[1] != (math.floor((platno.coords(player)[1]) / 64))):
			obstaclesMatrix[int(unwalkableBomb[1])][int(unwalkableBomb[0])].walkable = 'no'
			unwalkableBomb = []

  # ---------skapacie mechaniky
	if obstaclesMatrix[math.floor((platno.coords(player)[1]) / 64)][math.floor((platno.coords(player)[0]) / 64)].tileName == 'explosion':
		if PlayerPowerups.vest == 'no':
			gamestate = 'lost'
	if ai1_stats.dead != True:
		if obstaclesMatrix[ai1_stats.coords[0]][ai1_stats.coords[1]].tileName == 'explosion':
			if ai1_stats.vest == 'no':  # skapal
				print('AI1 SKAPAL')
				platno.delete(ai1)
				ai1_stats.dead = True
				died('ai1')
	if ai2_stats.dead != True:
		if obstaclesMatrix[ai2_stats.coords[0]][ai2_stats.coords[1]].tileName == 'explosion':
			if ai2_stats.vest == 'no':  # skapal
				print('AI2 SKAPAL')
				platno.delete(ai2)
				ai2_stats.dead = True
				died('ai2')
	if ai3_stats.dead != True:
		if obstaclesMatrix[ai3_stats.coords[0]][ai3_stats.coords[1]].tileName == 'explosion':
			if ai3_stats.vest == 'no':  # skapal
				print('AI3 SKAPAL')
				platno.delete(ai3)
				ai3_stats.dead = True
				died('ai3')
  # --------koniec skapacich mechanik

	if obstaclesMatrix[math.floor((platno.coords(player)[1]) / 64)][math.floor((platno.coords(player)[0]) / 64)].powerup != '':  # ak je tam nejaky powerup, ...
		powerup(obstaclesMatrix[math.floor((platno.coords(player)[1]) / 64)][math.floor((platno.coords(player)[0]) / 64)].powerup,
			obstaclesMatrix[math.floor((platno.coords(player)[1]) / 64)][math.floor((platno.coords(player)[0]) / 64)].powerupObj)
		ai1_stats.current_target_powerup_list = []
		ai1_stats.current_listXY = []
		ai2_stats.current_target_powerup_list = []
		ai2_stats.current_listXY = []
		ai3_stats.current_target_powerup_list = []
		ai3_stats.current_listXY = []

		obstaclesMatrix[math.floor((platno.coords(player)[1]) / 64)][
			math.floor((platno.coords(player)[0]) / 64)].powerup = ''

	if PlayerPowerups.vest == 'yes':
		if time.time() - PlayerPowerups.vestStartTime > 5:
			PlayerPowerups.vest = 'no'
			PlayerPowerups.vestStartTime = 0

	if ai1_stats.dead != True:
		if obstaclesMatrix[ai1_stats.coords[0]][ai1_stats.coords[1]].powerup != '':  # ak je tam nejaky powerup, ...
			ai_powerup(ai1, ai1_stats, obstaclesMatrix[math.floor((platno.coords(ai1)[1]) / 64)][
				                        math.floor((platno.coords(ai1)[0]) / 64)].powerup,
			                           obstaclesMatrix[math.floor((platno.coords(ai1)[1]) / 64)][
				                        math.floor((platno.coords(ai1)[0]) / 64)].powerupObj)
			obstaclesMatrix[math.floor((platno.coords(ai1)[1]) / 64)][
				math.floor((platno.coords(ai1)[0]) / 64)].powerup = ''
			print('-ai1 powerup pickup-')
	if ai2_stats.dead != True:
		if obstaclesMatrix[ai2_stats.coords[0]][ai2_stats.coords[1]].powerup != '':  # ak je tam nejaky powerup, ...
			ai_powerup(ai2, ai2_stats, obstaclesMatrix[math.floor((platno.coords(ai2)[1]) / 64)][
				                        math.floor((platno.coords(ai2)[0]) / 64)].powerup,
			                           obstaclesMatrix[math.floor((platno.coords(ai2)[1]) / 64)][
				                        math.floor((platno.coords(ai2)[0]) / 64)].powerupObj)
			obstaclesMatrix[math.floor((platno.coords(ai2)[1]) / 64)][
				math.floor((platno.coords(ai2)[0]) / 64)].powerup = ''
			print('-ai2 powerup pickup-')
	if ai3_stats.dead != True:
		if obstaclesMatrix[ai3_stats.coords[0]][ai3_stats.coords[1]].powerup != '':  # ak je tam nejaky powerup, ...
			ai_powerup(ai3, ai3_stats, obstaclesMatrix[math.floor((platno.coords(ai3)[1]) / 64)][
				                        math.floor((platno.coords(ai3)[0]) / 64)].powerup,
			                           obstaclesMatrix[math.floor((platno.coords(ai3)[1]) / 64)][
				                        math.floor((platno.coords(ai3)[0]) / 64)].powerupObj)
			obstaclesMatrix[math.floor((platno.coords(ai3)[1]) / 64)][
				math.floor((platno.coords(ai3)[0]) / 64)].powerup = ''
			print('-ai3 powerup pickup-')

	if ai1_stats.dead != True:
		if time.time() - ai1_anim_time > 0.01 - (ai1_stats.playerSpeed - 2) * 0.002:  # ai1 anim + movement
			if (ai1_stats.path != 'none') and (ai3_stats.dead != True):
				ai_move(ai1, ai1_stats, ai1Sprites)
				ai1_anim_time = time.time()
			else:
					update_stats_coords(ai1_stats, ai1)
					update_stats_coords(PlayerPowerups, player)
					aiLogic.decisionMaker(obstaclesMatrix, math.floor((platno.coords(ai1)[1]) / 64)
					                      , math.floor((platno.coords(ai1)[0]) / 64), ai1_stats, playersZoznam)
					ai_place_bomb(ai1_stats, ai1)
	if ai2_stats.dead != True:
		if time.time() - ai2_anim_time > 0.01 - (ai2_stats.playerSpeed - 2) * 0.002:  # ai2 anim + movement
			if (ai2_stats.path != 'none') and (ai3_stats.dead != True):
				ai_move(ai2, ai2_stats, ai2Sprites)
				ai2_anim_time = time.time()
			else:
					update_stats_coords(ai2_stats, ai2)
					update_stats_coords(PlayerPowerups, player)
					aiLogic.decisionMaker(obstaclesMatrix, math.floor((platno.coords(ai2)[1]) / 64)
					                      , math.floor((platno.coords(ai2)[0]) / 64), ai2_stats, playersZoznam)
					ai_place_bomb(ai2_stats, ai2)
	if ai3_stats.dead != True:
		if time.time() - ai3_anim_time > 0.01 - (ai3_stats.playerSpeed - 2) * 0.002:  # ai3 anim + movement
			if (ai3_stats.path != 'none') and (ai3_stats.dead != True):
				ai_move(ai3, ai3_stats, ai3Sprites)
				ai3_anim_time = time.time()
			else:
					update_stats_coords(ai3_stats, ai3)
					update_stats_coords(PlayerPowerups, player)
					aiLogic.decisionMaker(obstaclesMatrix, math.floor((platno.coords(ai3)[1]) / 64)
					                      , math.floor((platno.coords(ai3)[0]) / 64), ai3_stats, playersZoznam)
					ai_place_bomb(ai3_stats, ai3)

	if (ai1_stats.dead == True) and (ai2_stats.dead == True) and (ai3_stats.dead == True):
		gamestate = 'won'
if sound_settings:
	mixer.music.stop()

if gamestate == 'lost':
	if sound_settings:
		mixer.Sound.play(death_sound)
	game_over = Image.open('other_textures/game_over.png')
	game_over = ImageTk.PhotoImage(game_over)
	g_over = platno.create_image((64 * 15 + 276) / 2, 64 * 13 / 2, image=game_over)
	platno.update()

elif gamestate == 'won':
	mixer.Sound.play(victory_sound)
	game_won = Image.open('other_textures/victory_screen.png')
	game_won = ImageTk.PhotoImage(game_won)
	g_won = platno.create_image((64 * 15 + 276) / 2, 64 * 13 / 2, image=game_won)
	platno.update()


time.sleep(0.5)
keyboard.wait('Space')
okno.destroy()