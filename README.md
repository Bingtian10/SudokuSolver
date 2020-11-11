# A simple 9x9 Sudoku board solver
Given a nxn sudoku board, we can use backtrack/depth first search to recursively search for
all possible solution. Here I used 9x9 as an example for convenience, as the algorithm runtime
grow exponentially with larger board.

Here I include the solveer logic in Java, Python and make a GUI program in python.

# Prerequisite
To run the python program, make sure you install pygame in your local environment
```
python3 -m pip install -U pygame --user
```
To see if pygame is installed successfully, run the example alien game in following:
```
python3 -m pygame.examples.aliens
```
For more information, [Here](https://www.pygame.org/wiki/GettingStarted).

## Algorithm

### Solve(board)

For each empty space (i,j) on the board:
  - Try to place number 1...9 on the (i,j) position.
      - If placing that number causes a invalid board, we move to the next number/solution.
      - Else we go solve the board recursively by invoking solve() with new pieces inserted.
  - If we try all possible solution recursively and none gives valid board, backtrack to previous
  number we try to fill in.

We find the solution if we manage to fill every empty space on the board and reach here.

### Validate(board)

To validate whether a number is legal in current board:
  - check the 3x3 sub-boxes if there's a same number
  - check the column if there's a same number
  - check the row if there's a same number

### Random Board Generation
For each 3x3 subboard:
  pick a position in the 3x3 suboard
  generate a list of all potential number of that position, sample one from the list, and place it at the position

Invoke Solve(board) to solve the current board
Generate a list of all positions in the board, randomly shuffle it
For each position:
  Remove the current placed value
  count number of solutions the board has after removing the value
  If the board has **exactly one** solution, move to next position
  Else, we place back the value that we removed, move to next position
  


## Examples

To run the game, simply run:
```
python3 sudoku.py
```

Press "Enter/Return" to solve the board
Press "g" to generate a new board

Sometimes it might take minutes to generate a random board, because there's
some board that's inherently hard to solve and might take minutes to be solved.
Most of time the board should be generated within seconds.



## Analysis

### Time Complexity
Since each empty space has up to 9 solutions and there are O(n) empty spaces in the worst cases. 
Time complexity is O(9^n).

### Space Complexity
The algorithm place the potential solutions in-place, at first glance it would be O(1).
However we also uses the stack spaces when doing recursion/backtracking, the space
complexity is still O(9^n).

### Optimization
We could use contraint solving to further improve our runtime and space usage. Instead of trying
all 9 possible numbers when we encounter a empty space, we can prune away some candidate numbers by looking at
its corresponding 3x3 sub-box, its current row and its current column. Hence practically we could prune away
some recursion branches when running the algorithm, however the space/time complexity remain unchanged in
the worst case analysis.
