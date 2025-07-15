# Google Account Creator Bot 🤖

This Python script uses Selenium to automate the process of creating Google accounts. It generates random user details, navigates the signup form, handles common errors like taken usernames, and saves the credentials of successfully created accounts.

> **Disclaimer:** This script is intended for **educational purposes only**. Automating the creation of accounts may violate Google's Terms of Service. Use this script responsibly and at your own risk. The author is not responsible for any misuse or consequences, such as account suspension or IP blocking.

---

## ✨ Features

* **Automatic User Generation:** Creates random first names, last names, usernames, and secure passwords.
* **Dynamic Username Handling:** Automatically retries with a new username if the chosen one is already taken.
* **Interactive Menu:** A simple command-line interface to start the process or exit.
* **Manual Verification Pause:** The script intelligently pauses and waits for the user to complete the manual phone number verification step.
* **Credential Storage:** Saves the username and password for each successfully created account to an `accounts.txt` file.
* **Robust Error Handling:** Includes `try...except...finally` blocks to handle unexpected errors and ensure the browser closes correctly.

---

## 🔧 Setup & Installation

Follow these steps to get the script running on your local machine.

### Prerequisites

* [Python 3.x](https://www.python.org/downloads/)
* [Google Chrome](https://www.google.com/chrome/) browser
* [ChromeDriver](https://googlechromelabs.github.io/chrome-for-testing/)

### Steps

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/your-username/your-repository-name.git](https://github.com/your-username/your-repository-name.git)
    cd your-repository-name
    ```

2.  **Install Python dependencies:**
    The only required package is Selenium.
    ```bash
    pip install selenium
    ```

3.  **Download and Place ChromeDriver:**
    * Download the ChromeDriver version that **matches your Google Chrome browser version** from the [official Chromedriver downloads page](https://googlechromelabs.github.io/chrome-for-testing/).
    * Unzip the downloaded file and place the `chromedriver.exe` (Windows) or `chromedriver` (Mac/Linux) executable in the same directory as the Python script.

---

## 🚀 How to Use

1.  **Run the script from your terminal:**
    ```bash
    python your_script_name.py
    ```

2.  **Follow the Menu:**
    * Choose option `1` to start creating accounts.
    * Enter the number of accounts you wish to create (1-5).

3.  **Manual Phone Verification:**
    * The script will automate the initial steps and then pause when it reaches the phone verification page.
    * The console will display: `>>> PAUSED: Please complete phone verification in the browser. <<<`
    * At this point, you must **manually** enter a phone number in the browser, receive the verification code, and submit it.

4.  **Completion:**
    * Once you complete the phone verification and proceed to the next page, the script will automatically resume, complete the final steps, and save the account details.
    * The process will repeat for the number of accounts you specified.

---

## 📝 Output

Successfully created accounts will be saved in a file named `accounts.txt` in the following format:
```
username@gmail.com:password
```

---

## ⚙️ Configuration

You can easily customize the pool of names used for account generation by editing the `FIRST_NAMES` and `LAST_NAMES` lists at the top of the Python script.

```python
# You can add more names to these lists to increase variety.
FIRST_NAMES = [
    "James", "John", "Robert", "Michael", ...
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", ...
]
```

## 📜 License

This project is licensed under the MIT License. See the `LICENSE` file for details.
