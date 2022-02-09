# 11-Puzzle-Problem

## Overview

This is a completed program that solves the 11-Puzzle Problem using the weighted A* Search Algorithm. It takes an input in the form of a text file that contains the initial state and the goal state. It then produces an output file with the result containing the moves required to reach the goal state, the number of nodes generated, the depth of the tree, and the W-value given.

You can find sample input and output files for reference.

## Instructions on how to run the program:

  This program requires installing the heapq module using pip. The heapq module is used here for
  re-sorting the frontier and ensuring the state with the same smallest f-value is at the front.
  To install heapq, use this command:
  python -m pip install heapq
  Sometimes, "python" might need to be replaced with "python3", "py", or "py3" in the command   above.
  At the end of the source code, there is one line that calls a function named A_Star_Search.
  It takes two arguments. The first argument is the filename and the second argument tells the   program whether DEBUG_MODE should be enabled. If DEBUG_MODE is enabled, the program will   additonally output the G, H, and F values for every node on the solution path, along wih its
  state. To output the correct format, please set DEBUG_MODE to False.
  Ex. A_Star_Search("Input1.txt", False)
