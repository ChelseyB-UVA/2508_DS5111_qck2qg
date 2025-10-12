
default:
	@cat makefile
env:
	python3 -m venv env; . env/bin/activate; pip install --upgrade pip

update: env
	. env/bin/activate; pip install -r requirements.txt
	bash -c "source env/bin/activate && pip install -r requirements.txt"

ygainers.html:
	sudo google-chrome-stable --headless --disable-gpu --dump-dom --no-sandbox --timeout=5000 'https://finance.yahoo.com/markets/stocks/gainers/?start=0&count=200' > ygainers.html

ygainers.csv: ygainers.html
	. env/bin/activate; python -c "import pandas as pd; raw = pd.read_html('ygainers.html'); raw[0].to_csv('ygainers.csv')"

wsjgainers.html:
	sudo google-chrome-stable --headless --disable-gpu --dump-dom --no-sandbox --timeout=5000 https://www.wsj.com/market-data/stocks/us/movers > wsjgainers.html

wsjgainers.csv: wsjgainers.html
	. env/bin/activate; python -c "import pandas as pd; raw = pd.read_html('wsjgainers.html'); raw[0].to_csv('wsjgainers.csv')"

.PHONY: ygainers_tstamp
ygainers_tstamp: ygainers.csv
	mv ygainers.csv ygainers_$$(date +"%Y%m%d_%H%M%S").csv

.PHONY: wsjgainers_tstamp
wsjgainers_tstamp: wsjgainers.csv
	mv wsjgainers.csv wsjgainers_$$(date +"%Y%m%d_%H%M%S").csv

.PHONY: clean
clean:
	rm ygainers.html ygainers.csv wsjgainers.html wsjgainers.csv | true

lint:
	. env/bin/activate; pylint bin/normalize_gainers.py

test:
	. env/bin/activate; pytest -vv tests/

linttest: lint test
	@echo "✅ Linting and tests complete"
