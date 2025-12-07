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

From the repository root:

cd .\LV1_CONTACTFORM_REVIEWPRODUCT\

python -m venv .venv
..venv\Scripts\Activate.ps1

python -m pip install --upgrade pip
pip install -r requirements.txt

text

If you get an execution policy error when activating the venv:

Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

text


## 3. ChromeDriver

The tests require Google Chrome and a compatible ChromeDriver:

- Option 1: Put a matching `chromedriver.exe` on your `PATH` (or in this folder).
- Option 2: Use a driver manager (e.g. `webdriver-manager`) and update the code to create the driver via it.

Make sure the ChromeDriver version matches your installed Chrome, otherwise Selenium may fail to start the browser.


## 4. Running the tests

Run Contact Form tests:

cd .\LV1_CONTACTFORM_REVIEWPRODUCT
python .\ContactForm.py

text

Run Review Product tests:

cd .\LV1_CONTACTFORM_REVIEWPRODUCT
python .\ReviewProduct.py

text

Each script will:

- Read test data from its CSV file in the same folder.
- Open the LambdaTest demo product/contact pages.
- Execute multiple data‑driven test cases (1 CSV row = 1 test).
- Print a colored summary of passed / failed rows and overall pass rate.


## 5. Project structure

- `ContactForm.py`  — Selenium DDT tests for the contact form
- `ContactForm.csv` — Test data for contact form scenarios
- `ReviewProduct.py`  — Selenium DDT tests for product reviews
- `ReviewProduct.csv` — Test data for review scenarios
- `requirements.txt`  — Python dependencies


## 6. Notes & troubleshooting

- Keep the CSV files together with the Python scripts; they are required for the tests.
- If you see warnings like Selenium cache folder cannot be created under  
  `C:\Users\<user>\.cache\selenium`, you can:
  - Ignore them if tests still run, or
  - Run PowerShell as Administrator once so Selenium can create the folder.
- If you get driver or session errors, check that your Chrome and ChromeDriver
  versions are compatible and update one of them if needed.
