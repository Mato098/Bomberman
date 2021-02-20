#! python3


import tkinter
import os
from pygame import mixer

okenko = tkinter.Tk()
okenko.title('Bomberman')
okenko.focus_force()
sirka = 64 * 15  # playable area je 13*11 ale s krajmi je 15*13
vyska = 64 * 13  # 64*64
platno = tkinter.Canvas(width=sirka, height=vyska)
platno.pack()

background = tkinter.PhotoImage(file='other_textures/menu.png')
start_normal = tkinter.PhotoImage(file='other_textures/start_game_normal.png')
start_hover = tkinter.PhotoImage(file='other_textures/start_game_hover.png')
quit_normal = tkinter.PhotoImage(file='other_textures/quit_normal.png')
quit_hover = tkinter.PhotoImage(file='other_textures/quit_hover.png')
platno.create_image(64 * 15 / 2, 64 * 13 / 2, image=background)
start = platno.create_image(64 * 15 / 2, 450, image=start_normal)
quit = platno.create_image(64 * 15 / 2, 520, image=quit_normal)
platno.config(cursor='dotbox')
aa = 0




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


def click(event):
	global aa
	global  menu_tune
	x, y = event.x, event.y
	if (240 < x < 720) and (420 < y < 480):
		aa += 1
		okenko.destroy()

		mixer.Sound.play(click_sound)
		mixer.music.stop()

		import main  # launch game
		os.system('python "startup.py"')  # restart startup.py(else 'main' will not be imported again)

	elif (240 < x < 720) and (490 < y < 540):
		exit()


def koniec(event):
	exit()


mixer.init()
mixer.music.load('sound/menu_tune.wav')
mixer.music.play(-1)

click_sound = mixer.Sound('sound/menu_select.wav')


platno.bind('<Motion>', pohybMysi)
platno.bind('<Button-1>', click)
platno.bind_all('<Escape>', koniec)
tkinter.mainloop()
