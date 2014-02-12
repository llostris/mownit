from random import randint, shuffle, sample
from copy import deepcopy
import operator
from simulated_annealing import simulated_annealing

class Sudoku(object):
    
    def __init__(self, filename=None) :
        if filename is None :
            self.data = [   [5,3,0,0,7,0,0,0,0],
                            [6,0,0,1,9,5,0,0,0],
                            [0,9,8,0,0,0,0,6,0],
                            [8,0,0,0,6,0,0,0,3],
                            [4,0,0,8,0,3,0,0,1],
                            [7,0,0,0,2,0,0,0,6],
                            [0,6,0,0,0,0,2,8,0],
                            [0,0,0,4,1,9,0,0,5],
                            [0,0,0,0,8,0,0,7,9] ]
        else :
            self.read_sudoku(filename)
            
        self.board = deepcopy(self.data)
        self.view_sudoku()
        self.fill_in()
        

    def read_sudoku(self, filename):        
        f = open(filename)
        lines = [line.strip() for line in f]
        f.close()
        board = []
        for line in lines :
            tmp = line.split()
            row = [ int(x) if x != 'x' else 0 for x in tmp]
            board.append(row)
        self.data = board;
        

    def fill_in(self) :
        """ Fills in empty places on board (those with 0 or x ), generating random first state """
        for i in range(9) :
            indices = get_square_indices(i)
            tmp = map(lambda x : self.data[x[0]][x[1]], indices)
            indices = filter(lambda x: self.data[x[0]][x[1]] == 0, indices)
            possibilities = [x for x in range(1, 10) if x not in tmp ]
            shuffle(possibilities)
            
            for ind, value in zip(indices, possibilities) :
                self.data[ind[0]][ind[1]] = value
                
    
    def view_sudoku(self) :
        """ Prints sudoku board """
        
        for i in range(9) :
            print self.data[i]
        print
        
        
    def solve(self, temp0):
        board = self.board
        s = self.data
        
        def proposal(s):
            return next_sudoku(s, board);
            
        [best_s, best_score] = simulated_annealing(s, temp0, cost, proposal, 0)
        return best_s, best_score        


def next_sudoku(s, board):    
    new_data = deepcopy(s)
    block = randint(0,8)
    indices = get_square_indices(block)
    indices = filter(lambda x: board[x[0]][x[1]] == 0, indices)
    numbers = len(indices)
    numbers_to_swap = sample(range(numbers),2)
    num1, num2 = [ indices[ind] for ind in numbers_to_swap ]
    new_data[num1[0]][num1[1]], new_data[num2[0]][num2[1]] = new_data[num2[0]][num2[1]], new_data[num1[0]][num1[1]]
    return new_data


def get_square_indices(k):
    # przesuniecie dla lewego gornego rogu k-ego kwadratu
    row_offset = k // 3
    col_offset = k % 3

    indices = [ ( 3 * row_offset + (j // 3) , 3 * col_offset + (j % 3) ) for j in range(9)]
    return indices


def cost(s):
    score = 0
    for i in range(9) :
        # Sumujemy w kolumnach
        column = map(operator.itemgetter(i), s)
        tmp = list(set(column))
        score += 9 - len(tmp)
        
        # Sumujemy w wierszach
        row = s[i];
        tmp = list(set(row))
        score += 9 - len(tmp)
        
    return score