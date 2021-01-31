from enum import IntEnum


class Policko(IntEnum):
	krabica = 0
	stena = 1
	volne = 2
	bomba = 3


upScore = 0  # na porovnavanie vhodnosti rekurzivnych ciest - dlzka ciest do vs. smerov
downScore = 0
leftScore = 0
rightScore = 0


def decisionMaker(obstaclesmatrix, positionY, positionX, stats, playersZoznam):

	if dangerCalculator(obstaclesmatrix, positionX, positionY):
		dangerPathCalculator(obstaclesmatrix, positionX, positionY, positionX, positionY, stats)
		for i in range(13):
			for e in range(15):
				obstaclesmatrix[i][e].aiSeen = 'no'
	else:
		nearest_target_rekurzivne_master(obstaclesmatrix, positionX, positionY, stats)

		nearest_powerup_rekurzivne_master(obstaclesmatrix, positionX, positionY, stats)
		for i in range(13):
			for e in range(15):
				obstaclesmatrix[i][e].aiSeen = 'no'


	return stats


def nearest_powerup_rekurzivne_master(obstaclesmatrix, aiX, aiY, stats):
	global upScore, downScore, rightScore, leftScore
	stats.path = 'none'
	upScore = 0
	downScore = 0
	leftScore = 0
	rightScore = 0

	if obstaclesmatrix[aiY - 1][aiX].cislo == 2:  # hore
		obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
		upScore = 0
		upScore = nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX, aiY - 1, stats, upScore)

		for i in range(13):
			for e in range(15):
				obstaclesmatrix[i][e].aiSeen = 'no'


	if 	obstaclesmatrix[aiY + 1][aiX].cislo == 2:  # dole
			obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
			downScore = 0
			downScore = nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX, aiY + 1, stats, downScore)

			for i in range(13):
				for e in range(15):
					obstaclesmatrix[i][e].aiSeen = 'no'

	if obstaclesmatrix[aiY][aiX + 1].cislo == 2:  # vpravo
			obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
			rightScore = 0
			rightScore = nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX + 1, aiY, stats, rightScore)

			for i in range(13):
				for e in range(15):
					obstaclesmatrix[i][e].aiSeen = 'no'

	if obstaclesmatrix[aiY][aiX - 1].cislo == 2:  # vlavo
			obstaclesmatrix[aiY][aiX].aiSeen = 'yes'
			leftScore = 0
			leftScore = nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX - 1, aiY, stats, leftScore)

			for i in range(13):
				for e in range(15):
					obstaclesmatrix[i][e].aiSeen = 'no'


	if (upScore == 0) and \
		(downScore == 0) and \
		(rightScore == 0) and \
		(leftScore == 0):
		return False
	else:
		zoznam = [upScore, downScore, rightScore, leftScore]
		min = 9999
		print(zoznam)
		print('^   v   >   <')
		for i in zoznam:
			if min > i and i > 0:
				min = i
		pozicia = zoznam.index(min)
		if pozicia == 0:
			stats.path = 'up'
		elif pozicia == 1:
			stats.path = 'down'
		elif pozicia == 2:
			stats.path = 'right'
		elif pozicia == 3:
			stats.path = 'left'
		else:
			stats.path = 'none'
		pozicia = 4
		dlzka = 999
	print(stats.path)


def nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX, aiY, stats, score):

	if obstaclesmatrix[aiY][aiX].cislo == Policko.stena:
		return 0
	if obstaclesmatrix[aiY][aiX].cislo == Policko.krabica:
		return 0
	if obstaclesmatrix[aiY][aiX].cislo == Policko.bomba:
		return 0
	if obstaclesmatrix[aiY][aiX].aiSeen == 'yes':
		return 0

	if obstaclesmatrix[aiY][aiX].powerup != '':
		return 1

	obstaclesmatrix[aiY][aiX].aiSeen = 'yes'

	seqX = [+1, +0, -1, +0]
	seqY = [+0, +1, +0, -1]

	for i in range(4):

		if (score := nearest_powerup_rekurzivne_slave(obstaclesmatrix, aiX + seqX[i], aiY + seqY[i], stats, score)) > 0:  # vpravo
			#print('score' + str(score))
			score += 1
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






