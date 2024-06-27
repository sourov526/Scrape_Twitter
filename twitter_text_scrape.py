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

# Function to set up the WebDriver
def setup_driver():
    # Automatically download and install the appropriate ChromeDriver
    chromedriver_autoinstaller.install()

    options = webdriver.ChromeOptions()
    # options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome(options=options)
    return driver

# Function to log in to Twitter
def login(driver, username, password):
    driver.get("https://twitter.com/login")
    # time.sleep(10)  # Allow some time for the page to load

    username_input = WebDriverWait(
        driver, TIME_INTERVAL_EXPLICIT_WAIT
    ).until(
        EC.presence_of_element_located(
            (By.XPATH, XPATH_USERNAME_INPUT)
        )
    )
    # username_input = driver.find_element(By.XPATH, XPATH_USERNAME_INPUT)
    username_input.send_keys(username)
    # time.sleep(2)

    login_next_button = WebDriverWait(
        driver, TIME_INTERVAL_EXPLICIT_WAIT
    ).until(
        EC.element_to_be_clickable((By.XPATH, XPATH_LOGIN_NEXT_BUTTON))
    )
    # login_next_button = driver.find_element(By.XPATH, XPATH_LOGIN_NEXT_BUTTON)
    login_next_button.click()
    # time.sleep(10)


    password_input = WebDriverWait(
        driver, TIME_INTERVAL_EXPLICIT_WAIT
    ).until(
        EC.presence_of_element_located(
            (By.XPATH, XPATH_PASSWORD_INPUT)
        )
    )
    # password_input = driver.find_element(By.XPATH, XPATH_PASSWORD_INPUT)
    password_input.send_keys(password)


    login_button = WebDriverWait(
        driver, TIME_INTERVAL_EXPLICIT_WAIT
    ).until(EC.element_to_be_clickable((By.XPATH, XPATH_LOGIN_BUTTON)))
    # login_button = driver.find_element(By.XPATH, XPATH_LOGIN_BUTTON)
    login_button.click()
    
    time.sleep(5)  # Allow some time for the login process to complete


# Function to scrape tweets from a given Twitter URL or account name
def scrape_tweets(driver, url_or_account, page_number=1):
    if 'twitter.com' not in url_or_account:
        url_or_account = f"https://twitter.com/{url_or_account}"
    
    driver.get(url_or_account)
    time.sleep(5)  # Allow some time for the page to load

    texts = []

    # Scroll and collect tweets
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    
    for _ in range(page_number):
        # Collect tweets
        tweet_elements = driver.find_elements(By.XPATH, XPATH_CONTENT)
        for tweet in tweet_elements:
            text = tweet.find_elements(By.XPATH, XPATH_TEXT)
            if len(text) > 0:
                texts.append({
                    "Texts": text[0].text
                })
        
        # Scroll down to load more tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(5)  # Allow some time for new tweets to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        print("new_scroll height : ", new_height)
        if new_height == last_height:
            break
        last_height = new_height

    driver.quit()
    return texts

# Function to save tweets to a CSV file using pandas
def save_to_csv(tweets, output_folder="output", filename="tweet_texts.csv"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, filename)
    df = pd.DataFrame(tweets)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Data saved to {output_path}")
    return df

# Example usage
if __name__ == "__main__":

    driver = setup_driver()

    username='optionaluser151'
    password='123Sourov'
    login(driver, username, password) # Login to the twitter before login

    url_or_account = "nasa"  # Can be either a URL or an account name
    # url_or_account = "elonmusk"  # Can be either a URL or an account name
    page_number = 5  # Number of pages to scroll

    texts = scrape_tweets(driver, url_or_account, page_number)
    df = save_to_csv(texts)
    print("Twitter contents:", df)
    
    # quit the browser by pressing enter
    input("Press Enter to quit-------------")






        # # Scroll down to load more tweets
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # # print("show the scroll height : ", last_height)
        # # driver.execute_script("window.scrollTo(0, arguments[0]);", last_height)
        # time.sleep(5)  # Allow some time for new tweets to load