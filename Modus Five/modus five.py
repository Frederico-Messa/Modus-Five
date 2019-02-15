def Initialize():
    global belligerent, warnings, log, playersNames, players
    belligerent = [(1,1,1,1,1),(1,1,1,1,1)]
    warnings = [0,0]
    log = []
    playersNames = ['Player 1','Player 2']
    players = [True, True]

def SetPlayersNames():
    global playersNames
    buffer = input('Player 1\'s name? ')
    if (buffer != ''):
        playersNames[0] = buffer
    buffer = input('Player 2\'s name? ')
    if (buffer != ''):
        playersNames[1] = buffer

def SetNumberOfPlayers():
    global players

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
    defenderTeam = (attackerTeam + 1) % 2
    attackerHP = localBelligerent[defenderTeam][defenderSoldier - 1]
    defenderHP = localBelligerent[attackerTeam][attackerSoldier - 1]
    if (attackerSoldier >= 1 and attackerSoldier <= 5 and defenderSoldier >= 1 and defenderSoldier <= 5):
        if (attackerHP != 0 and defenderHP != 0):
            localBelligerent[defenderTeam] = localBelligerent[defenderTeam][:defenderSoldier - 1] + ((attackerHP + defenderHP) % 5,) + localBelligerent[defenderTeam][defenderSoldier:]
    return localBelligerent

def Register(data):
    global log
    log += [data]

def Archive():
    global log, playersNames
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

def IsDraw(current_turn):
    global log
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

def Evaluate(localBelligerent):
    value = 0
    for soldier in localBelligerent[0]:
        if (soldier == 0):
            value -= 5
    for soldier in localBelligerent[1]:
        if (soldier == 0):
            value += 5
    value += len(set(localBelligerent[0]))
    value -= len(set(localBelligerent[1]))
    return value

def ArtificalIntelligence(localBelligerent, team, depth):
    if (team == 1):
        signal = 1
    else:
        signal = -1
    move0, attacker0, deffender0 = 0, 0, 0
    value0 = -float('inf')
    for move1 in range(3):
        if (move1 == 0):
            for attacker1 in range(1,6):
                for deffender1 in range(1,6):
                    soldiers1 = list(localBelligerent)
                    soldiers1 = Attack(soldiers1, team, attacker1, deffender1)
                    if (belligerent != soldiers1):
                        value1 = float('inf')
                        for move2 in range(3):
                            if (move2 == 0):
                                for attacker2 in range(1,6):
                                    for deffender2 in range(1,6):
                                        soldiers2 = list(soldiers1)
                                        soldiers2 = Attack(soldiers2, (team + 1) % 2, attacker2, deffender2)
                                        if (soldiers1 != soldiers2):
                                            if (depth <= 1):
                                                value2 = signal * Evaluate(soldiers2)
                                            else:
                                                value2 = ArtificalIntelligence(soldiers2, team, depth - 1)[3]
                                            if (value2 < value1):
                                                value1 = value2
                            else:
                                soldiers2 = list(soldiers1)
                                if (move2 == 1):
                                    soldiers2 = FullAverage(soldiers2, 1)
                                elif (move2 == 2):
                                    soldiers2 = LivelyAverage(soldiers2, 1)
                                if (soldiers1 != soldiers2):
                                    if (depth <= 1):
                                        value2 = signal * Evaluate(soldiers2)
                                    else:
                                        value2 = ArtificalIntelligence(soldiers2, team, depth - 1)[3]
                                    if (value2 < value1):
                                        value1 = value2
                        if (value1 > value0):
                            value0, move0, attacker0, deffender0 = value1, move1, attacker1, deffender1
        else:
            soldiers1 = list(localBelligerent)
            if (move1 == 1):
                soldiers1 = FullAverage(soldiers1, 1)
            elif (move1 == 2):
                soldiers1 = LivelyAverage(soldiers1, 1)
            if (localBelligerent != soldiers1):
                value1 = float('inf')
                for move2 in range(3):
                    if (move2 == 0):
                        for attacker2 in range(1,6):
                            for deffender2 in range(1,6):
                                soldiers2 = list(soldiers1)
                                soldiers2 = Attack(soldiers2, (team + 1) % 2, attacker2, deffender2)
                                if (soldiers1 != soldiers2):
                                    if (depth <= 1):
                                        value2 = signal * Evaluate(soldiers2)
                                    else:
                                        value2 = ArtificalIntelligence(soldiers2, team, depth - 1)[3]
                                    if (value2 < value1):
                                        value1 = value2
                    else:
                        soldiers2 = list(soldiers1)
                        if (move2 == 1):
                            soldiers2 = FullAverage(soldiers2, 1)
                        elif (move2 == 2):
                            soldiers2 = LivelyAverage(soldiers2, 1)
                        if (soldiers1 != soldiers2):
                            if (depth <= 1):
                                value2 = signal * Evaluate(soldiers2)
                            else:
                                value2 = ArtificalIntelligence(soldiers2, team, depth - 1)[3]
                            if (value2 < value1):
                                value1 = value2
                if (value1 > value0):
                    value0, move0, attacker0, deffender0 = value1, move1, attacker1, deffender1
    return move0, attacker0, deffender0, value0

def Turn(current_turn, team):
    global belligerent, warnings, log, playersNames, players
    backup = list(belligerent)
    move, attacker, deffender, value = ArtificalIntelligence(belligerent[:], team, 2)
    print('\nTurn ' + str(current_turn) + ' | ' + str(value))
    print(playersNames[team] + '\'s time:')
    if (players[team]):
        move = int(input('Your move?  '))
        if (move == 0):
            attacker = int(input('Your attacker?  '))
            deffender = int(input(playersNames[(team + 1) % 2] + '\'s deffender?  '))
    if (move == 0):
        Attack(belligerent, team, attacker, deffender)
        move = (move, attacker, deffender)
    if (move == 1):
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
            print('\nPlayer ' + str((team + 1) % 2 + 1) + ' won!')
            print('Game over.')
            return log
    elif (BelligerentHP(belligerent, (team + 1) % 2) == 0):
        print('\nPlayer ' + str(team + 1) + ' won!')
        print('Game over.')
        return log
    elif (IsDraw(current_turn)):
        print('\nDraw! No one won.')
        print('Game over.')
        return log
    else:
        print(belligerent)
        Turn(current_turn + 1, (team + 1) % 2)

def Game():
    global belligerent
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
