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
		dangerPathCalculator(obstaclesmatrix, positionX, positionY, positionX, positionY, stats)  # ide z tade het
		for i in range(13):
			for e in range(15):
				obstaclesmatrix[i][e].aiSeen = 'no'
	else:
		nearest_target_rekurzivne_master(obstaclesmatrix, positionX, positionY, stats)  # dorobit

		if stats.name == 'ai1':
			if (stats.current_target_powerup_list == [None]) or (stats.current_target_powerup_list == []):  # ak nema ziaden ciel(powerup)
				nearest_powerup_rekurzivne_master(obstaclesmatrix, positionX, positionY, stats)  # tak si najde
			else:  # ak uz tam nejaka cesta je, t.j. ma ju nasledovat, nasleduje ju
				move_podla_zoznamu(positionX, positionY, stats)

		for i in range(13):
			for e in range(15):
				obstaclesmatrix[i][e].aiSeen = 'no'



	return stats


def nearest_powerup_rekurzivne_master(obstaclesmatrix, aiX, aiY, stats):
	global upScore, downScore, rightScore, leftScore
	stats.path = 'none'
	upScore = []
	downScore = []
	leftScore = []
	rightScore = []

	if obstaclesmatrix[aiY - 1][aiX].cislo == 2:  # hore
		obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
		upScore = []
		upScore = nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX, aiY - 1, stats, upScore)

		for i in range(13):
			for e in range(15):
				obstaclesmatrix[i][e].aiSeen = 'no'


	if 	obstaclesmatrix[aiY + 1][aiX].cislo == 2:  # dole
			obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
			downScore = []
			downScore = nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX, aiY + 1, stats, downScore)

			for i in range(13):
				for e in range(15):
					obstaclesmatrix[i][e].aiSeen = 'no'

	if obstaclesmatrix[aiY][aiX + 1].cislo == 2:  # vpravo
			obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
			rightScore = []
			rightScore = nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX + 1, aiY, stats, rightScore)

			for i in range(13):
				for e in range(15):
					obstaclesmatrix[i][e].aiSeen = 'no'

	if obstaclesmatrix[aiY][aiX - 1].cislo == 2:  # vlavo
			obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
			leftScore = []
			leftScore = nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX - 1, aiY, stats, leftScore)

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
				#print(zoznam[i])
				zoznam2.append(math.sqrt((aiX + zoznam[i][0]) ** 2 + (aiY + zoznam[i][1]) ** 2))

				zoznam[i] = A([aiX, aiY], zoznam[i], obstaclesmatrix)  # jednotlive X,Y ciele zmeni na A* output
			else:
				toPop.append(i)

		toPop.reverse()
		for i in toPop:  # odstrani zo zoznamu debility ako []
			zoznam.pop(i)

		najkratsiaCesta = min(zoznam2)  # da do {cesta} najkratsiu z 4 ciest co tam boli
		cesta = zoznam[zoznam2.index(najkratsiaCesta)]
		#print('cesta')
		#print(cesta)

		#cesta.reverse()

		stats.current_target_powerup_list = cesta



def nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX, aiY, stats, score):

	if obstaclesmatrix[aiY][aiX].cislo == Policko.stena:
		return []
	if obstaclesmatrix[aiY][aiX].cislo == Policko.krabica:
		return []
	if obstaclesmatrix[aiY][aiX].cislo == Policko.bomba:
		return []
	if obstaclesmatrix[aiY][aiX].aiSeen == 'yes':
		return []
	if obstaclesmatrix[aiY][aiX].tileName == 'explosion':
		return []
	if obstaclesmatrix[aiY][aiX].powerup != '':
		return [aiX, aiY]

	obstaclesmatrix[aiY][aiX].aiSeen = 'yes'

	seqX = [+1, +0, -1, +0]
	seqY = [+0, +1, +0, -1]

	for i in range(4):

		if (score := nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX + seqX[i], aiY + seqY[i], stats, score)) != []:  # vpravo
			#print('score' + str(score))
			#score += 1
			return score

	return score


def nearest_target_rekurzivne_master(obstaclesmatrix, positionX, positionY, stats):
	pass


def target_destructable_path_calculator(obstaclesmatrix, positionX, positionY, targetX, targetY):
	pass


def dangerCalculator(obstaclesmatrix, positionX, positionY):  # ci je v dosahu nejakej bomby

	for i in range(len(obstaclesmatrix[positionY])):  # vodorovne pozera na nebezpecenstvo
		if obstaclesmatrix[positionY][i].cislo == Policko.bomba:
			#print(obstaclesmatrix[positionY][i].bombRange)
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


def dangerPathCalculator(obstaclesmatrix, positionX, positionY, aiX, aiY, stats):
	stats.path = 'none'
	if obstaclesmatrix[positionY][positionX].cislo == Policko.stena:
		return False
	if obstaclesmatrix[positionY][positionX].cislo == Policko.krabica:
		return False
	if (positionX == aiX) and (positionY == aiY):  # ak stoji na bombe
		pass
	else:
		if obstaclesmatrix[positionY][positionX].cislo == Policko.bomba:
			return False
	if obstaclesmatrix[positionY][positionX].aiSeen == 'yes':
		return False

	if dangerCalculator(obstaclesmatrix, positionX, positionY) == False:
		return True
	elif (dangerCalculator(obstaclesmatrix, positionX, positionY) != False) and \
			(dangerCalculator(obstaclesmatrix, positionX, positionY) != True):
		print('nevratilo nic')

	obstaclesmatrix[positionY][positionX].aiSeen = 'yes'

	if dangerPathCalculator(obstaclesmatrix, positionX + 1, positionY, aiX, aiY, stats):
		if stats.lastPath != 'left':  # aby sa nevybral opacnym smerom akym zacal chodit( -> sa zasekne medzi 2 blockmi)
			stats.path = 'right'
			print('righttt')
			return True

	elif dangerPathCalculator(obstaclesmatrix, positionX, positionY + 1, aiX, aiY, stats):
		if stats.lastPath != 'up':
			stats.path = 'down'
			print('downnn')
			return True

	elif dangerPathCalculator(obstaclesmatrix, positionX - 1, positionY, aiX, aiY, stats):
		if stats.lastPath != 'right':
			stats.path = 'left'
			print('lefttt')
			return True

	elif dangerPathCalculator(obstaclesmatrix, positionX, positionY - 1, aiX, aiY, stats):
		if stats.lastPath != 'down':
			stats.path = 'up'
			print('upppp')
			return True


	return False


def A_get_h(start, goal):  # pocita heuristic distance = vzdialenost k cielu vzdusnou ciarou

	a = abs(goal[0] - start[0])
	b = abs(goal[1] - start[1])
	heuristic_distance = math.sqrt(a**2 + b**2)
	return heuristic_distance


	# A* algoritmus
def A(start, goal, matrix):  # start, goal = tuple - start[X, Y]
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
			print('mam ciel')
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

				if matrix[succ_coords[1]][succ_coords[0]].cislo == Policko.volne:
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
		#
		gut.reverse()
		print('gut')
		print(gut)
		gut.pop(0)
		print(gut)
		return gut


def move_podla_zoznamu(aiX, aiY, stats):
	zoznam = stats.current_target_powerup_list

	standing_onXY = zoznam[0][4]
	next_stepXY = zoznam[0][0]

	stats.current_target_powerup_list.pop(0)

	print('next step')
	print(next_stepXY)
	print('standing_onXY')
	print(standing_onXY)

	smer = [next_stepXY[0] - standing_onXY[0], next_stepXY[1] - standing_onXY[1]]
	print(smer)

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
	print(stats.path)















