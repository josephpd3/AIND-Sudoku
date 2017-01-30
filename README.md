# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?
A: Like the Elimination strategy, the purpose of Naked Twins (NT) is to eliminate possible choices from the peers of given boxes. With this in mind, it was ideal to utilize the NT strategy in the `reduce_puzzle` loop--alongside Elimination and Only Choice--so that the constraints applied on each iteration both lent to and included those imposed by NT. That is, the reduced puzzle from one iteration lent to the relevance and success of NT in the next iteration.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal sudoku problem?
A: In the adjustments to the implementation for a standard sudoku board, one may simply add the diagonal units to the board so that the peers of respective boxes within them may have the same constraints applied to them as the peers of boxes within standard units (3x3, horizontal, vertical). Given this consideration, we simply augment our strategies which work across all units to consider these diagonal units as well--adding to the constraints which they apply iteratively through propagation.

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project. 
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in function.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.