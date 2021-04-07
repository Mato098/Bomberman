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
bombSprites = []
for i in range(8):
	bombImg = Image.open(f'bomb_sprites/tile00{i}.png')
	bombImg = bombImg.resize((48, 48), Image.ANTIALIAS)
	bombImg = ImageTk.PhotoImage(bombImg)
	bombSprites.append(bombImg)

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
speedDownImg = Image.open('other_textures/speed/down.png')
speedDownImg = ImageTk.PhotoImage(speedDownImg)

vestImg = Image.open('other_textures/vest.png')
vestImg = ImageTk.PhotoImage(vestImg)

piercingImg = Image.open('other_textures/pierceBomb.png')
piercingImg = ImageTk.PhotoImage(piercingImg)

dead = Image.open(f'other_textures/dead.png')
dead = dead.resize((130, 130), Image.ANTIALIAS)
dead = ImageTk.PhotoImage(dead)

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


def createTile():
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


def createPlayer(name, color, controls):
	@dataclass
	class player_stats:
		vestStartTime: float = 0
		bombAmount: int = 1
		bombRange: int = 0
		bombPlaced: int = 0
		bombRangeFull: str = 'no'
		playerSpeed: int = 2
		vest: str = 'no'
		piercing: str = 'no'
		coords: List[str] = field(default_factory=list)
		animCounter: int = 0
		animSpeedRegulator: int = 0
		animTime: float = 0
		t0: float = time.time()
		strafeCounter: int = 0
		rotation: str = 'up'
		oldRotation: str = 'up'
		name: str = 'player1'
		job: str = 'none'
		color: str = 'color1'
		dead: bool = False
		controls: List[str] = field(default_factory=list)
		sprites: List[str] = field(default_factory=list)
		obj: List[str] = field(default_factory=list)
		board_objects: List[str] = field(default_factory=list)
	a = player_stats()
	player_stats = a

	player_stats.color = color
	player_stats.name = name
	player_stats.controls = controls
	player_stats.animTime = time.time()
	return player_stats


def createAi(name, color):
	@dataclass
	class ai_stats:
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
		animTime: float = 0
		path: str = 'none'
		lastPath = 'none'  # aby sa animacia zmenila hned co zmeni smer
		bombRangeFull: str = 'no'
		playerSpeed: int = 2
		vest: str = 'no'
		piercing: str = 'no'
		name: str = 'ai4'
		job: str = 'none'
		color: str = 'color1'
		dead: bool = False
		coords: List[str] = field(default_factory=list)
		board_objects: List[str] = field(default_factory=list)
		sprites: List[str] = field(default_factory=list)
		obj: List[str] = field(default_factory=list)

		current_target_powerup_list: List[str] = field(default_factory=list)  # cely zoznam co A* vypluje
		current_listXY: List[str] = field(default_factory=list)  # X, Y suradnice podla kt. sa orientuje v zozname^
	a = ai_stats()
	ai_stats = a

	ai_stats.name = name
	ai_stats.color = color
	ai_stats.animTime = time.time()

	return ai_stats


def playerAnim(playerObj, playerStats):
	if playerStats.rotation == 'up':
		if playerStats.animSpeedRegulator == 10:
			if playerStats.animCounter >= 4:
				playerStats.animCounter = 0
			platno.itemconfig(playerObj, image=playerStats.sprites[playerStats.animCounter])
			playerStats.animCounter = playerStats.animCounter + 1
			platno.update()
			playerStats.animSpeedRegulator = 0
		else:
			playerStats.animSpeedRegulator += 1

	if playerStats.rotation == 'down':
		if playerStats.animSpeedRegulator == 10:
			if (playerStats.animCounter < 8) or (playerStats.animCounter > 11):
				playerStats.animCounter = 8
			platno.itemconfig(playerObj, image=playerStats.sprites[playerStats.animCounter])
			playerStats.animCounter = playerStats.animCounter + 1
			platno.update()
			playerStats.animSpeedRegulator = 0
		else:
			playerStats.animSpeedRegulator += 1
	if playerStats.rotation == 'right':
		if playerStats.animSpeedRegulator == 10:
			if (playerStats.animCounter < 4) or (playerStats.animCounter > 7):
				playerStats.animCounter = 4
			platno.itemconfig(playerObj, image=playerStats.sprites[playerStats.animCounter])
			playerStats.animCounter = playerStats.animCounter + 1
			platno.update()
			playerStats.animSpeedRegulator = 0
		else:
			playerStats.animSpeedRegulator += 1
	if playerStats.rotation == 'left':
		if playerStats.animSpeedRegulator == 10:
			if (playerStats.animCounter < 12) or (playerStats.animCounter > 15):
				playerStats.animCounter = 12
			platno.itemconfig(playerObj, image=playerStats.sprites[playerStats.animCounter])
			playerStats.animCounter = playerStats.animCounter + 1
			platno.update()
			playerStats.animSpeedRegulator = 0
		else:
			playerStats.animSpeedRegulator += 1


def placeBomb(event):  # AI bude mat svoju funkciu na davanie bomb lebo toto je event??
	print('place bomb A')
	print(event.char)
	for stats in allPlayersList:
		print(i.controls[4])
		if event.char == i.controls[4]:
			print('place bomb B')
			if stats.bombPlaced < stats.bombAmount:
				x = math.floor(platno.coords(stats.obj)[0] / 64)
				y = math.floor((platno.coords(stats.obj)[1] + 20) / 64)
				if obstaclesMatrix[y][x].cislo != Policko.bomba:
					if sound_settings:
						mixer.Sound.play(bomb_place_sound)

					bomba = platno.create_image(x * 64 + 32, y * 64 + 32, image=bombSprites[0])
					obstaclesMatrix[y][x].obj = bomba
					obstaclesMatrix[y][x].cislo = Policko.bomba
					obstaclesMatrix[y][x].bombRange = stats.bombRange
					obstaclesMatrix[y][x].bombRangeFull = stats.bombRangeFull
					obstaclesMatrix[y][x].bombParent = stats.name
					platno.tag_raise(stats.obj)
					stats.bombPlaced += 1
					bombTimerBomb.append(bomba)
					bombTimerTime.append(time.time())

					if stats.piercing == 'yes':
						obstaclesMatrix[y][x].piercingBomb = 'yes'

					unwalkableBomb.append(math.floor((platno.coords(stats.obj)[0]) / 64))
					unwalkableBomb.append(math.floor((platno.coords(stats.obj)[1]) / 64))


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
	global bombTimerBomb, bombTimerTime
	cas = time.time()
	for f in range(len(bombTimerTime)):
		if cas - bombTimerTime[f] > 2:
			if bombTimerTime[f] != 0:
				if (obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)]
									[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombRangeFull == 'yes'):  # full ma full classic bez aj s piercingom
					for stats in allPlayersList:
						if stats.name == obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)]\
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent:
							stats.bombPlaced += -1
					explosionFull_only_or_also_Piercing(bombTimerBomb[f])

				elif (obstaclesMatrix[math.floor(platno.coords(bombTimerBomb[f])[1] / 64)]
									[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].piercingBomb == 'yes'):  # piercing classic
					for stats in allPlayersList:
						if stats.name == obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)]\
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent:
							stats.bombPlaced += -1
					explosionPiercing_only(bombTimerBomb[f])

				else:  # classic
					for stats in allPlayersList:
						if stats.name == obstaclesMatrix[math.floor((platno.coords(bombTimerBomb[f])[1]) / 64)]\
							[math.floor(platno.coords(bombTimerBomb[f])[0] / 64)].bombParent:
							stats.bombPlaced += -1
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


def moveRight(playerObj):
	x = math.floor((platno.coords(playerObj)[0] + 24) / 64)
	y = platno.coords(playerObj)[1]

	y1 = math.floor((y + 28) / 64)  # krajny pravy horny a dolny bod(nie celeho ale tam kde chodi)
	y2 = math.floor((y + 5) / 64)

	if (obstaclesMatrix[y1][x].cislo - 1 <= 0) or (obstaclesMatrix[y2][x].cislo - 1 <= 0) or \
			(obstaclesMatrix[y2][x].walkable == 'no') or (obstaclesMatrix[y1][x].walkable == 'no'):
		pass
	else:
		platno.coords(playerObj, (platno.coords(playerObj)[0]) + 3, platno.coords(playerObj)[1])
		platno.update()


def moveLeft(playerObj):
	x = math.floor((platno.coords(playerObj)[0] - 24) / 64)
	y = platno.coords(playerObj)[1]

	y1 = math.floor((y + 28) / 64)
	y2 = math.floor((y + 5) / 64)
	if (obstaclesMatrix[y1][x].cislo - 1 <= 0) or (obstaclesMatrix[y2][x].cislo - 1 <= 0) or \
			(obstaclesMatrix[y1][x].walkable == 'no') or (obstaclesMatrix[y2][x].walkable == 'no'):
		pass
	else:
		platno.coords(playerObj, (platno.coords(playerObj)[0]) - 3, platno.coords(playerObj)[1])
		platno.update()


def moveDown(playerObj):
	x = platno.coords(playerObj)[0]
	y = math.floor((platno.coords(playerObj)[1] + 33) / 64)

	x1 = math.floor((x + 20) / 64)
	x2 = math.floor((x - 20) / 64)

	if (obstaclesMatrix[y][x1].cislo - 1 <= 0) or (obstaclesMatrix[y][x2].cislo - 1 <= 0) or \
			(obstaclesMatrix[y][x1].walkable == 'no') or (obstaclesMatrix[y][x2].walkable == 'no'):
		pass
	else:
		platno.coords(playerObj, (platno.coords(playerObj)[0]), platno.coords(playerObj)[1] + 3)
		platno.update()


def moveUp(playerObj):
	x = platno.coords(playerObj)[0]
	y = math.floor((platno.coords(playerObj)[1] - 5) / 64)
	x1 = math.floor((x + 20) / 64)
	x2 = math.floor((x - 20) / 64)
	if (obstaclesMatrix[y][x1].cislo - 1 <= 0) or (obstaclesMatrix[y][x2].cislo - 1 <= 0) or \
			(obstaclesMatrix[y][x1].walkable == 'no') or (obstaclesMatrix[y][x2].walkable == 'no'):
		pass
	else:
		platno.coords(playerObj, (platno.coords(playerObj)[0]), platno.coords(playerObj)[1] - 3)
		platno.update()


def powerup(powerupName, stats):
	platno.delete(stats.obj)

	if powerupName == 'amountUpImg':
		if stats.bombAmount < 5:
			stats.bombAmount += 1
	if powerupName == 'amountDownImg':
		if stats.bombAmount >= 2:
			stats.bombAmount += -1
	if powerupName == 'amountFullImg':
		stats.bombAmount = 5

	if powerupName == 'speedUpImg':
		if stats.playerSpeed < 5:
			stats.playerSpeed += 1
	if powerupName == 'speedDownImg':
		if stats.playerSpeed > 0:
			stats.playerSpeed += -1

	if powerupName == 'rangeUpImg':
		if stats.bombRange < 4:
			stats.bombRange += 1
	if powerupName == 'rangeDownImg':
		if stats.bombRange > 1:
			if stats.bombRangeFull == 'yes':
				stats.bombRangeFull = 'no'
			else:
				stats.bombRange += -1

	if powerupName == 'rangeFullImg':
		stats.bombRangeFull = 'yes'

	if powerupName == 'vestImg':
		stats.vest = 'yes'
		stats.vestStartTime = time.time()

	if powerupName == 'piercingImg':
		stats.piercing = 'yes'
	update_powerup_board(stats)


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
			platno.coords(aiObj, math.floor(platno.coords(aiObj)[0] / 64) * 64 + 32,
			              math.floor(platno.coords(aiObj)[1] / 64) * 64 + 16)
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


def cisloDebug(event):
	x = math.floor(event.x / 64)
	y = math.floor(event.y / 64)
	#print(obstaclesMatrix[y][x].cislo, end=' ')
	#print(obstaclesMatrix[y][x].aiSeen)
	print(event.x, event.y)


def update_stats_coords(stats, Obj):
	stats.coords = [math.floor((platno.coords(Obj)[1]) / 64), math.floor((platno.coords(Obj)[0]) / 64)]
	#print(stats.coords)

  #TODO updaty lepsie urobit, + tabulku celu
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


def playerInput(playerStats):
	if keyboard.is_pressed(playerStats.controls[1]) and keyboard.is_pressed(playerStats.controls[0]):  # user input, najskor strafing
		playerStats.rotation = 'left'
		if time.time() - playerStats.t0 > 0.01 - (playerStats.playerSpeed - 2) * 0.002:  # hore, dolava
			if playerStats.strafeCounter % 2 == 0:
				moveLeft(playerStats.obj)
				playerStats.strafeCounter += 1
			else:
				moveUp(playerStats.obj)
				playerStats.strafeCounter += 1
			playerStats.t0 = time.time()
			playerAnim(playerStats.obj, playerStats)
	elif keyboard.is_pressed(playerStats.controls[1]) and keyboard.is_pressed(playerStats.controls[2]):  # dole, dolava
		playerStats.rotation = 'left'
		if time.time() - playerStats.t0 > 0.01 - (playerStats.playerSpeed - 2) * 0.002:
			if playerStats.strafeCounter % 2 == 0:
				moveLeft(playerStats.obj)
				playerStats.strafeCounter += 1
			else:
				moveDown(playerStats.obj)
				playerStats.strafeCounter += 1
			playerStats.t0 = time.time()
			playerAnim(playerStats.obj, playerStats)
	elif keyboard.is_pressed(playerStats.controls[3]) and keyboard.is_pressed(playerStats.controls[2]):  # dole, doprava
		playerStats.rotation = 'right'
		if time.time() - playerStats.t0 > 0.01 - (playerStats.playerSpeed - 2) * 0.002:
			if playerStats.strafeCounter % 2 == 0:
				moveRight(playerStats.obj)
				playerStats.strafeCounter += 1
			else:
				moveDown(playerStats.obj)
				playerStats.strafeCounter += 1
			playerStats.t0 = time.time()
			playerAnim(playerStats.obj, playerStats)
	elif keyboard.is_pressed(playerStats.controls[0]) and keyboard.is_pressed(playerStats.controls[3]):  # hore, doprava
		playerStats.rotation = 'right'
		if time.time() - playerStats.t0 > 0.01 - (playerStats.playerSpeed - 2) * 0.002:
			if playerStats.strafeCounter % 2 == 0:
				moveRight(playerStats.obj)
				playerStats.strafeCounter += 1
			else:
				moveUp(playerStats.obj)
				playerStats.strafeCounter += 1
			playerStats.t0 = time.time()
			playerAnim(playerStats.obj, playerStats)

	elif keyboard.is_pressed(playerStats.controls[1]):
		playerStats.oldRotation = playerStats.rotation
		playerStats.rotation = 'left'
		if time.time() - playerStats.t0 > 0.01 - (playerStats.playerSpeed - 2) * 0.002:
			if playerStats.oldRotation != playerStats.rotation:
				playerStats.animSpeedRegulator = 10
			moveLeft(playerStats.obj)
			playerStats.t0 = time.time()
			playerAnim(playerStats.obj, playerStats)
	elif keyboard.is_pressed(playerStats.controls[2]):
		playerStats.oldRotation = playerStats.rotation
		playerStats.rotation = 'down'
		if time.time() - playerStats.t0 > 0.01 - (playerStats.playerSpeed - 2) * 0.002:
			if playerStats.oldRotation != playerStats.rotation:
				playerStats.animSpeedRegulator = 10
			moveDown(playerStats.obj)
			playerStats.t0 = time.time()
			playerAnim(playerStats.obj, playerStats)
	elif keyboard.is_pressed(playerStats.controls[3]):
		playerStats.oldRotation = playerStats.rotation
		playerStats.rotation = 'right'
		if time.time() - playerStats.t0 > 0.01 - (playerStats.playerSpeed - 2) * 0.002:
			if playerStats.oldRotation != playerStats.rotation:
				playerStats.animSpeedRegulator = 10
			moveRight(playerStats.obj)
			playerStats.t0 = time.time()
			playerAnim(playerStats.obj, playerStats)
	elif keyboard.is_pressed(playerStats.controls[0]):
		playerStats.oldRotation = playerStats.rotation
		if time.time() - playerStats.t0 > 0.01 - (playerStats.playerSpeed - 2) * 0.002:
			playerStats.rotation = 'up'
			if playerStats.oldRotation != playerStats.rotation:
				playerStats.animSpeedRegulator = 10
			moveUp(playerStats.obj)
			playerStats.t0 = time.time()
			playerAnim(playerStats.obj, playerStats)


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


allPlayersList = []

# spracovanie nastaveni
for i in range(4):
	subor = open(f'multiplayer_settings/{i + 1}.txt', 'r')
	entity = 'none yet'
	for j in subor:
		j = j.strip()
		if j == 'player':
			entity = 'player'
		elif j == 'ai':
			entity = 'ai'
		elif j == 'empty':
			break
		if j[:-1] == 'color':
			color = j
		if entity == 'player':
			if j == 'wasd x':
				controls = ['w', 'a', 's', 'd', 'x']
			elif j == 'ijkl m':
				controls = ['i', 'j', 'k', 'l', 'm']
			elif j == 'arrows space':
				controls = ['Up', 'Left', 'Down', 'Right', 'space']
			elif j == '8456 0':
				controls = ['8', '4', '5', '6', '0']
	if entity == 'player':
		allPlayersList.append(createPlayer(f'player{i + 1}', color, controls))
		platno.bind_all(f'<{controls[4]}>', placeBomb)
	elif entity == 'ai':
		allPlayersList.append(createPlayer(f'player{i + 1}', color, None))
	subor.close()

# nacitanie obrazkov pre hracov(tu a ne na zaciatku, lebo tu vie co a ako)
for i in allPlayersList:
	player1Sprites = []
	for j in range(10):
		playerImg = Image.open(f'bomberman_sprites/{i.color}/tile00{j}.png')
		playerImg = playerImg.resize((44, 87), Image.ANTIALIAS)
		playerImg = ImageTk.PhotoImage(playerImg)
		player1Sprites.append(playerImg)
	for j in range(10, 16):
		playerImg = Image.open(f'bomberman_sprites/{i.color}/tile0{j}.png')
		playerImg = playerImg.resize((44, 87), Image.ANTIALIAS)
		playerImg = ImageTk.PhotoImage(playerImg)
		player1Sprites.append(playerImg)
	i.sprites = player1Sprites

	# vytvaranie hracov(obrazkov)
playersZoznam = []
for i in range(len(allPlayersList)):
	if i == 0:
		player1 = platno.create_image(150, 80, image=allPlayersList[i].sprites[0])
		playersZoznam.append([player1, allPlayersList[i]])
		update_stats_coords(allPlayersList[i], player1)
		allPlayersList[i].obj = player1
	elif i == 1:
		player2 = platno.create_image(14 * 64 - 32, 80, image=allPlayersList[i].sprites[0])
		playersZoznam.append([player2, allPlayersList[i]])
		update_stats_coords(allPlayersList[i], player2)
		allPlayersList[i].obj = player2
	elif i == 2:
		player3 = platno.create_image(14 * 64 - 32, 80 + 64 * 10, image=allPlayersList[i].sprites[0])
		playersZoznam.append([player3, allPlayersList[i]])
		update_stats_coords(allPlayersList[i], player3)
		allPlayersList[i].obj = player3
	elif i == 3:
		player4 = platno.create_image(2 * 64 - 32, 80 + 64 * 10, image=allPlayersList[i].sprites[0])
		playersZoznam.append([player4, allPlayersList[i]])
		update_stats_coords(allPlayersList[i], player4)
		allPlayersList[i].obj = player4

for i in allPlayersList:
	update_powerup_board(i)
	# allPlayersList = zoznam statov vsetkych hracov(aj AI), playerZoznam = posuva sa to len pre aiLogic
	# koniec init hracov

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

		obstaclesMatrix[i][e] = createTile()
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

for i in allPlayersList:
	platno.tag_raise(i.obj)

t0 = time.time()  # cas na animaciu hraca

playerPlacedBombs = 0
bombAnimCounter = 0
bombTimerBomb = []
bombTimerTime = []

tExplosion = time.time()
tBombs = time.time()

explosionImgTracking = []
unwalkableBomb = []


platno.bind_all('<Button-1>', cisloDebug)


# mainloop

gamestate = 'playing'
strafecounter = 0  # player strafe movement TODO dat pohyb registrovanie atd. ako funkciu
while gamestate == 'playing':
	for i in allPlayersList:
		playerInput(i)

	if keyboard.is_pressed('Escape'):
		exit()

	for i in allPlayersList:  # ak je nejaka bomba polozena -> anim
		if i.bombPlaced != 0:
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

	for i in unwalkableBomb:
		solidify = 0
		for j in allPlayersList:
			if (i[0] != (math.floor((platno.coords(j)[0]) / 64))) or \
			(i[1] != (math.floor((platno.coords(j)[1]) / 64))):
				solidify += 1
		if solidify > 0:
			obstaclesMatrix[int(unwalkableBomb[1])][int(unwalkableBomb[0])].walkable = 'no'
#	if len(unwalkableBomb) != 0:   #toto nadtym multiplayer fix??
#		if (unwalkableBomb[0] != (math.floor((platno.coords(player1)[0]) / 64))) \
#				or (unwalkableBomb[1] != (math.floor((platno.coords(player1)[1]) / 64))):
#			obstaclesMatrix[int(unwalkableBomb[1])][int(unwalkableBomb[0])].walkable = 'no'
#			unwalkableBomb = []

	for i in allPlayersList:
		if obstaclesMatrix[i.coords[0]][i.coords[1]].tileName == 'explosion':
			if i.vest == 'no':
				print(i.name, ' skapal')
				platno.delete(i.obj)
				i.dead = True
				died('ai1')  #TODO died(stats) pre vsetkych

	for i in allPlayersList:
		if obstaclesMatrix[math.floor((platno.coords(i.obj)[1]) / 64)][math.floor((platno.coords(i.obj)[0]) / 64)].powerup != '':  # ak je tam nejaky powerup, ...
			powerup(obstaclesMatrix[math.floor((platno.coords(i.obj)[1]) / 64)][math.floor((platno.coords(i.obj)[0]) / 64)].powerup,
		        obstaclesMatrix[math.floor((platno.coords(i.obj)[1]) / 64)][math.floor((platno.coords(i.obj)[0]) / 64)].powerupObj)
			if i.name[:-1] == 'ai':
				i.current_target_powerup_list = []
				i.current_listXY = []
			obstaclesMatrix[math.floor((platno.coords(i)[1]) / 64)][
			math.floor((platno.coords(i)[0]) / 64)].powerup = ''

	for i in allPlayersList:
		if i.vest == 'yes':
			if time.time() - i.vestStartTime > 5:
				i.vest = 'no'
				i.vestStartTime = 0

	for i in allPlayersList:
		if i.dead != True:
			if time.time() - i.animTime > 0.01 - (i.playerSpeed - 2) * 0.002:  # anim + movement
				update_stats_coords(i, i.obj)
				if i.name[:-1] == 'ai':
					if (i.path != 'none') and (i.dead != True):
						ai_move(i.obj, i, i.sprites)
						i.animTime = time.time()
					else:
						aiLogic.decisionMaker(obstaclesMatrix, math.floor((platno.coords(i.obj)[1]) / 64)
							                      , math.floor((platno.coords(i.obj)[0]) / 64), i, playersZoznam)
						ai_place_bomb(i, i.obj)
	platno.update()

	aliveCounter = 0
	for i in allPlayersList:
		if i.dead == False:
			aliveCounter += 1
	if aliveCounter == 1:
		gamestate = 'victory'
	elif aliveCounter == 0:
		gamestate = 'draw'


if sound_settings:
	mixer.music.stop()

if gamestate == 'draw':  # TODO draw screen
	if sound_settings:
		mixer.Sound.play(death_sound)
	game_over = Image.open('other_textures/game_over.png')
	game_over = ImageTk.PhotoImage(game_over)
	g_over = platno.create_image((64 * 15 + 276) / 2, 64 * 13 / 2, image=game_over)
	platno.update()

elif gamestate == 'victory':  # TODO kto vyhral?
	mixer.Sound.play(victory_sound)
	game_won = Image.open('other_textures/victory_screen.png')
	game_won = ImageTk.PhotoImage(game_won)
	g_won = platno.create_image((64 * 15 + 276) / 2, 64 * 13 / 2, image=game_won)
	platno.update()


time.sleep(0.5)
keyboard.wait('Space')
okno.destroy()
