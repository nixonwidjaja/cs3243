#public testcase 1: King capture in 3
p1 = [("King", 'white', (7,7)),
            ("King", 'black', (0,0)),
            ("Rook", 'white', (6,1)),
            ("Rook", 'white', (5,1)),
            ("Rook", 'black', (6,5)),
            ("Rook", 'black', (6,6))]
 
#Public testcase 2: King capture in 5
p2 = [("King", 'white', (2,3)),
          ("King", 'black', (0,4)),
          ("Combatant", 'white', (1,4)),
          ("Combatant", 'white', (2,5)),
          ("Combatant", 'black', (7,0))]
 
#Public testcase 3: King capture in 5
p3 = [("King", 'white', (3,4)),
          ("King", 'black', (3,2)),
          ("Rook", "white", (2,4)),
          ("Rook", "white", (1,1)),
          ("Combatant", "white", (2,0)),
          ("Squire", "white", (1,0)),
          ("Rook", "black", (4,2)),
          ("Bishop", "black", (7,7)),
          ("Knight", "black", (2,2))]
 
#Public testcase 4: King capture in 5
p4 = [('King', 'white', (0, 5)), 
      ('King', 'black', (7, 1)), 
      ('Rook', 'white', (7, 7)), 
      ('Squire', 'white', (5, 0)), 
      ('Knight', 'white', (6, 4)), 
      ('Squire', 'black', (7, 2)), 
      ('Bishop', 'black', (6, 3)), 
      ('Rook', 'black', (1, 7)), 
      ('Combatant', 'black', (6, 0)), 
      ('Combatant', 'black', (5, 1)), 
      ('Combatant', 'black', (6, 2))]

p5 = [('Knight', 'white', (7, 2)), ('Knight', 'black', (1, 6)), ('Combatant', 'white', (1, 5)), ('Combatant', 'black', (3, 3)), ('Combatant', 'white', (3, 0)), ('Combatant', 'black', (4, 3)), ('Combatant', 'white', (3, 1)), ('Combatant', 'black', (6, 4)), ('Combatant', 'white', (2, 1)), ('Combatant', 'black', (5, 5)), ('Bishop', 'white', (0, 5)), ('Bishop', 'black', (2, 4)), ('Squire', 'white', (3, 4)), ('Squire', 'white', (0, 2)), ('Squire', 'black', (7, 3)), ('Squire', 'black', (0, 7)), ('King', 'black', (0, 1)), ('King', 'white', (7, 7))]
p6=[('Rook', 'white', (7, 4)), ('Rook', 'black', (1, 5)), ('Knight', 'white', (1, 7)), ('Knight', 'black', (5, 3)), ('Knight', 'white', (6, 0)), ('Knight', 'black', (6, 7)), ('Combatant', 'white', (6, 6)), ('Combatant', 'black', (5, 7)), ('Combatant', 'white', (6, 2)), ('Combatant', 'black', (2, 1)), ('Combatant', 'white', (0, 3)), ('Combatant', 'black', (2, 4)), ('Combatant', 'white', (0, 6)), ('Combatant', 'black', (3, 3)), ('Bishop', 'white', (1, 4)), ('Bishop', 'white', (3, 5)), ('Bishop', 'black', (4, 7)), ('Bishop', 'black', (3, 1)), ('King', 'black', (0, 0)), ('King', 'white', (7, 7))]
p7=[('Rook', 'white', (2, 7)), ('Rook', 'black', (6, 1)), ('Knight', 'white', (7, 5)), ('Knight', 'black', (7, 7)), ('Knight', 'white', (5, 0)), ('Knight', 'black', (3, 6)), ('Combatant', 'white', (3, 2)), ('Combatant', 'black', (4, 5)), ('Combatant', 'white', (2, 0)), ('Combatant', 'black', (6, 4)), ('Combatant', 'white', (7, 4)), ('Combatant', 'black', (0, 5)), ('Combatant', 'white', (4, 4)), ('Combatant', 'black', (1, 7)), ('Bishop', 'white', (4, 6)), ('Bishop', 'black', (1, 6)), ('Squire', 'white', (1, 5)), ('Squire', 'black', (2, 5)), ('King', 'black', (0, 0)), ('King', 'white', (7, 6))]


def opponentAgent(gameboard):
    board = Board(gameboard)
    return ab(board, 3, 'B', -1e9, 1e9)[1]

def makeMove(gameboard, move):
    src, des = move
    ans = []
    for p, c, pos in gameboard:
        if pos == src:
            ans.append((p, c, des))
        elif pos == des:
            continue
        else:
            ans.append((p, c, pos))
    return ans

def isGameOver(gameboard):
    kings = 0
    other = 0
    for p, c, pos in gameboard:
        if p == 'King':
            kings += 1
        else:
            other += 1
    if other == 0 or kings < 2:
        return True
    return False

from timeit import default_timer as timer
gameboard = p7
total = 0
while True:
    start = timer()
    move = studentAgent(gameboard)
    end = timer()
    total += end - start
    print(end - start, total)
    gameboard = makeMove(gameboard, move)
    print(gameboard)
    if isGameOver(gameboard):
        break
    move = opponentAgent(gameboard)
    gameboard = makeMove(gameboard, move)
    if isGameOver(gameboard):
        break
# print(studentAgent(p1))
# print(studentAgent(p2))
# print(studentAgent(p3))
# print(studentAgent(p4))
# print(studentAgent(p6))