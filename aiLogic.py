from enum import IntEnum
import math


class Policko(IntEnum):
	krabica = 0
	stena = 1
	volne = 2
	bomba = 3


upScore = 0  # na pathfinding
downScore = 0
leftScore = 0
rightScore = 0


def decisionMaker(obstaclesmatrix, positionY, positionX, stats, playersZoznam):

	if dangerCalculator(obstaclesmatrix, positionX, positionY):  # ci nieje v nebezpecenstve
		pathfinder_master(obstaclesmatrix, positionX, positionY, stats, 'danger', playersZoznam)  # ide z tade het
		if stats.current_target_powerup_list != []:
			move_podla_zoznamu(positionX, positionY, stats, obstaclesmatrix, 'danger')
		for i in range(13):
			for e in range(15):
				obstaclesmatrix[i][e].aiSeen = 'no'
	else:
		if 1 == 1:
			if (stats.current_target_powerup_list == [None]) or (stats.current_target_powerup_list == []):  # ak nema ziaden ciel(powerup)
				pathfinder_master(obstaclesmatrix, positionX, positionY, stats, 'powerup', playersZoznam)  # tak si najde
				stats.job = 'powerup'
			else:  # ak uz tam nejaka cesta je, t.j. ma ju nasledovat, nasleduje ju
				if stats.job == 'powerup':
					move_podla_zoznamu(positionX, positionY, stats, obstaclesmatrix, 'powerup')
		for i in range(13):
			for e in range(15):
				obstaclesmatrix[i][e].aiSeen = 'no'

		if stats.current_target_powerup_list == []:
			pathfinder_master(obstaclesmatrix, positionX, positionY, stats, 'player_search', playersZoznam)
			stats.job = 'player'
		elif stats.job == 'player':

				move_podla_zoznamu(positionX, positionY, stats, obstaclesmatrix, 'powerup')

		if stats.current_target_powerup_list == []:
			pathfinder_master(obstaclesmatrix, positionX, positionY, stats, 'player_wall_search', playersZoznam)
			stats.job = 'player_wall'
		elif stats.job == 'player_wall':
			move_podla_zoznamu(positionX, positionY, stats, obstaclesmatrix, 'player_wall')

		check_for_targets(obstaclesmatrix, positionX, positionY, stats, playersZoznam)

	return stats


def pathfinder_master(obstaclesmatrix, aiX, aiY, stats, purpose, playersZoznam):
	global upScore, downScore, rightScore, leftScore
	stats.path = 'none'
	upScore = []
	downScore = []
	leftScore = []
	rightScore = []

	if obstaclesmatrix[aiY - 1][aiX].cislo == Policko.volne:  # hore
		obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
		upScore = []
		upScore = pathfinder_slave(obstaclesmatrix, aiX, aiY - 1, stats, upScore, purpose, playersZoznam)
		for i in range(13):
			for e in range(15):
				obstaclesmatrix[i][e].aiSeen = 'no'


	if 	obstaclesmatrix[aiY + 1][aiX].cislo == Policko.volne:  # dole
			obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
			downScore = []
			downScore = pathfinder_slave(obstaclesmatrix, aiX, aiY + 1, stats, downScore, purpose, playersZoznam)
			for i in range(13):
				for e in range(15):
					obstaclesmatrix[i][e].aiSeen = 'no'

	if obstaclesmatrix[aiY][aiX + 1].cislo == Policko.volne:  # vpravo
			obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
			rightScore = []
			rightScore = pathfinder_slave(obstaclesmatrix, aiX + 1, aiY, stats, rightScore, purpose, playersZoznam)
			for i in range(13):
				for e in range(15):
					obstaclesmatrix[i][e].aiSeen = 'no'

	if obstaclesmatrix[aiY][aiX - 1].cislo == Policko.volne:  # vlavo
			obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
			leftScore = []
			leftScore = pathfinder_slave(obstaclesmatrix, aiX - 1, aiY, stats, leftScore, purpose, playersZoznam)
			for i in range(13):
				for e in range(15):
					obstaclesmatrix[i][e].aiSeen = 'no'


	if (upScore == []) and \
		(downScore == []) and \
		(rightScore == []) and \
		(leftScore == []):
		return False
	else:
		zoznam = [upScore, downScore, rightScore, leftScore]
		zoznam2 = []
		toPop = []
		for i in range(len(zoznam)):  # z [X,Y] zoznamu urobi h zoznam2    h=vzdusna vzdialenost
			if (zoznam[i] != []) and (zoznam[i] != 0):
				zoznam2.append(math.sqrt((aiX + zoznam[i][0]) ** 2 + (aiY + zoznam[i][1]) ** 2))

				zoznam[i] = A_star([aiX, aiY], zoznam[i], obstaclesmatrix, purpose)  # jednotlive X,Y ciele zmeni na A* output
			else:
				toPop.append(i)

		toPop.reverse()
		for i in toPop:  # odstrani zo zoznamu debility ako []
			zoznam.pop(i)

		najkratsiaCesta = min(zoznam2)  # da do {cesta} najkratsiu z 4 ciest co tam boli
		cesta = zoznam[zoznam2.index(najkratsiaCesta)]

		stats.current_target_powerup_list = cesta


def pathfinder_slave(obstaclesmatrix, aiX, aiY, stats, score, purpose, playersZoznam):

	if obstaclesmatrix[aiY][aiX].cislo == Policko.stena:
		return []

	if obstaclesmatrix[aiY][aiX].cislo == Policko.krabica:
		if purpose == 'player_wall_search':
			return [aiX, aiY]
		else:
			return []
	if obstaclesmatrix[aiY][aiX].cislo == Policko.bomba:
		return []
	if obstaclesmatrix[aiY][aiX].aiSeen == 'yes':
		return []
	if obstaclesmatrix[aiY][aiX].tileName == 'explosion':
		return []
	if purpose == 'powerup':
		if dangerCalculator(obstaclesmatrix, aiX, aiY) == False:
			if obstaclesmatrix[aiY][aiX].powerup != '':
				return [aiX, aiY]
		else:
			return []
	elif purpose == 'danger':
		if dangerCalculator(obstaclesmatrix, aiX, aiY) == False:
			return [aiX, aiY]
	elif purpose == 'player_search':
		for i in range(len(playersZoznam)):
			if i % 2 == 0:
				#print(playersZoznam[i][1].coords)
				if (playersZoznam[i][1].coords[1] == aiX) and (playersZoznam[i][1].coords[0] == aiY):
					return [aiX, aiY]


	obstaclesmatrix[aiY][aiX].aiSeen = 'yes'

	seqX = [+1, +0, -1, +0]
	seqY = [+0, +1, +0, -1]

	for i in range(4):

		if (score := pathfinder_slave(obstaclesmatrix, aiX + seqX[i], aiY + seqY[i], stats, score, purpose, playersZoznam)) != []:  # vpravo
			#print('score' + str(score))
			#score += 1
			return score

	return score


def check_for_targets(obstaclesmatrix, aiX, aiY, stats, playersZoznam):
	for i in playersZoznam:
		targetX = i[1].coords[1]
		targetY = i[1].coords[0]

		placing = False  # ci na konci polozi bombu alebo ne

		if (targetX == aiX) and (targetY == aiY):  # aby nepocital s tym ze on sam je oponent(aj ked dakto stoji na nom
			# ta nebude davat... ale to by sa nemalo stat, keby hej, ta nevadi?)
			break

		if targetY == aiY:  # checkne vodorovne
			if stats.bombRangeFull == 'no':
				if abs(targetX - aiX) <= (stats.bombRange + 1):  # ak vie bomba zasiahnut niekoho:
					if stats.piercing == 'no':  # ak neni piercing, pozre ci je medzi nimi krabica
						if abs(targetX - aiX) >= 1:  # hmmmm?
							if aiX > targetX:  # ak je AI napravo od ciela
								for k in range(aiX - targetX):
									if (obstaclesmatrix[targetY][targetX + k].cislo == Policko.krabica) or\
										(obstaclesmatrix[targetY][targetX + k].cislo == Policko.stena):  # ak je medzi nimi krabica
										placing = False
										break
									else:
										placing = True

							if aiX < targetX:  # ak je AI nalavo od ciela
								for k in range(targetX - aiX):
									if (obstaclesmatrix[targetY][targetX - k].cislo == Policko.krabica) or\
										(obstaclesmatrix[targetY][targetX - k].cislo == Policko.stena):
										placing = False
										break
									else:
										placing = True
					else:  # piercing bomba klasicka
						placing = True
			else:  # full bomba bez, aj s piercingom
				if stats.piercing == 'no':  # pozre ci je medzi nimi krabica
					if aiX > targetX:
						for k in range(aiX - targetX):
							if (obstaclesmatrix[targetY][targetX + k].cislo == Policko.krabica) or\
								(obstaclesmatrix[targetY][targetX + k].cislo == Policko.stena):
								placing = False
								break
							else:
								placing = True
					if aiX < targetX:
						for k in range(targetX - aiX):
							if (obstaclesmatrix[targetY][targetX - k].cislo == Policko.krabica) or \
								(obstaclesmatrix[targetY][targetX - k].cislo == Policko.stena):
								placing = False
								break
							else:
								placing = True
			if placing:
				#print('AI places a bomb')
				ai_place_bomb(obstaclesmatrix, aiX, aiY, stats)
				return

		elif targetX == aiX:  # horizontalne checkuje
			if stats.bombRangeFull == 'no':
				if abs(targetY - aiY) <= (stats.bombRange + 1):  # ak vie bomba zasiahnut niekoho:
					if stats.piercing == 'no':  # ak neni piercing, pozre ci je medzi nimi krabica
						if abs(targetY - aiY) >= 1:  # hmmmm?
							if aiY > targetY:  # ak je AI pod cielom
								for k in range(aiY - targetY):
									if (obstaclesmatrix[targetY - k][targetX].cislo == Policko.krabica) or \
									(obstaclesmatrix[targetY - k][targetX].cislo == Policko.stena):  # ak je medzi nimi krabica
										placing = False
										break
									else:
										placing = True

							if aiY < targetY:  # ak je AI nad cielom
								for k in range(targetY - aiY):
									if (obstaclesmatrix[targetY + k][targetX].cislo == Policko.krabica) or \
										(obstaclesmatrix[targetY + k][targetX].cislo == Policko.stena):
										placing = False
										break
									else:
										placing = True
					else:  # piercing bomba klasicka
						placing = True
			else:  # full bomba bez, aj s piercingom
				if stats.piercing == 'no':  # pozre ci je medzi nimi krabica
					if aiY > targetY:  # ai je pod cielom
						for k in range(aiY - targetY):
							if (obstaclesmatrix[targetY - k][targetX].cislo == Policko.krabica) or\
								(obstaclesmatrix[targetY - k][targetX].cislo == Policko.stena):

								placing = False
								break
							else:
								placing = True
					if aiY < targetY:  # ak je ai nad cielom
						for k in range(targetY - aiY):
							if (obstaclesmatrix[targetY + k][targetX].cislo == Policko.krabica)\
									or obstaclesmatrix[targetY + k][targetX].cislo == Policko.stena:
								placing = False
								break
							else:
								placing = True
			if placing:
				#print('AI places a bomb')
				ai_place_bomb(obstaclesmatrix, aiX, aiY, stats)
				return


def ai_place_bomb(obstaclesmatrix, aiX, aiY, stats):
	if stats.bombAmount > stats.bombPlaced:
		if obstaclesmatrix[aiY][aiX].cislo != Policko.bomba:
			stats.placeBomb = True
			if stats.name == 'ai1':
				print('ai1', end='')


def dangerCalculator(obstaclesmatrix, positionX, positionY):  # ci je v dosahu nejakej bomby

	for i in range(len(obstaclesmatrix[positionY])):  # vodorovne pozera na nebezpecenstvo
		if obstaclesmatrix[positionY][i].cislo == Policko.bomba:
			if obstaclesmatrix[positionY][i].bombRangeFull == 'no':
				for j in range(1, obstaclesmatrix[positionY][i].bombRange + 2):
					if (positionX == i) or (positionX == i - j) or (positionX == i + j):  # ak vie bomba ho zasiahnut

						if obstaclesmatrix[positionY][i].piercingBomb == 'no':  # ak neni piercing, pozre ci je medzi nimi krabica
							if abs(positionX - i) > 1:
								if i > positionX:
									for k in range(i - positionX):
										if obstaclesmatrix[positionY][positionX + k].cislo == Policko.krabica:
											return False
								if i < positionX:
									for k in range(positionX - i):
										if obstaclesmatrix[positionY][positionX - k].cislo == Policko.krabica:
											return False

						return True
			else:  # full bomba bez aj s piercingom
				if obstaclesmatrix[positionY][i].piercingBomb == 'no':  # pozre ci je medzi nimi krabica
					if abs(positionX - i) > 1:
						if i > positionX:
							for k in range(i - positionX):
								if obstaclesmatrix[positionY][positionX + k].cislo == Policko.krabica:
									return False
						if i < positionX:
							for k in range(positionX - i):
								if obstaclesmatrix[positionY][positionX - k].cislo == Policko.krabica:
									return False
					return True
				else:  # je full s piercingom
					return True

	for i in range(1, 12):  # pozera na nebezpecenstvo zvislo
		if obstaclesmatrix[i][positionX].cislo == Policko.bomba:
			#print(obstaclesmatrix[i][positionX].bombRange)
			if obstaclesmatrix[i][positionX].bombRangeFull == 'no':
				for j in range(1, obstaclesmatrix[i][positionX].bombRange + 2):
					if (positionY == i) or (positionY == i - j) or (
							positionY == i + j):  # ak vie bomba ho zasiahnut

						if obstaclesmatrix[i][positionX].piercingBomb == 'no':  # ak neni piercing, pozre ci je medzi nimi krabica
							if abs(positionY - i) > 1:
								if i > positionY:
									for k in range(i - positionY):
										if obstaclesmatrix[positionY + k][positionX].cislo == Policko.krabica:
											return False
								if i < positionY:
									for k in range(positionY - i):
										if obstaclesmatrix[positionY - k][positionX].cislo == Policko.krabica:
											return False
						return True

			else:  # full bomba bez aj s piercingom
				if obstaclesmatrix[i][positionX].piercingBomb == 'no':  # not correct?
					if abs(positionY - i) > 1:
						if i > positionY:
							for k in range(i - positionY):
								if obstaclesmatrix[positionY + k][positionX].cislo == Policko.krabica:
									return False
						if i < positionY:
							for k in range(positionY - i):
								if obstaclesmatrix[positionY - k][positionX].cislo == Policko.krabica:
									return False
					return True
				else:  # je full a piercing
					return True

	return False


def A_get_h(start, goal):  # pocita heuristic distance = vzdialenost k cielu vzdusnou ciarou

	a = abs(goal[0] - start[0])
	b = abs(goal[1] - start[1])
	heuristic_distance = math.sqrt(a**2 + b**2)
	return heuristic_distance


	# A* algoritmus
def A_star(start, goal, matrix, purpose):  # start, goal = tuple - start[X, Y]
	open = []
	closed = []
					# [coords[x, y] of that square, g(vzdialenost prejdena od zaciatku),
	#                   h(vzdusna vzdialenost k cielu), f(g + h), predchadzajuci block(coords)]
	open.append([start, 0, A_get_h(start, goal), A_get_h(start, goal), None])
	node_current = 'cisty blud'

	while open != []:
		najmensi_f = 9999

		for i in open:  # z open vyberie to s najmensim h
			if i[3] < najmensi_f:
				najmensi_f = i[3]
				node_current = i

		if node_current[0] == goal:  # ak je dane policko cielom
			#print('mam ciel')
			closed.append(node_current)
			break

		seqX = [+1, +0, -1, +0]
		seqY = [+0, +1, +0, -1]
		for i in range(4):  # generate succesors
			succ_coords = [seqX[i] + node_current[0][0], seqY[i] + node_current[0][1]]
			succ_cost = node_current[1] + 1

			oo = 0  # iba nato ze ci je pravda niektore z tych for--ov

			for j in open:  # ci je ten successor v OPEN
				if j[0] == succ_coords:
					if j[1] <= succ_cost:  # ak terajsia cesta je kratsia ako ta, kt. je zapisana v potomkovi(successore)
						oo = 1
						j[4] = node_current[4] # zmeni parenta na toho co na terajsieho(co ma kratsiu cestu)

			for j in closed:  # ci je ten successor v CLOSED
				if j[0] == succ_coords:
					if j[1] <= succ_cost:
						oo = 2
						#j[4] = node_current[4]
					else:
						a = closed.index(j)
						closed.pop(a)
						open.append(j)  # move from closed to open

			if oo == 0:  # add to open
				#print(succ_coords)

				if (matrix[succ_coords[1]][succ_coords[0]].cislo == Policko.volne) or \
						((matrix[succ_coords[1]][succ_coords[0]].cislo == Policko.krabica) and (purpose == 'player_wall_search')):
					open.append([succ_coords, succ_cost, A_get_h(succ_coords, goal),
									succ_cost + A_get_h(succ_coords, goal), node_current[0]])

		a = open.index(node_current)
		open.pop(a)
		closed.append(node_current)

	if node_current[0] != goal:
		print('OPEN list is empty!')

	else:  # list branches cleanup
		origo = []
		for i in closed:
			origo.append(i)
		origo.reverse()

		gut = []
		gut.append(origo[0])  # [coords[x, y] of that square, g, h, f(g + h), predchadzajuci block(coords)]

		while gut[len(gut) - 1] != closed[0]:
			for i in origo:
				if i[0] == gut[len(gut) - 1][4]:  # toto nerobi to co ma
					gut.append(i)

		gut.reverse()
		gut.pop(0)

		return gut


def move_podla_zoznamu(aiX, aiY, stats, obstaclesmatrix, purpose):
	zoznam = stats.current_target_powerup_list
	#print(zoznam)

	standing_onXY = zoznam[0][4]
	next_stepXY = zoznam[0][0]

	stats.current_target_powerup_list.pop(0)

	smer = [next_stepXY[0] - standing_onXY[0], next_stepXY[1] - standing_onXY[1]]

	if stats.name == 'ai1':
		print(purpose, end='')
		print(zoznam)

	if obstaclesmatrix[next_stepXY[1]][next_stepXY[0]].cislo == Policko.bomba:
		print('le bomba')
		stats.path = 'none'
		stats.current_target_powerup_list = []
		stats.current_listXY = []
		return

	if (obstaclesmatrix[next_stepXY[1]][next_stepXY[0]].cislo == Policko.krabica) and (purpose == 'player_wall'):
		ai_place_bomb(obstaclesmatrix, aiX, aiY, stats)
		stats.path = 'none'
		stats.current_target_powerup_list = []
		stats.current_listXY = []
		return

	if (obstaclesmatrix[next_stepXY[1]][next_stepXY[0]].tileName == 'explosion'):
		stats.path = 'none'
		stats.current_target_powerup_list = []
		stats.current_listXY = []
		return

	if(dangerCalculator(obstaclesmatrix, next_stepXY[0], next_stepXY[1]) == False) or (purpose == 'danger'):
		if smer == [0, -1]:
			stats.path = 'up'
		elif smer == [0, 1]:
			stats.path = 'down'
		elif smer == [1, 0]:
			stats.path = 'right'
		elif smer == [-1, 0]:
			stats.path = 'left'
		else:
			print('neni dobry smer tunak')
			stats.path = 'none'
			stats.current_target_powerup_list = []
			stats.current_listXY = []
		#print(stats.path)
	else:
		print('wont go there - danger')
		stats.current_target_powerup_list = []
		stats.current_listXY = []
















