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

# Information

The rss.py script is a Python application designed to fetch and process an RSS feed, send the latest items to a Discord webhook, and ensure that duplicate items are not sent. The script is highly performant and concise, adhering to best practices for modular design, error handling, and documentation. Here's a detailed description of the script:

Purpose
The primary purpose of rss.py is to:

Fetch an RSS feed at regular intervals.
Send the latest items from the feed to a Discord webhook.
Ensure that duplicate items are not sent by remembering previously sent items.
Handle rate limiting by implementing a retry mechanism with exponential backoff.
Features
RSS Feed Fetching: The script uses the feedparser library to parse the RSS feed.
Discord Integration: The script sends messages to a Discord webhook using the requests library.
Scheduling: The script uses the schedule library to run the RSS feed processing at regular intervals (every 20 minutes).
Rate Limiting Handling: The script implements a retry mechanism with exponential backoff to handle rate limiting from the Discord API.
Duplicate Item Avoidance: The script maintains a set of previously sent items to avoid sending duplicates.
Modules and Functions
fetch_rss_feed(url):

Purpose: Fetches and parses the RSS feed from the given URL.
Arguments:
url (str): The URL of the RSS feed.
Returns:
feedparser.FeedParserDict: The parsed RSS feed.
send_to_discord(webhook_url, message):

Purpose: Sends a message to the Discord webhook with retry logic for rate limiting.
Arguments:
webhook_url (str): The Discord webhook URL.
message (str): The message to send.
Logic:
Sends a POST request to the Discord webhook.
If the request is rate-limited (status code 429), waits for the specified retry_after time before retrying.
Logs a warning message when rate-limited.
Raises a ValueError if the request returns an error other than rate limiting.
process_rss_feed():

Purpose: Processes the RSS feed, sends new items to the Discord webhook, and updates the set of sent items. Only the 10 latest items are processed.
Logic:
Fetches the RSS feed.
Sorts the feed entries by publication date.
Iterates through the 10 latest entries.
Checks if the item has been sent before using its unique ID.
Sends the item to Discord if it hasn't been sent before.
Adds the item ID to the set of sent items.
main():

Purpose: Runs the RSS feed processing once upon boot and then schedules it to run every 20 minutes.
Logic:
Runs process_rss_feed once upon boot.
Uses the schedule library to run process_rss_feed every 20 minutes.
Keeps the script running indefinitely to check for pending tasks.
