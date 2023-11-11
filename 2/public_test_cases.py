
##Project 2.1 (CSP Implementation)
public_1 = {
    'domains' : {
        "A" : [1,2,3,4,5],
        "B" : [2,3,4,5,6],
        "C" : [3,4,5,6,7],
        "D" : [5,7,9,11,13]
    },
    'constraints' : {
        ("A", "B") : lambda a, b : a + b == 8 and a >= b,
        ("B", "C") : lambda b, c : b <= c / 2,
        ("C", "D") : lambda c, d : (c + d) % 2 == 0
    }
}
"""
Possible solution: 
{'A': 5, 'B': 3, 'C': 7, 'D': 13}
"""

public_2 = {
    'domains' : {
        "A" : [1,2,3,4,5,6,7,8,9,10],
        "B" : [1,2,3,4,5,6,7,8,9,10],
        "C" : [1,2,3,4,5,6,7,8,9,10],
        "D" : [1,2,3,4,5,6,7,8,9,10]
    },
    'constraints' : {
        ("A", "B") : lambda a, b : a * b < 50,
        ("A", "C") : lambda a, c : (a + c) % 10 == 0,
        ("A", "D") : lambda a, d : a + d > 10,
        ("B", "C") : lambda b, c : b > c // 3 and b < c,
        ("B", "D") : lambda b, d : (b + d) % 2 == 1,
        ("C", "D") : lambda c, d : (c % d) == 0 and c != d
    }
}
"""
Possible solution:
{'A': 10, 'B': 4, 'C': 10, 'D': 1} OR
{'A': 10, 'B': 4, 'C': 10, 'D': 5}
"""


##Project 2.2 (Local search)
public_1 = {
    'width' : 8,
    'height' : 8,
    'input_squares' : {
        2 : 12,
        4 : 1
    }
}
'''
Possible solution:
[(2, 6, 6), (2, 6, 0), (2, 0, 2), (2, 2, 2), (2, 6, 4), (2, 6, 2), (4, 0, 4), (2, 0, 0), (2, 2, 0), (2, 4, 6), (2, 4, 4), (2, 4, 2), (2, 4, 0)]
'''

public_2 = {
    'width' : 9,
    'height' : 9,
    'input_squares' : {
        5 : 1,
        4 : 2,
        3 : 1,
        2 : 3,
        1 : 3
    }
}
'''
Possible solution:
[(5, 4, 0), (4, 5, 5), (4, 0, 0), (2, 0, 4), (2, 2, 4), (3, 0, 6), (2, 3, 6), (1, 3, 8), (1, 4, 5), (1, 4, 8)]
'''


##Project 2.2 (CSP)
public_1 = {
    'cols' : 8,
    'rows' : 4,
    'input_squares' : {
        1 : 5,
        2 : 2,
        4 : 1
    },
    'obstacles' : [(3,0), (1,2), (3,7)]
}
'''
Possible solution:
[(1, 0, 2), (1, 0, 7), (1, 1, 7), (1, 2, 0), (1, 2, 7), (2, 0, 0), (2, 2, 1), (4, 0, 3)]
'''

public_2 = {
    'cols' : 8,
    'rows' : 8,
    'input_squares' : {
        2 : 7,
        3 : 4
    },
    'obstacles' : []
}
'''
Possible solution:
[(2, 0, 6), (2, 2, 6), (2, 4, 6), (2, 6, 0), (2, 6, 2), (2, 6, 4), (2, 6, 6), (3, 0, 0), (3, 0, 3), (3, 3, 0), (3, 3, 3)]
'''

public_3 = {
    'cols' : 8,
    'rows' : 8,
    'input_squares' : {
        2 : 6,
        6 : 1,
        1 : 3
    },
    'obstacles' : [(0,0)]
}

'''
Possible solution:
[(2, 1, 0), (2, 3, 0), (2, 5, 0), (2, 6, 2), (2, 6, 4), (2, 6, 6), (6, 0, 2), (1, 0, 1), (1, 7, 0), (1, 7, 1)]
'''