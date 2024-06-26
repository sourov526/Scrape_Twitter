from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import chromedriver_autoinstaller
import os
import csv
import pandas as pd


# All Xpaths
XPATH_CONTENT = '//article[@data-testid="tweet"]'
XPATH_TEXT = './/div[@data-testid="tweetText"]'
XPATH_REPLY_COUNT = './/button[@data-testid="reply"]'
XPATH_REPOST_COUNT = './/button[@data-testid="retweet"]'
XPATH_FAVORITE_COUNT = './/button[@data-testid="like"]'
XPATH_VIEWS_COUNT = './/a[contains(@aria-label, "View post analytics")]'

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
    created_at = []
    links = []
    texts = []
    reply_counts = []
    repost_counts = []
    favorite_counts = []
    views_counts = []

    
    # Scroll and collect tweets
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # Collect tweets
        tweet_elements = driver.find_elements(By.XPATH, XPATH_CONTENT)
        for tweet in tweet_elements:
            try:
                # content = tweet.find_element(By.XPATH, ".//div[2]/div[2]/div[1]").text
                text = tweet.find_elements(By.XPATH, XPATH_TEXT)[0].text
                texts.append(text)

                reply_count = tweet.find_elements(By.XPATH, XPATH_REPLY_COUNT)[0].text
                reply_counts.append(reply_count)

                repost_count = tweet.find_elements(By.XPATH, XPATH_REPOST_COUNT)[0].text
                repost_counts.append(repost_count)

                favorite_count = tweet.find_elements(By.XPATH, XPATH_FAVORITE_COUNT)[0].text
                favorite_counts.append(favorite_count)

                views_count = tweet.find_elements(By.XPATH, XPATH_VIEWS_COUNT)[0].text
                views_counts.append(views_count)

                tweets.append({
                    "Reply Count": reply_count,
                    "repost_count": repost_count,
                    "favorite_count": favorite_count,
                    "views_count": views_count,
                    "text": text
                })

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
    
    print("Length of text list: ", len(texts))
    print("Text list : ", texts)

    print("Length of reply count: ", len(reply_counts))
    print("Reply count list : ",reply_counts)

    print("Length of repost count: ", len(repost_counts))
    print("Repost count list : ",repost_counts)

    print("Length of favorite count: ", len(favorite_counts))
    print("Favorite count list : ",favorite_counts)

    print("Length of views count: ", len(views_counts))
    print("Views count list : ",views_counts)

    # driver.quit()
    return tweets

# # Function to save tweets to a CSV file
# def save_to_csv(tweets, output_folder="output", filename="tweets.csv"):
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
    
#     output_path = os.path.join(output_folder, filename)
#     with open(output_path, mode='w', newline='', encoding='utf-8') as file:
#         writer = csv.DictWriter(file, fieldnames=["text", "reply_count", "repost_count", "favorite_count", "views_count"])
#         writer.writeheader()
#         for tweet in tweets:
#             writer.writerow(tweet)
#     print(f"Data saved to {output_path}")

# Function to save tweets to a CSV file using pandas
def save_to_csv(tweets, output_folder="output", filename="tweets.csv"):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    output_path = os.path.join(output_folder, filename)
    df = pd.DataFrame(tweets)
    df.to_csv(output_path, index=False, encoding='utf-8')
    print(f"Data saved to {output_path}")
    return df

# Example usage
if __name__ == "__main__":
    url_or_account = "nasa"  # Can be either a URL or an account name
    # scrape_tweets(url_or_account)
    # for tweet in tweets:
    #     print(tweet)

    tweets = scrape_tweets(url_or_account)
    df = save_to_csv(tweets)
    print("Twitter contents : ", df)
    
    # quit the browser by pressing enter
    input("Press Enter to quit-------------")
