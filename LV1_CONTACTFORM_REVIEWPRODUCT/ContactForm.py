# -*- coding: utf-8 -*-
import unittest
import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# ================== COLORS & GLOBAL RESULTS ==================

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

TEST_RESULTS = {}   # row_number -> PASSED / FAILED

# ================== CONTACT FORM DDT CLASS ==================

class ContactFormDDT(unittest.TestCase):

    def setUp(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-features=PasswordManagerEnabled,PasswordLeakDetection")
        chrome_options.add_argument("--disable-browser-password-manager")
        chrome_options.add_argument("--disable-save-password-bubble")
        chrome_options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
                "profile.password_manager_leak_detection": False,
                "password_manager_enabled": False
            }
        )

        self.driver = webdriver.Chrome(service=Service(), options=chrome_options)
        self.driver.implicitly_wait(10)
        self.verificationErrors = []
        self.current_row = None

    # ---- validate input data from CSV (optional, giống Deposit) ----
    def validate_input_data(self, row):
        errors = []
        required_fields = ["yourName", "yourEmail", "subject", "message", "expectedResult"]
        for f in required_fields:
            if f not in row or row[f].strip() == "":
                errors.append(f"Missing or empty field: {f}")
        return (len(errors) == 0, "; ".join(errors) if errors else None)

    def run_contact_test(self, row, row_number):
        d = self.driver
        self.current_row = row_number
        print(f"\n{Colors.BLUE}[Contact Row {row_number}] Processing:{Colors.RESET}", row)

        try:
            # validate data
            is_valid, msg = self.validate_input_data(row)
            if not is_valid:
                TEST_RESULTS[row_number] = "FAILED"
                self.verificationErrors.append(f"Input validation failed: {msg}")

            name = row["yourName"].strip()
            email = row["yourEmail"].strip()
            subject = row["subject"].strip()
            message = row["message"].strip()
            expected = row["expectedResult"].strip()

            # 1. mở trang Contact form
            d.get("https://ecommerce-playground.lambdatest.io/index.php?route=extension/maza/page&page_id=9")

            # cuộn xuống vùng contact form
            d.execute_script("arguments[0].scrollIntoView();",
                            d.find_element(By.XPATH, "//h2[normalize-space()='Contact form']"))
            time.sleep(1)

            # 2. nhập dữ liệu
            name_input = d.find_element(By.XPATH, "//input[@placeholder='Your name']")
            name_input.clear()
            name_input.send_keys(name)

            email_input = d.find_element(By.XPATH, "//input[@placeholder='Your email']")
            email_input.clear()
            email_input.send_keys(email)

            subject_input = d.find_element(By.XPATH, "//input[@placeholder='Subject']")
            subject_input.clear()
            subject_input.send_keys(subject)

            message_input = d.find_element(By.XPATH, "//textarea[@placeholder='Message']")
            message_input.clear()
            message_input.send_keys(message)

            # nút Send message
            d.find_element(
                By.XPATH,
                "//button[normalize-space()='Send message']"
            ).click()


            # 4. chờ message
            WebDriverWait(d, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(1)

            body_text = d.find_element(By.TAG_NAME, "body").text
            self.verify_contact_expected(body_text, expected, row_number)

            # đánh dấu pass/fail cho row
            if not self.verificationErrors:
                TEST_RESULTS[row_number] = "PASSED"
                print(f"{Colors.GREEN}[Contact Row {row_number}] PASSED{Colors.RESET}")
            else:
                TEST_RESULTS[row_number] = "FAILED"
                print(f"{Colors.RED}[Contact Row {row_number}] FAILED{Colors.RESET}")

        except NoSuchElementException as e:
            TEST_RESULTS[row_number] = "FAILED"
            self.verificationErrors.append(f"Element not found: {e}")
            print(f"{Colors.RED}[Contact Row {row_number}] FAILED (NoSuchElement){Colors.RESET}")
        except Exception as e:
            TEST_RESULTS[row_number] = "FAILED"
            self.verificationErrors.append(f"Unexpected error: {type(e).__name__}: {e}")
            print(f"{Colors.RED}[Contact Row {row_number}] FAILED (Exception){Colors.RESET}")

    def verify_contact_expected(self, body_text, expected, row_number):
        # map expectedResult -> message substring
        if expected == "SUCCESS":
            if "Your message has been sent" not in body_text:
                self.verificationErrors.append(
                    f"[Row {row_number}] Expected SUCCESS message not shown"
                )
        elif expected == "ERR_NAME":
            if "Name must be between 3 and 32 characters" not in body_text:
                self.verificationErrors.append(
                    f"[Row {row_number}] Name error message not shown"
                )
        elif expected == "ERR_EMAIL":
            if "E-Mail Address does not appear to be valid" not in body_text:
                self.verificationErrors.append(
                    f"[Row {row_number}] Email error message not shown"
                )
        elif expected == "ERR_SUBJECT":
            if "Subject must be between 3 and 78 characters" not in body_text:
                self.verificationErrors.append(
                    f"[Row {row_number}] Subject error message not shown"
                )
        elif expected == "ERR_MESSAGE":
            if "Message must be between 10 and 3000 characters" not in body_text:
                self.verificationErrors.append(
                    f"[Row {row_number}] Message error message not shown"
                )

    def tearDown(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Warning in tearDown: {e}")
        if self.verificationErrors and self.current_row:
            TEST_RESULTS[self.current_row] = "FAILED"

# ================== DDT LOADER FOR CONTACT ==================

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    
    with open("ContactForm.csv", mode="r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Warning: ContactFormDDT.csv is empty")
        return suite

    print(f"\n{Colors.BOLD}{'='*70}")
    print(f"Loading {len(rows)} Contact Form test cases from CSV...")
    print(f"{'='*70}{Colors.RESET}")

    for idx, row in enumerate(rows):
        row_number = idx + 1
        test_name = f"test_contact_row_{row_number}"

        def create_test(r, rnum):
            def test_method(self):
                self.run_contact_test(r, rnum)
            return test_method

        setattr(ContactFormDDT, test_name, create_test(row, row_number))
        suite.addTest(ContactFormDDT(test_name))

    return suite

# ================== SUMMARY & RUNNER (DÙNG CHUNG) ==================

def print_test_summary():
    if not TEST_RESULTS:
        return
    print(f"\n{Colors.BOLD}{'='*70}")
    print(f"TEST EXECUTION SUMMARY (Contact Form)")
    print(f"{'='*70}{Colors.RESET}")

    passed = sum(1 for s in TEST_RESULTS.values() if s == "PASSED")
    failed = sum(1 for s in TEST_RESULTS.values() if s == "FAILED")
    total = len(TEST_RESULTS)

    print(f"\n{Colors.BOLD}{'Row':<10} {'Status':<15}{Colors.RESET}")
    print(f"{'-'*30}")
    for row_num in sorted(TEST_RESULTS.keys()):
        status = TEST_RESULTS[row_num]
        color = Colors.GREEN if status == "PASSED" else Colors.RED
        symbol = "✓" if status == "PASSED" else "✗"
        print(f"{row_num:<10} {color}{symbol} {status:<10}{Colors.RESET}")

    print(f"\n{Colors.BOLD}{'-'*30}")
    print(f"Total Tests: {total}")
    print(f"{Colors.GREEN}Passed: {passed}{Colors.RESET}")
    print(f"{Colors.RED}Failed: {failed}{Colors.RESET}")
    pass_rate = (passed / total * 100) if total else 0
    color = Colors.GREEN if pass_rate == 100 else (Colors.YELLOW if pass_rate >= 50 else Colors.RED)
    print(f"{color}Pass Rate: {pass_rate:.1f}%{Colors.RESET}")
    print(f"{Colors.BOLD}{'='*70}{Colors.RESET}\n")

class CustomTestResult(unittest.TextTestResult):
    def stopTestRun(self):
        super().stopTestRun()
        print_test_summary()

class CustomTestRunner(unittest.TextTestRunner):
    resultclass = CustomTestResult

if __name__ == "__main__":
    unittest.main(testRunner=CustomTestRunner(verbosity=2))
