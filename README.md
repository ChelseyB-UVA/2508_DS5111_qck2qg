# 2508_DS5111_qck2qg

# Repository Setup Guide

## Requirements (Starting Point)
- A fresh VM (Linux-based, e.g. Ubuntu 20.04+).
- GitHub SSH key configured for access.
- Git installed (`git --version`).
- Python 3.8+ installed (`python3 --version`).

---

## Step 1: Clone the Repository
```bash
git clone git@github.com:<your-username>/repository_name.git
cd repository_name

the top line is to clone your repository and the second line (cd) is to make sure you are inside your
repository. 

## Step 2: Set up the Environment
Create a new file in the repository called makefile:
nano makefile

inside this file you will add this:
default:
	@cat makefile

env: 
	python3 -m venv env; .env/bin/activate; pip install --upgrade pip

update:	env
	. env/bin/activate; pip install -r requirements.txt

Ensure you are using tab for spacing and not the spacebar as this could make an error message.

no need to execute this command as the make command will take care of this, to verify the file
is working type make into the bash command line,this should bring up to code that was typed above.

## Step 3: Verification
In Bash type

ls env/bin/activate

This is to check to make sure the enviorment exists, if it exists then we can activate and install 
the needed packages by running:

. env/bin/activate
python -m pip list

This will install the Python package, once complete we can verify with:

python scripts/example.py

## Step 4: Push to github

Once completed and you want to save your files you will execute the following commands:

git add . 
(This will all add files, if you are looking to add specific files you would type git add (file name)

git commit -m "notes for the push"

git push

To verify the files were pushed you can type:

git log (verifies commit is done)

git status (will show you if everything is up to date)

## Please note

When in the nano file for updating 

CTRL+0 - enter to save your file 
CTRL+X to exit
Enter to return to bash


## Headless Chrome Setup

This repo includes a helper script to install Google Chrome (headless) on Ubuntu.

### Run the installer
**This repo command  was cloned from 2508_DS5111_materials/scripts/ **
```bash
bash scripts/install_chrome_headless.sh

### Verify it works
google-chrome-stable --version
google-chrome-stable --headless --no-sandbox --disable-gpu --dump-dom https://example.com | head

## Normalizer function

This project provides a script to normalize stock gainer tables scraped from:

Yahoo Finance (top gainers)

Wall Street Journal (WSJ) (U.S. movers)

The normalizer will output a more legiable CSV file containing the schemas: symbol, company_name, price, change, perc_change, volume

## Step 1
Clone the repository and install python
 
git clone git@github.com:ChelseyB-UVA/2508_DS5111_qck2qg.git
cd 2508_DS5111_qck2qg
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt

Then  clone the repository 2508_DS5111_materials/scripts/ into your scripts file
Then clone the repository 2508_DS5111_materials/scripts/Makefile into your scripts file

## Step 2
Collect the raw data using the makefiles in bash

make ygainers.csv
make wsjgainers.csv

##Step 3
Build  the .py file to house the functions needed to normalize the data

nano bin.normalize_gainers.py

once functions are written and saved then pull python to run

##Step 4 
Test the functions:

python bin/normalize_gainers.py

if scripts are correct it should produce
yganiers_normalized.csv
wsjgainers_normalized.csv

I tested the script by:

Generating raw CSVs (make ygainers.csv, make wsjgainers.csv).

Running the normalizer (python bin/normalize_gainers.py).

Checking the outputs:
head ygainers_normalized.csv
head wsjgainers_normalized.csv

##Noted

.gitignore is set up to exclude raw .html and .csv scrape files, but keeps the normalized outputs (*_normalized.csv).

WSJ and Yahoo may change their table column names. If parsing fails, inspect the columns:
python -c "import pandas as pd; print(pd.read_csv('wsjgainers.csv').columns)"

