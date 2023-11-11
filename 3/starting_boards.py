

public_1 = [("King", 'white', (7,7)),
            ("King", 'black', (0,0)),
            ("Rook", 'white', (6,1)),
            ("Rook", 'white', (5,1)),
            ("Rook", 'black', (6,5)),
            ("Rook", 'black', (6,6))]

'''
White wins in 3 moves
Best first move: ((5,1), (5,0))
'''


public_2 = [("King", 'white', (2,3)),
            ("King", 'black', (0,4)),
            ("Combatant", 'white', (1,4)),
            ("Combatant", 'white', (2,5)),
            ("Combatant", 'black', (7,0))]

'''
White wins in 5 moves
Best first move: ((2,3), (2,4))
'''

public_3 = [("King", 'white', (3,4)),
            ("King", 'black', (3,2)),
            ("Rook", "white", (2,4)),
            ("Rook", "white", (1,1)),
            ("Combatant", "white", (2,0)),
            ("Squire", "white", (1,0)),
            ("Rook", "black", (4,2)),
            ("Bishop", "black", (7,7)),
            ("Knight", "black", (2,2))]

'''
White wins in 5 moves
Best first move: ((2,4), (2,2))
'''

public_4 = [('King', 'white', (0, 5)), 
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

'''
White wins in 5 moves
Best first move: ((7,7), (7,2))
'''