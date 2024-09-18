import requests
import os
from datetime import datetime

# qBittorrent Web UI details
#QB_HOST = 'http://localhost:8080'  # Change the port as necessary
QB_HOST = 'http://qnapnas:25000'
QB_USERNAME = 'admin'              # Change to your qBittorrent username
QB_PASSWORD = 'password'           # Change to your qBittorrent password

# Constants
ONE_GB = 1 * 1024 * 1024 * 1024  # 1 GB in bytes
HOME_DIR = os.getenv('HOME_DIR') or os.getenv('HOME')
TRACKING_FILE = os.path.join(HOME_DIR,'PythonScripts/downloaded_today.txt')

# Log in to qBittorrent
def login():
    session = requests.Session()
    login_url = f'{QB_HOST}/api/v2/auth/login'
    login_data = {
        'username': QB_USERNAME,
        'password': QB_PASSWORD
    }
    response = session.post(login_url, data=login_data)

    if response.status_code == 200 and response.text == "Ok.":
        print("Logged in successfully.")
        return session
    else:
        raise Exception("Failed to log in. Check your credentials and qBittorrent settings.")

# Get torrent information from qBittorrent
def get_torrent_info(session):
    torrents_url = f'{QB_HOST}/api/v2/torrents/info'
    response = session.get(torrents_url)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception("Failed to retrieve torrent info.")

# Load previously downloaded data from file
def load_previous_downloaded_data():
    try:
        with open(TRACKING_FILE, 'r') as f:
            data = f.read()
            last_date, last_downloaded = data.split(',')
            return last_date, int(last_downloaded)
    except FileNotFoundError:
        # If file does not exist, assume it's the first run of the day
        return None, 0

# Save downloaded data to file
def save_downloaded_data(total_downloaded):
    today = datetime.now().strftime('%Y-%m-%d')
    with open(TRACKING_FILE, 'w') as f:
        f.write(f"{today},{total_downloaded}")

# Pause all torrents
def pause_all_torrents(session):
    pause_url = f'{QB_HOST}/api/v2/torrents/pause'
    response = session.post(pause_url)

    if response.status_code == 200:
        print("All torrents paused successfully.")
    else:
        raise Exception("Failed to pause torrents.")

# Check how much data has been downloaded today
def check_downloaded_data():
    session = login()
    torrents = get_torrent_info(session)

    today = datetime.now().strftime('%Y-%m-%d')

    # Get the previous data if it exists
    last_date, last_downloaded = load_previous_downloaded_data()

    # Total data downloaded right now
    total_downloaded_now = sum(torrent.get('downloaded', 0) for torrent in torrents)

    if last_date == today:
        # Calculate only the data downloaded today
        downloaded_today = total_downloaded_now - last_downloaded
    else:
        # First run of the day, track total
        downloaded_today = total_downloaded_now

    print(f"Total downloaded today: {downloaded_today / (1024 * 1024)} MB")

    # Save current total downloaded data for future runs
    save_downloaded_data(total_downloaded_now)

    if downloaded_today >= ONE_GB:
        print("More than 1GB has been downloaded today.")
        pause_all_torrents(session)

if __name__ == '__main__':
    check_downloaded_data()