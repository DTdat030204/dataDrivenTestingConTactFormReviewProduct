# LV1 — Contact Form & Review Product (Selenium Data-Driven Tests)

This folder contains Selenium + `unittest` data-driven tests for the LambdaTest  
e-commerce demo site:

- Contact form submission — `ContactForm.py` with data from `ContactForm.csv`
- Product review submission — `ReviewProduct.py` with data from `ReviewProduct.csv`

---

## 1. Requirements

- Python 3.10+ (tested with Python 3.12)
- Google Chrome installed
- Matching ChromeDriver (managed by Selenium 4 or placed on your `PATH`)

---

## 2. Setup (Windows PowerShell)

From the repository root:

```powershell
cd .\LV1_CONTACTFORM_REVIEWPRODUCT\
````

```powershell
python -m venv .venv
```

```powershell
.\.venv\Scripts\Activate.ps1
```

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If you get an execution policy error when activating the venv:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 3. ChromeDriver

The tests require Google Chrome and a compatible ChromeDriver.

**Option 1 — Manual:**
Place `chromedriver.exe` in this folder or anywhere on your system `PATH`.

**Option 2 — Driver manager:**
Install `webdriver-manager` and update the scripts to load ChromeDriver automatically.

Make sure ChromeDriver **matches your Chrome version**, otherwise Selenium may fail.

---

## 4. Running the tests

### Contact Form:

```powershell
cd .\LV1_CONTACTFORM_REVIEWPRODUCT
python .\ContactForm.py
```

### Review Product:

```powershell
cd .\LV1_CONTACTFORM_REVIEWPRODUCT
python .\ReviewProduct.py
```

Each script will:

* Read test data from its CSV file
* Open the LambdaTest demo pages
* Execute multiple data-driven test cases (1 CSV row = 1 test)
* Print a colored summary of passed/failed rows and the final pass rate

---

## 5. Project structure

* `ContactForm.py`
* `ContactForm.csv`
* `ReviewProduct.py`
* `ReviewProduct.csv`
* `requirements.txt`

---

## 6. Notes & Troubleshooting

* Keep CSV files in the same directory as the scripts.
* If Selenium warns about `.cache` not being accessible, you can ignore it or run PowerShell once as Admin.
* If you run into driver/session errors, verify the Chrome ↔ ChromeDriver version compatibility.

