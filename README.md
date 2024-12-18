# ann-python
animenewsnetwork rss feedser that sends all the information to an discord webhook

# Setup
python3 -m venv venv
source venv/bin/activate
pip install feedparser requests schedule

# Edit
Edit 'DISCORD_WEBHOOK_URL' in rss.py.
Paste the discord webhook link inside 'DISCORD_WEBHOOK_URL'

# Run
python rss.py
