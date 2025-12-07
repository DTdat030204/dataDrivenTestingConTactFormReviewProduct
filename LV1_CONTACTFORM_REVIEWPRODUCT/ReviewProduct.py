# -*- coding: utf-8 -*-
import unittest
import csv
from pathlib import Path
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

TEST_RESULTS = {}

class ReviewProductDDT(unittest.TestCase):

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

    def validate_input_data(self, row):
        errors = []
        required_fields = ["rating", "yourName", "yourReview", "expectedResult"]
        for f in required_fields:
            if f not in row or row[f].strip() == "":
                errors.append(f"Missing or empty field: {f}")
        return (len(errors) == 0, "; ".join(errors) if errors else None)

    # def run_review_test(self, row, row_number):
    #     d = self.driver
    #     self.current_row = row_number
    #     print(f"\n{Colors.BLUE}[Review Row {row_number}] Processing:{Colors.RESET}", row)

    #     try:
    #         is_valid, msg = self.validate_input_data(row)
    #         if not is_valid:
    #             TEST_RESULTS[row_number] = "FAILED"
    #             self.verificationErrors.append(f"Input validation failed: {msg}")

    #         rating = row["rating"].strip()
    #         name = row["yourName"].strip()
    #         review = row["yourReview"].strip()
    #         expected = row["expectedResult"].strip()

    #         # d.get("https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=42")

    #         # # cuộn xuống khu vực review
    #         # d.execute_script(
    #         #     "arguments[0].scrollIntoView();",
    #         #     d.find_element(By.XPATH, "//h2[normalize-space()='Write a review']")
    #         # )
    #         # time.sleep(1)
    #         # 1. mở tab review

    #         # # 2. chọn sao (nếu rating hợp lệ 1-5)
    #         # if rating.isdigit() and 1 <= int(rating) <= 5:
    #         #     star_xpath = f"//input[@name='rating'][@value='{rating}']"
    #         #     try:
    #         #         d.find_element(By.XPATH, star_xpath).click()
    #         #     except NoSuchElementException:
    #         #         self.verificationErrors.append(
    #         #             f"[Row {row_number}] Rating star {rating} not found"
    #         #         )

    #         # # 3. nhập tên, review
    #         # d.find_element(By.ID, "input-name").clear()
    #         # d.find_element(By.ID, "input-name").send_keys(name)

    #         # d.find_element(By.ID, "input-review").clear()
    #         # d.find_element(By.ID, "input-review").send_keys(review)

    #         # # 4. submit
    #         # d.find_element(By.ID, "button-review").click()


    #         # d.get("https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=42")

    #         # # cuộn tới khu Write a review
    #         # d.execute_script(
    #         #     "arguments[0].scrollIntoView();",
    #         #     d.find_element(By.XPATH, "//h3[normalize-space()='Write a review']")
    #         # )
    #         # time.sleep(1)

    #         # # chọn rating (radio 1..5)
    #         # if rating.isdigit() and 1 <= int(rating) <= 5:
    #         #     star_xpath = f"//input[@name='rating'][@value='{rating}']"
    #         #     d.find_element(By.XPATH, star_xpath).click()

    #         # # Your Name (input)
    #         # name_input = d.find_element(By.XPATH, "//input[@id='input-name' or @placeholder='Your Name']")
    #         # name_input.clear()
    #         # name_input.send_keys(name)

    #         # # Your Review (textarea)
    #         # review_input = d.find_element(By.XPATH, "//textarea[@id='input-review' or @placeholder='Your Review']")
    #         # review_input.clear()
    #         # review_input.send_keys(review)

    #         # # nút Write Review
    #         # d.find_element(By.XPATH, "//button[normalize-space()='Write Review']").click()

    #         d.get("https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=42")

    #         # cuộn tới form review
    #         form = WebDriverWait(d, 5).until(
    #             EC.presence_of_element_located((By.ID, "form-review"))
    #         )
    #         d.execute_script("arguments[0].scrollIntoView();", form)
    #         time.sleep(1)

    #         # # chọn sao rating
    #         # if rating.isdigit() and 1 <= int(rating) <= 5:
    #         #     star_xpath = f"//form[@id='form-review']//input[@name='rating'][@value='{rating}']"
    #         #     d.find_element(By.XPATH, star_xpath).click()
    #         if rating.isdigit() and 1 <= int(rating) <= 5:
    #             # input có value = rating
    #             input_xpath = f"//form[@id='form-review']//input[@name='rating' and @value='{rating}']"
    #             rating_input = WebDriverWait(d, 5).until(
    #                 EC.presence_of_element_located((By.XPATH, input_xpath))
    #             )
    #             rating_id = rating_input.get_attribute("id")

    #             # label tương ứng với input đó
    #             label_xpath = f"//form[@id='form-review']//label[@for='{rating_id}']"
    #             star_label = WebDriverWait(d, 5).until(
    #                 EC.element_to_be_clickable((By.XPATH, label_xpath))
    #             )
    #             star_label.click()



    #         # Your Name
    #         name_input = d.find_element(
    #             By.XPATH, "//form[@id='form-review']//input[@placeholder='Your Name']"
    #         )
    #         name_input.clear()
    #         name_input.send_keys(name)

    #         # Your Review
    #         review_input = d.find_element(
    #             By.XPATH, "//form[@id='form-review']//textarea[@placeholder='Your Review']"
    #         )
    #         review_input.clear()
    #         review_input.send_keys(review)

    #         # nút Write Review
    #         d.find_element(
    #             By.XPATH, "//form[@id='form-review']//button[normalize-space()='Write Review']"
    #         ).click()



    #         WebDriverWait(d, 5).until(
    #             EC.presence_of_element_located((By.TAG_NAME, "body"))
    #         )
    #         time.sleep(1)

    #         body_text = d.find_element(By.TAG_NAME, "body").text
    #         self.verify_review_expected(body_text, expected, row_number)

    #         if not self.verificationErrors:
    #             TEST_RESULTS[row_number] = "PASSED"
    #             print(f"{Colors.GREEN}[Review Row {row_number}] PASSED{Colors.RESET}")
    #         else:
    #             TEST_RESULTS[row_number] = "FAILED"
    #             print(f"{Colors.RED}[Review Row {row_number}] FAILED{Colors.RESET}")

    #     except NoSuchElementException as e:
    #         TEST_RESULTS[row_number] = "FAILED"
    #         self.verificationErrors.append(f"Element not found: {e}")
    #         print(f"{Colors.RED}[Review Row {row_number}] FAILED (NoSuchElement){Colors.RESET}")
    #     except Exception as e:
    #         TEST_RESULTS[row_number] = "FAILED"
    #         self.verificationErrors.append(f"Unexpected error: {type(e).__name__}: {e}")
    #         print(f"{Colors.RED}[Review Row {row_number}] FAILED (Exception){Colors.RESET}")

    def run_review_test(self, row, row_number):
        d = self.driver
        self.current_row = row_number
        print(f"\n{Colors.BLUE}[Review Row {row_number}] Processing:{Colors.RESET}", row)

        try:
            is_valid, msg = self.validate_input_data(row)
            if not is_valid:
                TEST_RESULTS[row_number] = "FAILED"
                self.verificationErrors.append(f"Input validation failed: {msg}")

            rating = row["rating"].strip()
            name = row["yourName"].strip()
            review = row["yourReview"].strip()
            expected = row["expectedResult"].strip()

            d.get("https://ecommerce-playground.lambdatest.io/index.php?route=product/product&product_id=42")

            # cuộn tới form review
            form = WebDriverWait(d, 10).until(
                EC.presence_of_element_located((By.ID, "form-review"))
            )
            d.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                form
            )
            time.sleep(0.5)

            # chọn sao rating (nếu hợp lệ)
            if rating.isdigit() and 1 <= int(rating) <= 5:
                input_xpath = f"//form[@id='form-review']//input[@name='rating' and @value='{rating}']"
                rating_input = WebDriverWait(d, 5).until(
                    EC.presence_of_element_located((By.XPATH, input_xpath))
                )
                d.execute_script(
                    "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                    rating_input
                )
                time.sleep(0.2)
                rating_id = rating_input.get_attribute("id")
                label_xpath = f"//form[@id='form-review']//label[@for='{rating_id}']"
                star_label = WebDriverWait(d, 5).until(
                    EC.element_to_be_clickable((By.XPATH, label_xpath))
                )
                star_label.click()

            # Your Name
            name_input = WebDriverWait(d, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//form[@id='form-review']//input[@placeholder='Your Name']")
                )
            )
            d.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                name_input
            )
            time.sleep(0.2)
            name_input.clear()
            name_input.send_keys(name)

            # Your Review
            review_input = WebDriverWait(d, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//form[@id='form-review']//textarea[@placeholder='Your Review']")
                )
            )
            d.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                review_input
            )
            time.sleep(0.2)
            review_input.clear()
            review_input.send_keys(review)

            # nút Write Review
            submit_btn = WebDriverWait(d, 5).until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//form[@id='form-review']//button[normalize-space()='Write Review']")
                )
            )
            d.execute_script(
                "arguments[0].scrollIntoView({block: 'center', inline: 'nearest'});",
                submit_btn
            )
            time.sleep(0.2)
            submit_btn.click()

            WebDriverWait(d, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            time.sleep(1)

            body_text = d.find_element(By.TAG_NAME, "body").text
            self.verify_review_expected(body_text, expected, row_number)

            if not self.verificationErrors:
                TEST_RESULTS[row_number] = "PASSED"
                print(f"{Colors.GREEN}[Review Row {row_number}] PASSED{Colors.RESET}")
            else:
                TEST_RESULTS[row_number] = "FAILED"
                print(f"{Colors.RED}[Review Row {row_number}] FAILED{Colors.RESET}")

        except NoSuchElementException as e:
            TEST_RESULTS[row_number] = "FAILED"
            self.verificationErrors.append(f"Element not found: {e}")
            print(f"{Colors.RED}[Review Row {row_number}] FAILED (NoSuchElement){Colors.RESET}")
        except Exception as e:
            TEST_RESULTS[row_number] = "FAILED"
            self.verificationErrors.append(f"Unexpected error: {type(e).__name__}: {e}")
            print(f"{Colors.RED}[Review Row {row_number}] FAILED (Exception){Colors.RESET}")


    def verify_review_expected(self, body_text, expected, row_number):
        if expected == "SUCCESS":
            if "Thank you for your review" not in body_text:
                self.verificationErrors.append(
                    f"[Row {row_number}] SUCCESS message not shown"
                )
        elif expected == "ERR_RATING":
            if "Warning: Please select a review rating" not in body_text:
                self.verificationErrors.append(
                    f"[Row {row_number}] Rating warning not shown"
                )
        elif expected == "ERR_NAME":
            if "Warning: Review Name must be between 3 and 25 characters" not in body_text:
                self.verificationErrors.append(
                    f"[Row {row_number}] Name warning not shown"
                )
        elif expected == "ERR_REVIEW":
            if "Warning: Review Text must be between 25 and 1000 characters" not in body_text:
                self.verificationErrors.append(
                    f"[Row {row_number}] Review text warning not shown"
                )

    def tearDown(self):
        try:
            self.driver.quit()
        except Exception as e:
            print(f"Warning in tearDown: {e}")
        if self.verificationErrors and self.current_row:
            TEST_RESULTS[self.current_row] = "FAILED"

# ================== LOADER ==================

def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()

    csv_path = Path(__file__).resolve().parent / "ReviewProduct.csv"
    if not csv_path.exists():
        print(f"Warning: Review data file not found: {csv_path}")
        return suite

    with csv_path.open(newline='', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        rows = list(reader)

    if not rows:
        print("Warning: ReviewProductDDT.csv is empty")
        return suite

    print(f"\n{Colors.BOLD}{'='*70}")
    print(f"Loading {len(rows)} Review Product test cases from CSV...")
    print(f"{'='*70}{Colors.RESET}")

    for idx, row in enumerate(rows):
        row_number = idx + 1
        test_name = f"test_review_row_{row_number}"

        def create_test(r, rnum):
            def test_method(self):
                self.run_review_test(r, rnum)
            return test_method

        setattr(ReviewProductDDT, test_name, create_test(row, row_number))
        suite.addTest(ReviewProductDDT(test_name))

    return suite

# ================== SUMMARY & RUNNER ==================

def print_test_summary():
    if not TEST_RESULTS:
        return
    print(f"\n{Colors.BOLD}{'='*70}")
    print(f"TEST EXECUTION SUMMARY (Review Product)")
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
