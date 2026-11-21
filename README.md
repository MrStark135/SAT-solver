# SAT CNF solver for latin squares - proof of concept
This project includes a SAT CNF solver and a latin square generator and interface to the solver

## How to run
### Setup
First we need a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate
```
Then install the package itself to the environment
```bash
pip install -e .
```
And finally run any of the scripts from ```examples/```
```bash
python examples/example.py
python examples/test.py
```

## Play around
Once the package is installed (in the virtual env or globally) you can make files and import the packages, see ```example.py``` for reference