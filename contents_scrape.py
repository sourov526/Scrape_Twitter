from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller

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

# Function to scrape tweets from a given Twitter URL or account name
def scrape_tweets(url_or_account):
    driver = setup_driver()
    if 'twitter.com' not in url_or_account:
        url_or_account = f"https://twitter.com/{url_or_account}"
    
    driver.get(url_or_account)
    time.sleep(5)  # Allow some time for the page to load

    tweets = []
    
    # Scroll and collect tweets
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Collect tweets
        tweet_elements = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
        for tweet in tweet_elements:
            try:
                content = tweet.find_element(By.XPATH, ".//div[2]/div[2]/div[1]").text
                tweets.append(content)
            except Exception as e:
                print("Error reading tweet:", e)
                continue
        
        # Scroll down to load more tweets
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)  # Allow some time for new tweets to load

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # driver.quit()
    return tweets

# Example usage
if __name__ == "__main__":
    url_or_account = "nasa"  # Can be either a URL or an account name
    tweets = scrape_tweets(url_or_account)
    for tweet in tweets:
        print(tweet)
    
    # quit the browser by pressing enter
    input("Press Enter to quit-------------")
