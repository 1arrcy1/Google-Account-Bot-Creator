import time
import random
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


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
    # CHANGE 1: Add this line to prevent errors.
    driver = None

    # CHANGE 2: Add the 'try' keyword here.
    try:
        while True:
            choice = display_menu()
            if choice == '1':
                # CHANGE 3: The rest of the logic is wrapped in a new try/finally
                # to ensure the browser from each run is closed properly.
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

                    options = webdriver.ChromeOptions()
                    options.add_argument("--disable-blink-features=AutomationControlled")
                    options.add_experimental_option("excludeSwitches", ["enable-automation"])
                    options.add_experimental_option('useAutomationExtension', False)

                    driver = webdriver.Chrome(options=options)
                    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

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
