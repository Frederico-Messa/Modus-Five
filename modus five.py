def initialize():
    return [[[1,1,1,1,1],[1,1,1,1,1]], [0,0], []]

def life(soldiers, team):
    return sum(soldiers[team % 2])

def MT(soldiers, team):
    current_life = life(soldiers, team)
    if (current_life % 5 == 0):
        mean = int(current_life / 5)
        soldiers[team] = [mean for i in range (5)]
    return soldiers

def MA(soldiers, team):
    alive = 0
    for i in range(5):
        if (soldiers[team][i] != 0):
            alive += 1
    current_life = life(soldiers, team)
    if (current_life % alive == 0):
        mean = int(current_life / alive)
        for i in range(5):
            if (soldiers[team][i] != 0):
                soldiers[team][i] = mean
    return soldiers

def attack(soldiers, team, attacker, deffender):
    if (soldiers[(team + 1) % 2][deffender - 1] != 0 and soldiers[team][attacker - 1] != 0):
        soldiers[(team + 1) % 2][deffender - 1] += soldiers[team][attacker - 1]
        soldiers[(team + 1) % 2][deffender - 1] %= 5
    return soldiers

def save(soldiers):
    backup = [[],[]]
    for i in range(2):
        backup[i] += soldiers[i]
    return backup

def register(log, move):
    log += [move]
    return log

def turn(current_turn, team, soldiers, warnings, log):
    print('\nTurn ' + str(current_turn))
    print('Player ' + str(team + 1) + '\'s time:')
    backup = save(soldiers)
    move = int(input('Your move? '))
    if (move == 0):
        attacker = int(input('Your attacker? '))
        deffender = int(input('Opponent deffender? '))
        attack(soldiers, team, attacker, deffender)
        register(log, [current_turn, team, [move, attacker, deffender]])
    elif (move == 1):
        MT(soldiers, team)
        register(log, [current_turn, team, [move]])
    elif (move == 2):
        MA(soldiers, team)
        register(log, [current_turn, team, [move]])
    if (soldiers == backup):
        print(soldiers)
        warnings[team] += 1
        log.pop()
        print('Player ' + str(team + 1) + '\'s warning number [' + str(warnings[team]) + '/3].')
        if (warnings[team] < 3):
            turn(current_turn, team, soldiers, warnings, log)
        else:
            print('\nPlayer ' + str((team + 1) % 2 + 1) + ' won!')
            print('Game over.')
            print(log)
    elif (life(soldiers, (team + 1) % 2) != 0):
        print(soldiers)
        turn(current_turn + 1, (team + 1) % 2, soldiers, warnings, log)
    else:
        print('\nPlayer ' + str(team + 1) + ' won!')
        print('Game over.')
        print(log)
    

def game():
    print('Currently, move 0 is to attack, move 1 is to MT and move 2 is to MA.\nYour soldiers are labeled from 1 to 5.\n') 
    initial = initialize()
    soldiers = initial[0]
    warnings = initial[1]
    log = initial[2]
    print('Turn 0')
    print(soldiers)
    turn(1, 0, soldiers, warnings, log)
    print('\n')
    game()

game()
