# LV1 — Contact Form & Review Product (Selenium Data-Driven Tests)

This folder contains Selenium + `unittest` data-driven tests for the LambdaTest
e‑commerce demo site:

- Contact form submission — `ContactForm.py` with data from `ContactForm.csv`
- Product review submission — `ReviewProduct.py` with data from `ReviewProduct.csv`


## 1. Requirements

- Python 3.10+ (tested with Python 3.12)
- Google Chrome installed
- Matching ChromeDriver (managed by Selenium 4 or placed on your `PATH`)


## 2. Setup (Windows PowerShell)

From this folder:

python -m venv .venv
..venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

text

If you get an execution policy error when activating the venv:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

text


## 3. Running the tests

Run Contact Form tests:

python .\ContactForm.py

text

Run Review Product tests:

python .\ReviewProduct.py

text

Each script will:

- Read test data from its CSV file in the same folder.
- Open the LambdaTest demo product/contact pages.
- Execute multiple data‑driven test cases (1 CSV row = 1 test).
- Print a colored summary of passed / failed rows and overall pass rate.


## 4. Project structure

- `ContactForm.py`  — Selenium DDT tests for the contact form
- `ContactForm.csv` — Test data for contact form scenarios
- `ReviewProduct.py`  — Selenium DDT tests for product reviews
- `ReviewProduct.csv` — Test data for review scenarios
- `requirements.txt`  — Python dependencies


## 5. Notes & troubleshooting

- Keep the CSV files together with the Python scripts; they are required for the tests.
- If you see warnings like Selenium cache folder cannot be created under  
  `C:\Users\<user>\.cache\selenium`, you can:
  - Ignore them if tests still run, or
  - Run PowerShell as Administrator once so Selenium can create the folder.
- Make sure your Chrome and ChromeDriver versions are compatible.  
  If you get driver/session errors, update Chrome or ChromeDriver accordingly.
