import sudoku
import sys

if len(sys.argv) > 0 :
    filename = sys.argv[1]
else :
    filename = ''

my_sudoku = sudoku.Sudoku(filename)

[ best_s, best_cost] = my_sudoku.solve(10)
my_sudoku.data = best_s 
print 
my_sudoku.view_sudoku()