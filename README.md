# Internship Notificator

A Python script that monitors the FIB UPC internship board through web scrapping and sends notifications for new job postings using Pushover.

## Features

- Monitors FIB UPC's internship board every 30 minutes during working hours
- Sends push notifications for new job postings via Pushover
- Runs automatically using GitHub Actions
- Notification includes job title, location, and direct link to the posting

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Configuration

1. Create a Pushover account at [pushover.net](https://pushover.net)
2. Get your User Key from Pushover
3. Create a new Application in Pushover to get an API Token
4. Add these secrets to your GitHub repository:
   - `PUSH_API_KEY`: Your Pushover API Token
   - `USER_KEY`: Your Pushover User Key

## Running Locally

To run the script locally, set the following environment variables:
```bash
export PUSH_USER_KEY='your-user-key'
export PUSH_API_KEY='your-api-token'
python job_notifier.py
```

## GitHub Actions

The script runs automatically through GitHub Actions:
- Every 30 minutes from 8:00 to 18:00 (UTC+2)
- Monday through Friday
- Can also be triggered manually through workflow_dispatch

## License

MIT License
