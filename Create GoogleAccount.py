import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.service import Service


# --- Configuration ---
# You can add more names to these lists to increase variety.
FIRST_NAMES = [
    "James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph",
    "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson"
]

def generate_details():
    """Generates a realistic first name, last name, and a username."""
    first_name = random.choice(FIRST_NAMES)
    last_name = random.choice(LAST_NAMES)
    # Generate 5 random numbers to append to the name for the username
    random_suffix = ''.join(random.choices(string.digits, k=5))
    username = f"{first_name.lower()}{last_name.lower()}{random_suffix}"
    # Generate a secure password (10 letters + 2 digits + 1 symbol)
    birth_year = random.randint(1970, 2018)
    password = ''.join(random.choices(string.ascii_letters, k=10)) + \
               ''.join(random.choices(string.digits, k=2)) + \
               random.choice("!@#$%^&*()")
    return first_name, last_name, username, password, birth_year

def get_random_user_agent():
    """Returns a random user agent from the list."""
    UAGENTS = [
        'Mozilla/5.0 (X11; CrOS x86_64 14526.57.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.64 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.84.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.93 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.59.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.91.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.55 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.23.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.20 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.36.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.36 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.26 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.6 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.67.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.41 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14685.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4992.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.69.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.82 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14682.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.16 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.9.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.5 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14574.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4937.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.52.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14716.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5002.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14268.81.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14469.41.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.48 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14388.61.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.37.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.37 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.51.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.32 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.92.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.56 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.43.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.54 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14505.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4870.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.16.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.25 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.28.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.44 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14543.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4918.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.11.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.6 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.89.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.133 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14588.31.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.19 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14526.6.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.13 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14658.0.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.4975.0 Safari/537.36',
        'Mozilla/5.0 (X11; CrOS x86_64 14695.25.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5002.0 Safari/537.36'
    ]
    return random.choice(UAGENTS)

def save_account_details(username, password):
    """Saves the successfully created account credentials to a text file."""
    with open("accounts.txt", "a") as file:
        file.write(f"{username}@gmail.com:{password}\n")
    print(f"[SUCCESS] Account details saved to accounts.txt: {username}@gmail.com")

def create_google_account(driver, first_name, last_name, username, password, birth_year):
    """
    Automates the Google account creation process with a more robust, sequential flow.
    """
    try:
        # 1. Navigate and fill in name
        driver.get("https://accounts.google.com/signup")
        print(f"Step 1: Filling in name '{first_name}'")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "firstName"))).send_keys(first_name)
        driver.find_element(By.NAME, "lastName").send_keys(last_name)
        print(f"Step 1: Filling in name '{last_name}'")
        driver.find_element(By.XPATH, "//span[contains(text(),'Next')]").click()

        # 2. Fill in Birthday and Gender
        print(f"Step 2: Filling in birthday: '{birth_year}' and gender: male")
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "year"))).send_keys(birth_year)
        driver.find_element(By.ID, "day").send_keys(str(random.randint(1, 28)))
        driver.find_element(By.ID, "month").click()
        month_value = str(random.randint(1, 12))
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, f"//li[@data-value='{month_value}']"))).click()
        driver.find_element(By.ID, "gender").click()
        WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.XPATH, "//li[.//span[text()='Male']]"))).click()
        driver.find_element(By.XPATH, "//span[contains(text(),'Next')]").click()

        # --- START: MODIFIED SECTION ---
       # 3. Choose how you’ll sign in
        print("Step 3: Clicking 'Create a Gmail address")
        try:
            # Wait for the button to be clickable and then click it.
            create_address_button = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, "//*[text()='Create a Gmail address']"))
            )
            create_address_button.click()
            driver.find_element(By.XPATH, "//span[contains(text(),'Next')]").click()
            print("[INFO] Successfully clicked 'Create a Gmail address'.")

        except TimeoutException:
            # This handles the case where the button doesn't appear.
            # The script will just move on instead of crashing.
            print("[INFO] 'Create a Gmail address' button not found, proceeding assuming it was not needed.")



        # 4. Loop for username creation and handling "username taken" error
        print("Step 4: Entering username:")
        while True:
            username_input = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.NAME, "Username"))
            )
            username_input.clear()
            username_input.send_keys(username)
            print(username)

            # Click the 'Next' button
            next_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Next')]"))
            )
            next_button.click()

            # Wait briefly for the page to react (e.g., DOM update)
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )

            # Check if the "username taken" message is present in the DOM
            taken_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'That username is taken')]")
            if taken_elements:
                print(f"[INFO] Username '{username}' is taken. Retrying with a new one.")
                _, _, username, _ = generate_details()
                continue  # Try again with a new username

            print("[SUCCESS] Username accepted.")
            break  # Move to the next step



        # 5. Create Password
        print(f"Step 5: Setting password: '{password}'")
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.NAME, "Passwd"))).send_keys(password)
        driver.find_element(By.NAME, "PasswdAgain").send_keys(password)
        WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Next')]"))).click()




        # 6. Indefinite wait for manual phone verification
        print("\n" + "="*60)
        print(">>> PAUSED: Please complete phone verification in the browser. <<<")
        print("       The script will wait indefinitely until you are finished.")
        print("       Close the browser manually if you wish to stop.")
        print("="*60 + "\n")

        # Wait until the URL changes, indicating user has passed the phone step
        WebDriverWait(driver, timeout=9999).until(EC.url_contains("reviewyouraccount"))
        print("Phone verification completed by user. Proceeding...")
        driver.find_element(By.XPATH, "//span[contains(text(),'Next')]").click()

        # 7. Agree to Privacy and Terms
        print("Step 7: Agreeing to Privacy and Terms...")
        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'I agree')]"))
        ).click()

        # Wait for the final page to load
        WebDriverWait(driver, 20).until(EC.url_contains("myaccount.google.com"))

        return True

    except Exception as e:
        print(f"\n[FATAL ERROR] An unexpected error occurred: {e}")
        print("The script cannot continue. Saving a screenshot as 'fatal_error.png'.")
        driver.save_screenshot("fatal_error.png")
        return False


def display_menu():
    """Displays the main menu and handles user input."""
    print("\n" + "="*30)
    print("  Google Account Creator")
    print("="*30)
    print("1. Start Creating Accounts")
    print("2. Exit")
    print("="*30)
    return input("Choose an option: ")

def main():
    """Main function to run the script."""
    driver = None

    # The path to your chromedriver executable
    CHROME_DRIVER_PATH = "/usr/bin/chromedriver"
    service = Service(executable_path=CHROME_DRIVER_PATH)

    try:
        while True:
            choice = display_menu()
            if choice == '1':
                try:
                    while True:
                        try:
                            num_accounts = int(input("How many accounts do you want to create? (max 5): "))
                            if 1 <= num_accounts <= 5:
                                break
                            else:
                                print("Invalid number. Please enter a number between 1 and 5.")
                        except ValueError:
                            print("Invalid input. Please enter a number.")

                    # --- MODIFIED SECTION STARTS HERE ---

                    user_agent = get_random_user_agent()

                    options = webdriver.ChromeOptions()
                    options.add_argument(f"--user-agent={user_agent}")
                    options.add_argument("--incognito")

                    # --- FIX FOR ROOT USER ---
                    options.add_argument("--no-sandbox")
                    options.add_argument("--disable-dev-shm-usage")
                    # -------------------------

                    options.add_argument("--disable-blink-features=AutomationControlled")
                    options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    options.add_experimental_option('useAutomationExtension', False)

                    # --- MODIFIED SECTION ENDS HERE ---

                    # Pass the service object here
                    driver = webdriver.Chrome(service=service, options=options)
                    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
                    print(f"[INFO] Starting browser with User Agent: {user_agent}")

                    successful_creations = 0
                    for i in range(num_accounts):
                        print(f"\n--- Starting Account Creation #{i+1} ---")
                        first_name, last_name, username, password, birth_year = generate_details()

                        if create_google_account(driver, first_name, last_name, username, password, birth_year):
                            save_account_details(username, password)
                            successful_creations += 1
                        else:
                            print(f"--- Failed to create account #{i+1} ---")
                            input("An error occurred. The browser is paused. Press Enter to close the browser and end the script.")
                            break
                        time.sleep(3)
                    print(f"\nFinished. Successfully created {successful_creations}/{num_accounts} accounts.")
                finally:
                    if driver:
                        driver.quit()
                        driver = None

            elif choice == '2':
                print("Exiting script. Goodbye!")
                break
            else:
                print("Invalid option, please try again.")

    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Shutting down and exiting.")

    finally:
        if driver:
            print("Ensuring browser is closed...")
            driver.quit()


if __name__ == "__main__":
    main()
