default:
	@cat makefile

env:
	python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update: env
	. env/bin/activate; pip install -r requirements.txt

lint:
        . env/bin/activate; pylint bin/normalize_gainers.py

test:
        . env/bin/activate; pytest -vv tests/
