from tkinter import *

okno = Tk()
okno.title('Multiplayer settings')
okno.focus_force()

pltype_text = StringVar(okno)
pltype_text.set('Player type')
plcolor_text = StringVar(okno)
plcolor_text.set('Color')
plcontrols_text = StringVar(okno)
plcontrols_text.set('Controls')

pl1_text = StringVar(okno)  # SLOT 1 data
pl1_text.set('Slot 1')
player1 = StringVar(okno)
player1.set("player")  # default value
color1 = StringVar(okno)
color1.set('white')
controls1 = StringVar(okno)
controls1.set('wasd x')

pl2_text = StringVar(okno)  # SLOT 2 data
pl2_text.set('Slot 2')
player2 = StringVar(okno)
player2.set("player")
color2 = StringVar(okno)
color2.set('orange')
controls2 = StringVar(okno)
controls2.set('ijkl m')

pl3_text = StringVar(okno)  # SLOT 3 data
pl3_text.set('Slot 3')
player3 = StringVar(okno)
player3.set("player")
color3 = StringVar(okno)
color3.set('green')
controls3 = StringVar(okno)
controls3.set('arrows space')

pl4_text = StringVar(okno)  # SLOT 4 data
pl4_text.set('Slot 4')
player4 = StringVar(okno)
player4.set("player")
color4 = StringVar(okno)
color4.set('pink')
controls4 = StringVar(okno)
controls4.set('8456 0')

pltype = Label(okno, textvariable=pltype_text).grid(row=0, column=1)
plcolor = Label(okno, textvariable=plcolor_text).grid(row=0, column=2)
plcontrols = Label(okno, textvariable=plcontrols_text).grid(row=0, column=3)
pl1 = Label(okno, textvariable=pl1_text).grid(row=1, column=0)
pl2 = Label(okno, textvariable=pl2_text).grid(row=2, column=0)
pl3 = Label(okno, textvariable=pl3_text).grid(row=3, column=0)
pl4 = Label(okno, textvariable=pl4_text).grid(row=4, column=0)

player1_menu = OptionMenu(okno, player1, "player", "CPU", "empty").grid(row=1, column=1)
color1_menu = OptionMenu(okno, color1, "white", "orange", "blue", "pink", "green", "terminator").grid(row=1, column=2)
controls1_menu = OptionMenu(okno, controls1, "wasd x", "ijkl m", "arrows space", "8456 0").grid(row=1, column=3)

player2_menu = OptionMenu(okno, player2, "player", "CPU", "empty").grid(row=2, column=1)
color2_menu = OptionMenu(okno, color2, "white", "orange", "blue", "pink", "green", "terminator").grid(row=2, column=2)
controls2_menu = OptionMenu(okno, controls2, "wasd x", "ijkl m", "arrows space", "8456 0").grid(row=2, column=3)

player3_menu = OptionMenu(okno, player3, "player", "CPU", "empty").grid(row=3, column=1)
color3_menu = OptionMenu(okno, color3, "white", "orange", "blue", "pink", "green", "terminator").grid(row=3, column=2)
controls3_menu = OptionMenu(okno, controls3, "wasd x", "ijkl m", "arrows space", "8456 0").grid(row=3, column=3)

player4_menu = OptionMenu(okno, player4, "player", "CPU", "empty").grid(row=4, column=1)
color4_menu = OptionMenu(okno, color4, "white", "orange", "blue", "pink", "green", "terminator").grid(row=4, column=2)
controls4_menu = OptionMenu(okno, controls4, "wasd x", "ijkl m", "arrows space", "8456 0").grid(row=4, column=3)


# txt file formatting
# line 1 - player type(player/ai/empty)
# line 2 - color(color1/color2/...)
# line 3 - controls(wasd x/ijkl m/arrows space/8456 0)


def start_game():  # writes settings into files, for the game to work with
	global player1, color1, controls1, player2, color2, controls2, player3, color3, controls3, player4, color4, controls4
	colors = [color1, color2, color3, color4]

	for i in colors:
		if i.get() == 'white':
			i.set('color1')
		elif i.get() == 'orange':
			i.set('color2')
		elif i.get() == 'blue':
			i.set('color3')
		elif i.get() == 'pink':
			i.set('color4')
		elif i.get() == 'green':
			i.set('color5')
		elif i.get() == 'terminator':
			i.set('color6')

	a = player1, color1, controls1
	b = player2, color2, controls2
	c = player3, color3, controls3
	d = player4, color4, controls4

	file1 = open('multiplayer_settings/1.txt', 'w')
	for i in a:
		file1.write(i.get())
		file1.write('\n')
	file1.close()

	file2 = open('multiplayer_settings/2.txt', 'w')
	for i in b:
		file2.write(i.get())
		file2.write('\n')
	file2.close()

	file3 = open('multiplayer_settings/3.txt', 'w')
	for i in c:
		file3.write(i.get())
		file3.write('\n')
	file3.close()

	file4 = open('multiplayer_settings/4.txt', 'w')
	for i in d:
		file4.write(i.get())
		file4.write('\n')
	file4.close()
	okno.destroy()


start_text = StringVar()
start_text.set('START')
start = Button(okno, textvariable=start_text, bg='green', command=start_game).grid(row=5, column=0)

mainloop()
