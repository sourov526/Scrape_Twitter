# Create virtual environment
python -m venv env_name
# Activate the env
source env_name/bin/activate
# install the requirements
pip install -r requirements.txt

# Now run twitter_text_scrape.py for Scraping
python twitter_text_scrape.py

# After scraping if you want to deactivate the env, run:
deactivate