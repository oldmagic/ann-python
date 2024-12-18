import feedparser
import requests
import schedule
import time
import logging
from datetime import datetime

# Discord webhook URL
DISCORD_WEBHOOK_URL = 'your_discord_webhook_url_here'

# RSS feed URL
RSS_FEED_URL = 'https://www.animenewsnetwork.com/all/rss.xml?ann-edition=w'

# Set to remember previously sent items
sent_items = set()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fetch_rss_feed(url):
    """
    Fetch and parse the RSS feed from the given URL.

    Args:
        url (str): The URL of the RSS feed.

    Returns:
        feedparser.FeedParserDict: The parsed RSS feed.
    """
    return feedparser.parse(url)

def send_to_discord(webhook_url, message):
    """
    Send a message to the Discord webhook with retry logic for rate limiting.

    Args:
        webhook_url (str): The Discord webhook URL.
        message (str): The message to send.
    """
    data = {
        "content": message
    }
    retry_after = 0
    while True:
        response = requests.post(webhook_url, json=data)
        if response.status_code == 204:
            break
        elif response.status_code == 429:
            retry_after = response.json().get('retry_after', 1)
            logger.warning(f"Rate limited. Retrying after {retry_after} seconds.")
            time.sleep(retry_after)
        else:
            raise ValueError(f"Request to Discord returned an error {response.status_code}, the response is:\n{response.text}")

def process_rss_feed():
    """
    Process the RSS feed, send new items to the Discord webhook, and update the set of sent items.
    Only the 10 latest items are processed.
    """
    feed = fetch_rss_feed(RSS_FEED_URL)
    entries = feed.entries

    # Sort entries by publication date (assuming 'published' or 'updated' field is present)
    entries.sort(key=lambda x: datetime(*x.published_parsed[:6]), reverse=True)

    # Process only the 10 latest items
    for entry in entries[:10]:
        item_id = entry.id  # Assuming each entry has a unique 'id' field
        if item_id not in sent_items:
            message = f"{entry.title}\n{entry.link}"
            send_to_discord(DISCORD_WEBHOOK_URL, message)
            sent_items.add(item_id)

def main():
    """
    Run the RSS feed processing once upon boot and then schedule it to run every 20 minutes.
    """
    # Run the process once upon boot
    process_rss_feed()

    # Schedule the process to run every 20 minutes
    schedule.every(20).minutes.do(process_rss_feed)

    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == "__main__":
    main()
