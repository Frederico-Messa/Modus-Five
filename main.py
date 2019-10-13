from time import time

def initialize():
	global log, globalDict, numberOfPlayers, nextPlayer, playersNames, playersHumanity, warnings, belligerents, currentTurn, currentPlayer, deepest
	log = list()
	globalDict = dict()
	numberOfPlayers = setNumberOfPlayers()
	nextPlayer = setNextPlayer()
	playersNames = setPlayersNames()
	playersHumanity = setHumanPlayers()
	warnings = setWarnings()
	belligerents = setBelligerents()
	currentTurn = 1
	currentPlayer = 0
	deepest = 0

def deletePlayer(player):
	global numberOfPlayers, nextPlayer, playersNames, playersHumanity, warnings, belligerents
	numberOfPlayers -= 1
	nextPlayer[numberOfPlayers - 1] = 0
	#nextPlayer.pop(numberOfPlayers)
	playersNames.pop(player)
	playersHumanity.pop(player)
	warnings.pop(player)
	belligerents.pop(player)

def getBool(prompt):
	while True:
		try:
		   return {'true':True,
				   't':True,
				   'false':False,
				   'f':False,
				   'yes':True,
				   'y':True,
				   'no':False,
				   'n':False
				   }[input(prompt).lower()]
		except KeyError:
		   print('Invalid input please enter Yes or No!')

def setNumberOfPlayers():
	buffer = input('Number of players? (press Enter for default) ')
	if (buffer != ''):
		numberOfPlayers = int(buffer)
	else:
		numberOfPlayers = 2
		print('Default selected: 2 players')
	return numberOfPlayers

def setPlayersNames():
	playersNames = list()
	for player in range(numberOfPlayers):
		buffer = input('Player ' + str(player + 1) + '\'s name? ')
		if (buffer != ''):
			playersNames.append(buffer)
		else:
			playersNames.append('Player ' + str(player + 1))
	return playersNames

def setHumanPlayers():
	playersHumanity = list()
	for player in range(numberOfPlayers):
		if (getBool(playersNames[player] + ' is a human player? ')):
			playersHumanity.append(True)
		else:
			playersHumanity.append(False)
	return playersHumanity

def setNextPlayer():
	nextPlayer = dict()
	for player in range(numberOfPlayers):
		if (player + 1 != numberOfPlayers):
			nextPlayer[player] = player + 1
		else:
			nextPlayer[player] = 0
	return nextPlayer

def setWarnings():
	warnings = [0] * numberOfPlayers
	return warnings

def setBelligerents():
	belligerents = [(1,1,1,1,1)] * numberOfPlayers
	return belligerents

def belligerentHP(localBelligerents, team):
	localBelligerents = list(localBelligerents)
	return sum(localBelligerents[team])

def tryFullAverage(localBelligerents, team):
	localBelligerents = list(localBelligerents)
	current_life = belligerentHP(localBelligerents, team)
	differentAliveSoldiersSet = differentAliveSoldiers(localBelligerents, team)
	if (len(differentAliveSoldiersSet) > 1 and current_life % 5 == 0):
		return True
	else:
		return False

def fullAverage(localBelligerents, team):
	localBelligerents = list(localBelligerents)
	current_life = belligerentHP(localBelligerents, team)
	if (tryFullAverage(localBelligerents, team)):
		mean = int(current_life / 5)
		localBelligerents[team] = (mean, mean, mean, mean, mean)
	return localBelligerents

def tryLivelyAverage(localBelligerents, team):
	localBelligerents = list(localBelligerents)
	current_life = belligerentHP(localBelligerents, team)
	aliveSoldiersSet = aliveSoldiers(localBelligerents, team)
	differentAliveSoldiersSet = differentAliveSoldiers(localBelligerents, team)
	if (len(differentAliveSoldiersSet) > 1 and current_life % len(aliveSoldiersSet) == 0):
		return True
	else:
		return False

def livelyAverage(localBelligerents, team):
	localBelligerents = list(localBelligerents)
	current_life = belligerentHP(localBelligerents, team)
	aliveSoldiersSet = aliveSoldiers(localBelligerents, team)
	if (tryLivelyAverage(localBelligerents, team)):
		mean = int(current_life / len(aliveSoldiersSet))
		for soldier in aliveSoldiersSet:
			localBelligerents[team] = localBelligerents[team][:soldier] + (mean,) + localBelligerents[team][soldier + 1:]
	return localBelligerents

def tryAttack(localBelligerents, attackerTeam, attackerSoldier, defenderSoldier):
	localBelligerents = list(localBelligerents)
	defenderTeam = nextPlayer[attackerTeam]
	if (attackerSoldier >= 0 and attackerSoldier <= 4 and defenderSoldier >= 0 and defenderSoldier <= 4 and localBelligerents[attackerTeam][attackerSoldier] != 0 and localBelligerents[defenderTeam][defenderSoldier] != 0):
		return True
	else:
		return False

def attack(localBelligerents, attackerTeam, attackerSoldier, defenderSoldier):
	localBelligerents = list(localBelligerents)
	defenderTeam = nextPlayer[attackerTeam]
	attackerHP = localBelligerents[defenderTeam][defenderSoldier]
	defenderHP = localBelligerents[attackerTeam][attackerSoldier]
	if (tryAttack(localBelligerents, attackerTeam, attackerSoldier, defenderSoldier)):
		localBelligerents[defenderTeam] = localBelligerents[defenderTeam][:defenderSoldier] + ((attackerHP + defenderHP) % 5,) + localBelligerents[defenderTeam][defenderSoldier + 1:]
	return localBelligerents

def archive(localPlayersNames):
	print('\nLog:')
	file = open('modus-five.txt','a')
	file.write('New game:\n')
	for playerName in localPlayersNames:
		file.write('Player 1\'s name: ' + playerName + '\n')
	for i in range(len(log)):
		print('Turn ' + str(log[i][0]) + ' (player ' + str(log[i][1] + 1) + '\'s turn): ' + str(log[i][2:]))
		file.write('Turn ' + str(log[i][0]) + ' (player ' + str(log[i][1] + 1) + '\'s turn): ' + str(log[i][2:]) + '\n')
	file.write('Game over.\n\n')
	file.close()
	file = open('modus-five-dict.txt','w')
	for key in sorted(globalDict):
		file.write(str(key[0]) + ' ' + str(key[1]) + ' ' + str(globalDict[key]) + '\n')
	file.close()

def isDraw(currentTurnLocal):
	draw_log = {}
	for size in range(1, 1 + int((currentTurnLocal + 1) / (numberOfPlayers * 3)), 1):
		for i in range(0, 6, numberOfPlayers):
			slicer = slice(currentTurnLocal - size * (i + 1) - 1, currentTurnLocal - size * i, numberOfPlayers)
			item = log[slicer]
			key = list()
			for line in item:
				key += [tuple(line[2])]
			key = tuple(key)
			if (key in draw_log):
				draw_log[key] += 1
			else:
				draw_log[key] = 1
			if (draw_log[key] >= 3):
				return 1
	return 0

def evaluate(localBelligerents, attackerTeam):
	localBelligerents = list(localBelligerents)
	value = 0
	for player in range(numberOfPlayers):
		for soldier in localBelligerents[player]:
			if (soldier == 0):
				if (player == attackerTeam):
					value += 5
				else:
					value -= 5 / (numberOfPlayers - 1)
		if (player == attackerTeam):
			value += len(set(localBelligerents[player]))
		else:
			value -= len(set(localBelligerents[player])) / (numberOfPlayers - 1)
	return value

def aliveSoldiers(localBelligerents, team):
	localBelligerents = list(localBelligerents)
	AliveSoldiers = set()
	for soldier in range(5):
		if (localBelligerents[team][soldier] != 0):
			AliveSoldiers.add(soldier)
	return AliveSoldiers

def differentAliveSoldiers(localBelligerents, team):
	localBelligerents = list(localBelligerents)
	aliveSoldiersSet = aliveSoldiers(localBelligerents, team)
	differentAliveSoldiers = set()
	differentSoldiersHPs = set()
	for soldier in aliveSoldiersSet:
		if (not (localBelligerents[team][soldier] in differentSoldiersHPs)):
			differentSoldiersHPs.add(localBelligerents[team][soldier])
			differentAliveSoldiers.add(soldier)
	return differentAliveSoldiers

def tryAllMovements(localBelligerents, attackerTeam):
	localBelligerents = list(localBelligerents)
	allMovements = dict()
	defenderTeam = nextPlayer[attackerTeam]
	differentAttackerSoldiers = differentAliveSoldiers(localBelligerents, attackerTeam)
	differentDefenderSoldiers = differentAliveSoldiers(localBelligerents, defenderTeam)
	for attackerBuffer in differentAttackerSoldiers:
		for defenderBuffer in differentDefenderSoldiers:
			allMovements[(0, attackerBuffer, defenderBuffer)] = attack(localBelligerents, attackerTeam, attackerBuffer, defenderBuffer)
	if (tryFullAverage(localBelligerents, attackerTeam)):
		allMovements[1] = fullAverage(localBelligerents, attackerTeam)
	if (tryLivelyAverage(localBelligerents, attackerTeam)):
		allMovements[2] = livelyAverage(localBelligerents, attackerTeam)
	return allMovements

def artificalIntelligence(localBelligerents, attackerTeam, depth):
	localBelligerents = list(localBelligerents)
	defenderTeam = nextPlayer[attackerTeam]
	movement = 3
	key = (tuple(sorted(localBelligerents[attackerTeam])), tuple(sorted(localBelligerents[defenderTeam])))
	if (belligerentHP(localBelligerents, attackerTeam) == 0):
		globalDict[key] = (float('-inf'), depth)
		return 3, float('-inf')
	elif (belligerentHP(localBelligerents, defenderTeam) == 0):
		globalDict[key] = (float('inf'), depth)
		return 3, float('inf')
	elif (depth <= 0):
		return 3, evaluate(localBelligerents, attackerTeam)
	value = float('-inf')
	allMovements = tryAllMovements(localBelligerents, attackerTeam)
	for movementBuffer in allMovements.keys():
		localBelligerentsBuffer = allMovements[movementBuffer]
		keyBuffer = (tuple(sorted(localBelligerentsBuffer[defenderTeam])),
					tuple(sorted(localBelligerentsBuffer[attackerTeam])))
		if (keyBuffer in globalDict and globalDict[keyBuffer][1] >= depth - 1):
			valueBuffer = -globalDict[keyBuffer][0]
		else:
			valueBuffer = -artificalIntelligence(localBelligerentsBuffer, defenderTeam, depth - 1)[1]
		if (valueBuffer == float('inf')):
			return movementBuffer, float('inf')
		if (valueBuffer >= value):
			movement, value = movementBuffer, valueBuffer
	globalDict[key] = (value, depth)
	return movement, value

def printBelligerents(localBelligerents):
	localBelligerents = list(belligerents)
	print('')
	for player in range(numberOfPlayers):
		print(playersNames[player] + '\'s belligerent: ' + str(localBelligerents[player]))

def turn():
	global belligerents, deepest
	warning = False
	localBelligerents = list(belligerents)
	print('\nTurn ' + str(currentTurn) + '\n' + playersNames[currentPlayer] + '\'s turn:')
	if (playersHumanity[currentPlayer]):
		move = int(input('Your move? '))
		if (move == 0):
			attacker = int(input('Your attacker? ')) - 1
			defender = int(input(playersNames[nextPlayer[currentPlayer]] + '\'s defender? ')) - 1
			belligerents = attack(belligerents, currentPlayer, attacker, defender)
			move = (move, attacker, defender)
	else:
		then = time()
		while True:
			move, value = artificalIntelligence(belligerents, currentPlayer, deepest)
			now = time()
			ellapsedTime = now - then
			if (ellapsedTime > 1):
				break
			else:
				deepest += 1
		print('Advantage: ' + str(value) + ' | Depth: ' + str(deepest))
		if (type(move) is tuple):
			print('Your move? ' + str(move[0]))
			print('Your attacker? ' + str(move[1] + 1))
			print(playersNames[nextPlayer[currentPlayer]] + '\'s defender? ' + str(move[2] + 1))
			belligerents = attack(belligerents, currentPlayer, move[1], move[2])
		else:
			print('Your move? ' + str(move))
	if (move == 1):
		belligerents = fullAverage(belligerents, currentPlayer)
	elif (move == 2):
		belligerents = livelyAverage(belligerents, currentPlayer)
	if (belligerents == localBelligerents):
		move = 3
		belligerents = localBelligerents
		warnings[currentPlayer] += 1
		print('Player ' + str(currentPlayer + 1) + '\'s warning number [' + str(warnings[currentPlayer]) + '/3].')
		warning = True
	printBelligerents(belligerents)
	log.append((currentTurn, currentPlayer, localBelligerents, move))
	if (isDraw(currentTurn)):
		print('\nDraw! No one won.')
		print('Game over.')
		return 'Threefold repetition'
	elif (belligerentHP(belligerents, nextPlayer[currentPlayer]) == 0):
		deletePlayer(nextPlayer[currentPlayer])
		if (numberOfPlayers == 1):
			print('\n' + playersNames[0] + ' won!')
			print('Game over.')
			return 'Checkmate'
	elif (warnings[currentPlayer] == 3):
		deletePlayer(currentPlayer)
		if (numberOfPlayers == 1):
			print('\n' + playersNames[0] + ' won!')
			print('Game over.')
			return 'Threefold warnings'
	elif (warning == True):
		return turn()
	return ''

def game():
	global currentPlayer, currentTurn
	initialize()
	localPlayersNames = list(playersNames)
	print('\nTurn 0')
	printBelligerents(belligerents)
	condition = ''
	while (condition == ''):
		condition = turn()
		currentPlayer = nextPlayer[currentPlayer]
		currentTurn += 1
	archive(localPlayersNames)
	print('\n')

print('Currently, move 0 is to attack, move 1 is to Full Average and move 2 is to Lively Average.\nYour soldiers are labeled from 1 to 5.\n')
game()
while getBool('Play again? '):
	game()
