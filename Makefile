PYTHON=python3

install:
	$(PYTHON) -m pip install -r requirements.txt

test:
	$(PYTHON) -m pytest -q

smoke:
	$(PYTHON) -m sdhtlc.run_experiment --experiment smoke

e1:
	$(PYTHON) -m sdhtlc.run_experiment --experiment E1 --seeds 20 --swaps-per-seed 10000

all:
	$(PYTHON) -m sdhtlc.run_experiment --experiment all --seeds 20 --swaps-per-seed 1000
