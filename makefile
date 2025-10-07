default:
	@cat makefile

env:
	python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update: env
	. env/bin/activate; pip install -r requirements.txt

test:
	. env/bin/activate; pytest -vv tests/

lint:
	. env/bin/activate; pylint bin/normalize_gainers.py

linttest: lint test
	@echo "✅ Linting and tests complete"
