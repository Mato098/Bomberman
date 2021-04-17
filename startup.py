#! python3

import tkinter, random
import os, sys
from pygame import mixer
#from main_multiplayer import resource_path



def resource_path(relative_path):
    #try:
        #base_path = sys._MEIPASS
    #except Exception:
    base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)


okenko = tkinter.Tk()
okenko.title('Bomberman')
okenko.focus_force()
sirka = 64 * 15  # playable area je 13*11 ale s krajmi je 15*13
vyska = 64 * 13  # 64*64
platno = tkinter.Canvas(width=sirka, height=vyska)
platno.pack()

backgrounasd = tkinter.PhotoImage(file=resource_path('other_textures/bg64.png'))
background = tkinter.PhotoImage(file=resource_path('other_textures/menu.png'))
start_normal = tkinter.PhotoImage(file=resource_path('other_textures/start_game_normal.png'))
start_hover = tkinter.PhotoImage(file=resource_path('other_textures/start_game_hover.png'))
quit_normal = tkinter.PhotoImage(file=resource_path('other_textures/quit_normal.png'))
quit_hover = tkinter.PhotoImage(file=resource_path('other_textures/quit_hover.png'))
sound_on = tkinter.PhotoImage(file=resource_path('other_textures/sound_on.png'))
sound_off = tkinter.PhotoImage(file=resource_path('other_textures/sound_off.png'))
singleplayer = tkinter.PhotoImage(file=resource_path('other_textures/singleplayer.png'))
multiplayer = tkinter.PhotoImage(file=resource_path('other_textures/multiplayer.png'))
platno.create_image(64 * 15 / 2, 64 * 13 / 2, image=background)
start = platno.create_image(64 * 15 / 2, 450, image=start_normal)
quit = platno.create_image(64 * 15 / 2, 520, image=quit_normal)
platno.config(cursor='dotbox')

colors = ['color2', 'color3', 'color4', 'color5', 'color6']

subor = open(resource_path('sound/settings.txt'), 'r')
for i in subor:
	i.strip()
	if i == 'on':
		sound_settings = True
	elif i == 'off':
		sound_settings = False
subor.close()

if sound_settings:
	sound_image = platno.create_image(50, 50, image=sound_on)
else:
	sound_image = platno.create_image(50, 50, image=sound_off)

def pohybMysi(event):
	global start
	global quit
	x, y = event.x, event.y
	if (240 < x < 720) and (420 < y < 480):
		platno.delete(start)
		start = platno.create_image(64 * 15 / 2, 450, image=start_hover)
	else:
		platno.delete(start)
		start = platno.create_image(64 * 15 / 2, 450, image=start_normal)
	if (240 < x < 720) and (490 < y < 540):
		platno.delete(quit)
		quit = platno.create_image(64 * 15 / 2, 520, image=quit_hover)
	else:
		platno.delete(quit)
		quit = platno.create_image(64 * 15 / 2, 520, image=quit_normal)

mode_selection = 0
def click(event):
	global  menu_tune
	global  sound_settings
	global sound_image
	global mode_selection
	if sound_settings:
		mixer.Sound.play(click_sound)

	x, y = event.x, event.y
	if (240 < x < 720) and (420 < y < 480):  # mode selection
		sp = platno.create_image(64 * 15 / 2 - 100, 330, image=singleplayer)
		mp = platno.create_image(64 * 15 / 2 + 100, 330, image=multiplayer)
		mode_selection = 1

	elif (64 * 15 / 2 - 200 < x < 64 * 15 / 2) and (240 < y < 430) and (mode_selection == 1):  # start singleplayer game
		okenko.destroy()
		if sound_settings:
			mixer.music.stop()

		for i in range(1, 5):
			subor = open(resource_path(f'multiplayer_settings/{i}.txt'), 'w')
			if i == 1:
				print('asd')
				subor.write('player\n')
				subor.write('color1\n')
				subor.write('wasd x\n')
			elif i > 1:
				aiColor = random.choice(colors)
				colors.pop(colors.index(aiColor))

				subor.write('CPU\n')
				subor.write(f'{aiColor}\n')
				subor.write('wasd x\n')
			subor.close()
		subor = open(resource_path('multiplayer_settings/mode.txt'), 'w')
		subor.write('singleplayer')
		subor.close()

		#import main  # launch game
		import main_multiplayer
		os.system('python "startup.py"')  # restart startup.py(else 'main' will not be imported again)

	elif (64 * 15 / 2 < x < 64 * 15 / 2 + 200) and (240 < y < 430) and (mode_selection == 1):  # start multiplayer game
		okenko.destroy()
		if sound_settings:
			mixer.music.stop()

		import multiplayer_settings_menu

		subor = open(resource_path('multiplayer_settings/mode.txt'), 'w')
		subor.write('multiplayer')
		subor.close()

		import main_multiplayer  # launch game
		os.system('python "startup.py"')  # restart startup.py(else 'main' will not be imported again)

	elif (240 < x < 720) and (490 < y < 540):  # quit
		sys.exit()
	elif (x < 100) and (y < 100):  # sound toggle
		subor = open(resource_path('sound/settings.txt'), 'r')
		for i in subor:
			i.strip()
			if i == 'on':
				sound_settings = True
			elif i == 'off':
				sound_settings = False
		subor.close()
		subor = open(resource_path('sound/settings.txt'), 'w')
		if sound_settings == True:
			subor.write('off')
			sound_settings = False
		else:
			subor.write('on')
			sound_settings = True
		subor.close()

		if sound_settings:
			mixer.music.play(-1)
			platno.delete(sound_image)
			sound_image = platno.create_image(50, 50, image=sound_on)
		elif sound_settings == False:
			mixer.music.stop()
			platno.delete(sound_image)
			sound_image = platno.create_image(50, 50, image=sound_off)


def koniec(event):
	exit()


mixer.init()
mixer.music.load(resource_path('sound/menu_tune.wav'))
if sound_settings:
	mixer.music.play(-1)

click_sound = mixer.Sound(resource_path('sound/menu_select.wav'))


platno.bind('<Motion>', pohybMysi)
platno.bind('<Button-1>', click)
platno.bind_all('<Escape>', koniec)
tkinter.mainloop()
