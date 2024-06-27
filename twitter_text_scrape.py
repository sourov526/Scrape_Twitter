from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller
import os
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Xpaths for login
XPATH_USERNAME_INPUT = '//input[@name="text"]'
XPATH_LOGIN_NEXT_BUTTON = '//*[@id="layers"]//button[2]'
XPATH_PASSWORD_INPUT = '//input[@name="password"]'
XPATH_LOGIN_BUTTON = '//button[@data-testid="LoginForm_Login_Button"]'

# Xpaths for scraping
XPATH_CONTENT = '//article[@data-testid="tweet"]'
XPATH_TEXT = './/div[@data-testid="tweetText"]'

TIME_INTERVAL_EXPLICIT_WAIT = 10


# # Function to set up the WebDriver
# def setup_driver():
#     # Automatically download and install the appropriate ChromeDriver
#     chromedriver_autoinstaller.install()

#     options = webdriver.ChromeOptions()
#     options.add_argument('--headless')  # Run in headless mode
#     options.add_argument("--no-sandbox")
#     options.add_argument("--disable-dev-shm-usage")
#     driver = webdriver.Chrome(options=options)
#     return driver

def setup_driver():
    # Automatically download and install the appropriate ChromeDriver
    chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920x1080')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('start-maximized')
    options.add_argument('enable-automation')
    options.add_argument('--disable-infobars')
    options.add_argument('--disable-extensions')
    options.add_argument('--disable-browser-side-navigation')
    options.add_argument('--disable-notifications')
    driver = webdriver.Chrome(options=options)
    return driver


# Function to log in to Twitter
def login(driver, username, password):
    driver.get("https://twitter.com/login")

    username_input = WebDriverWait(driver, TIME_INTERVAL_EXPLICIT_WAIT).until(
        EC.presence_of_element_located((By.XPATH, XPATH_USERNAME_INPUT))
    )
    username_input.send_keys(username)

    login_next_button = WebDriverWait(driver, TIME_INTERVAL_EXPLICIT_WAIT).until(
        EC.element_to_be_clickable((By.XPATH, XPATH_LOGIN_NEXT_BUTTON))
    )
    login_next_button.click()

    password_input = WebDriverWait(driver, TIME_INTERVAL_EXPLICIT_WAIT).until(
        EC.presence_of_element_located((By.XPATH, XPATH_PASSWORD_INPUT))
    )
    password_input.send_keys(password)

    login_button = WebDriverWait(driver, TIME_INTERVAL_EXPLICIT_WAIT).until(
        EC.element_to_be_clickable((By.XPATH, XPATH_LOGIN_BUTTON))
    )
    login_button.click()

    time.sleep(3)  # Allow some time for the login process to complete


# Function to scrape tweets from a given Twitter URL or account name
def scrape_tweets(driver, url_or_account, page_number=1):
    if "x.com" not in url_or_account:
        url_or_account = f"https://twitter.com/{url_or_account}"

    driver.get(url_or_account)
    time.sleep(3)  # Allow some time for the page to load

    texts = []

    # Scroll and collect tweets
    scroll_height = driver.execute_script("return document.body.scrollHeight")
    for _ in range(page_number):
        # Collect tweet text
        tweet_elements = driver.find_elements(By.XPATH, XPATH_CONTENT)
        for tweet in tweet_elements:
            text = tweet.find_elements(By.XPATH, XPATH_TEXT)
            if len(text) > 0:
                texts.append({"Tweet Text": text[0].text})

        # Scroll down to load more tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)  # Allow some time for new tweets to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == scroll_height:
            break
        scroll_height = new_height
    # driver.quit()
    return texts


# Function to save tweets to a CSV file using pandas
def save_to_csv(tweets, output_folder="output", filename="tweet_text.csv"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, filename)
    df = pd.DataFrame(tweets)
    df.to_csv(output_path, index=False, encoding="utf-8")
    print(f"Data saved to {output_path}")
    return df


# Example usage
if __name__ == "__main__":
    driver = setup_driver()

    # username = "put twitter username"
    # password = "put password here"
    # login(driver, username, password)  # Login to the twitter before login

    url_or_account = "nasa"  # Can be either a URL or an account name
    # url_or_account = "https://x.com/NASA"  # Can be either a URL or an account name
    page_number = 6  # Number of pages to scroll

    texts = scrape_tweets(driver, url_or_account, page_number)
    df = save_to_csv(texts)
    print("Twitter contents:", df)
