# Basic SAT CNF solver for latin squares - proof of concept
This project includes a basic SAT cnf solver and a grid which supports sizes up to 9x9, but the solver is not optimized, so it can solve a square of maximum size of 3x3 (27 variables, 108 rules) in ~45sec

## How to run
### Prerequisites
To install the dependencies just run
```bash
pip install -r requirements.txt
```
or optionally make a virtual environment first to avoid cluttering global packages
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### Run 
The code is in 2 files, cnf.py and grid.py, where grid.py is the main code, so just run
```bash
python3 grid.py
```

### Modify
Currently there is not much to play with since the SAT resolver is not poweful enough to handle latin squares larger than 3x3, but just to mention it
```python
grid = Grid(3) # the size of the square
```

## Problems
### Symbols
Currently the squares are using numbers {1, 2, 3...} instead of symbols {A, B, C...} which I implemented to simplify addressing and decrease amount of variables, but at a cost of readibility. The indexing starts from 0, where the variables from 1, so the mapping is always +1 as can be noticed throughout the code. A better alternative would be storing an actual list of symbols and mapping them to values, since {A:0, B:1, C:2...} is much more intelligible than {1:0, 2:1, 3:2...}

### Combinations
Currently the eval function uses a binary ripple counter to go through all the combinations, with only basic boolean logic optimizations:
- a chain of ORs evaluates to True after the first True value, i.e. the rest can be skipped
- a chain of ANDs evaluates to False after the first False, -||-
There are more optimizations to make

## Challenges encountered
- writing dynamic rule generation for a given size of the square
- mapping the variables to actual positions in the grid
- not yet optimized