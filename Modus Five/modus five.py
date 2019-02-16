def GetBool(prompt):
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

def Initialize():
    global belligerent, warnings, log, playersNames, players, nextTeam, globalCounter, globalDict
    belligerent = [(1,1,1,1,1),(1,1,1,1,1)]
    warnings = [0,0]
    log = []
    playersNames = ['Player 1','Player 2']
    players = [False, False]
    nextTeam = {0:1, 1:0}
    globalCounter = 0
    globalDict = {}

def SetPlayersNames():
    buffer = input('Player 1\'s name? ')
    if (buffer != ''):
        playersNames[0] = buffer
    buffer = input('Player 2\'s name? ')
    if (buffer != ''):
        playersNames[1] = buffer

def SetNumberOfPlayers():
    if (GetBool(playersNames[0] + ' is a human player? ')):
        players[0] = True
    if (GetBool(playersNames[1] + ' is a human player? ')):
        players[1] = True

def BelligerentHP(localBelligerent, team):
    return sum(localBelligerent[team])

def FullAverage(localBelligerent, team):
    current_life = BelligerentHP(localBelligerent, team)
    if (current_life % 5 == 0):
        mean = int(current_life / 5)
        localBelligerent[team] = (mean, mean, mean, mean, mean)
    return localBelligerent

def LivelyAverage(localBelligerent, team):
    current_life = BelligerentHP(localBelligerent, team)
    if (current_life > 0):
        alive = 0
        for soldier in localBelligerent[team]:
            if (soldier != 0):
                alive += 1
        if (current_life % alive == 0):
            mean = int(current_life / alive)
            for soldier in localBelligerent[team]:
                if (soldier != 0):
                    soldier = mean
    return localBelligerent

def Attack(localBelligerent, attackerTeam, attackerSoldier, defenderSoldier):
    defenderTeam = nextTeam[attackerTeam]
    attackerHP = localBelligerent[defenderTeam][defenderSoldier]
    defenderHP = localBelligerent[attackerTeam][attackerSoldier]
    if (attackerSoldier >= 0 and attackerSoldier <= 4 and defenderSoldier >= 0 and defenderSoldier <= 4):
        if (attackerHP != 0 and defenderHP != 0):
            localBelligerent[defenderTeam] = localBelligerent[defenderTeam][:defenderSoldier] + ((attackerHP + defenderHP) % 5,) + localBelligerent[defenderTeam][defenderSoldier + 1:]
    return localBelligerent

def Register(data):
    log.append(data)

def Archive():
    print('\nLog:')
    file = open('modus-five.txt','a')
    file.write('New game:\n')
    file.write('Player 1\'s name: ' + playersNames[0] + '\n')
    file.write('Player 2\'s name: ' + playersNames[1] + '\n')
    for i in range(len(log)):
        print('Turn ' + str(log[i][0]) + ' (player ' + str(log[i][1] + 1) + '\'s turn): ' + str(log[i][2:]))
        file.write('Turn ' + str(log[i][0]) + ' (player ' + str(log[i][1] + 1) + '\'s turn): ' + str(log[i][2:]) + '\n')
    file.write('Game over.\n\n')
    file.close()
    file = open('modus-five-dict.txt','w')
    for key in sorted(globalDict):
        file.write(str(key[0]) + ' ' + str(key[1]) + ' ' + str(globalDict[key]) + '\n')
    file.close()

def IsDraw(current_turn):
    draw_log = {}
    for size in range(1, 1 + int((current_turn + 1) / 6), 1):
        for i in range(0,6,2):
            slicer = slice(current_turn + 1 - size * (i + 2), current_turn - size * i, 2)
            item = log[slicer]
            key = []
            for line in item:
                key += [tuple(tuple(line[3][0]) + tuple(line[3][1]))]
            key = tuple(key)
            if (key in draw_log):
                draw_log[key] += 1
            else:
                draw_log[key] = 1
            if (draw_log[key] >= 3):
                return 1
    return 0

def Evaluate(localBelligerent, attackerTeam):
    defenderTeam = nextTeam[attackerTeam]
    value = 0
    for soldier in localBelligerent[attackerTeam]:
        if (soldier == 0):
            value -= 5
    for soldier in localBelligerent[defenderTeam]:
        if (soldier == 0):
            value += 5
    value += len(set(localBelligerent[attackerTeam]))
    value -= len(set(localBelligerent[defenderTeam]))
    return value

def DifferentSoldiers(localBelligerent, team):
    differentSoldiers = []
    for soldierHP in set(localBelligerent[team]):
        for soldierName in range(5):
            if soldierHP != 0 and localBelligerent[team][soldierName] == soldierHP:
                differentSoldiers.append(soldierName)
                break
    return differentSoldiers



def ArtificalIntelligence(localBelligerent, attackerTeam, depth):
    defenderTeam = nextTeam[attackerTeam]
    move, attacker, defender = 0, -1, -1
    key = (tuple(sorted(localBelligerent[attackerTeam])), tuple(sorted(localBelligerent[defenderTeam])))
    if (BelligerentHP(localBelligerent, attackerTeam) == 0):
        globalDict[key] = (-100, depth)
        return 0, -1, -1, -100
    elif (BelligerentHP(localBelligerent, defenderTeam) == 0):
        globalDict[key] = (100, depth)
        return 0, -1, -1, 100
    elif (depth <= 0):
        return 0, -1, -1, Evaluate(localBelligerent, attackerTeam)
    value = -100
    differentAttackerSoldiers = DifferentSoldiers(localBelligerent, attackerTeam)
    differentDefenderSoldiers = DifferentSoldiers(localBelligerent, defenderTeam)
    for moveBuffer in range(3):
        if (moveBuffer == 0):
            for attackerBuffer in differentAttackerSoldiers:
                for defenderBuffer in differentDefenderSoldiers:
                    localBelligerentBuffer = list(localBelligerent)
                    localBelligerentBuffer = Attack(localBelligerentBuffer, attackerTeam, attackerBuffer, defenderBuffer)
                    if (localBelligerent != localBelligerentBuffer):
                        keyBuffer = (tuple(sorted(localBelligerentBuffer[defenderTeam])), tuple(sorted(localBelligerentBuffer[attackerTeam])))
                        if (keyBuffer in globalDict and globalDict[keyBuffer][1] >= depth - 1):
                            valueBuffer = -globalDict[keyBuffer][0]
                        else:
                            valueBuffer = -ArtificalIntelligence(localBelligerentBuffer, defenderTeam, depth - 1)[3]
                        if (valueBuffer == 100):
                            return moveBuffer, attackerBuffer, defenderBuffer, 100
                        if (valueBuffer >= value):
                            move, attacker, defender, value = moveBuffer, attackerBuffer, defenderBuffer, valueBuffer
        else:
            localBelligerentBuffer = list(localBelligerent)
            if (moveBuffer == 1):
                localBelligerentBuffer = FullAverage(localBelligerentBuffer, 1)
            else:
                localBelligerentBuffer = LivelyAverage(localBelligerentBuffer, 1)
            if (localBelligerent != localBelligerentBuffer):
                keyBuffer = (tuple(sorted(localBelligerentBuffer[defenderTeam])), tuple(sorted(localBelligerentBuffer[attackerTeam])))
                if (keyBuffer in globalDict and globalDict[keyBuffer][1] >= depth - 1):
                    valueBuffer = -globalDict[keyBuffer][0]
                else:
                    valueBuffer = -ArtificalIntelligence(localBelligerentBuffer, defenderTeam, depth - 1)[3]
                if (valueBuffer == 100):
                    return moveBuffer, -1, -1, 100
                if (valueBuffer >= value):
                    move, attacker, defender, value = moveBuffer, -1, -1, valueBuffer
    globalDict[key] = (value, depth)
    return move, attacker, defender, value

def Turn(current_turn, team):
    backup = list(belligerent)
    move, attacker, defender, value = ArtificalIntelligence(belligerent, team, 50)
    print('\nTurn ' + str(current_turn) + ' | ' + str(value) + ' | ' + str(len(globalDict)))
    print(playersNames[team] + '\'s time:')
    if (players[team]):
        move = int(input('Your move? '))
        if (move == 0):
            attacker = int(input('Your attacker? ')) - 1
            defender = int(input(playersNames[nextTeam[team]] + '\'s defender? ')) - 1
    else:
        print('Your move? ' + str(move))
        if (move == 0):
            print('Your attacker? ' + str(attacker + 1))
            print(playersNames[nextTeam[team]] + '\'s defender? ' + str(defender + 1))
    if (move == 0):
        Attack(belligerent, team, attacker, defender)
        move = (move, attacker, defender)
    elif (move == 1):
        FullAverage(belligerent, team)
    elif (move == 2):
        LivelyAverage(belligerent, team)
    Register((current_turn, team, move, backup))
    if (belligerent == backup):
        print(belligerent)
        warnings[team] += 1
        log.pop()
        print('Player ' + str(team + 1) + '\'s warning number [' + str(warnings[team]) + '/3].')
        if (warnings[team] < 3):
            Turn(current_turn, team)
        else:
            Register((current_turn, team, 3, backup))
            print('\nPlayer ' + str(nextTeam[team] + 1) + ' won!')
            print('Game over.')
            return log
    elif (BelligerentHP(belligerent, nextTeam[team]) == 0):
        print('\n' + playersNames[team] + ' won!')
        print('Game over.')
        return log
    elif (IsDraw(current_turn)):
        print('\nDraw! No one won.')
        print('Game over.')
        return log
    else:
        print(belligerent)
        Turn(current_turn + 1, nextTeam[team])

def Game():
    Initialize()
    print('Turn 0')
    SetPlayersNames()
    SetNumberOfPlayers()
    print(belligerent)
    Turn(1, 0)
    Archive()
    print('\n')
    Game()

print('Currently, move 0 is to attack, move 1 is to Full Average and move 2 is to Lively Average.\nYour soldiers are labeled from 1 to 5.\n')
Game()
