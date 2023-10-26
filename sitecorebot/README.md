# How to run
This assumes you've already cloned the repository or otherwise have it on your local machine.

## If you've never done any Python on your machine:

### Windows
1. Install Python -> `winget install -e --id Python.Python.3.11`
2. Restart your shell (might not even be needed. If you can run 'python' from the command-line after winget, you're all set)

### Linux
1. `sudo apt update`
2. `sudo apt install python3`

Done. That's all the steps.

## Install requirements
1. Install required modules -> `pip install -r requirements.txt`
2. Create .env file

        SLACK_BOT_TOKEN= Copy this from OAuth Tokens for Your Workspace on https://api.slack.com/apps/A062D72K36J/oauth?
        SLACK_APP_TOKEN= Copy this from App-Level Tokens -> sitecore_community_slackbot_token on https://api.slack.com/apps/A062D72K36J/general

3. And then run the bot. Either directly -> `python app.py` or open `code app.py` and run it via the "Play" button top right. F5 probably also works.

## Profit!
The bot is (currently) configured to run in [https://api.slack.com/apis/connections/socket](Sockets Mode), so no further configuration is required. It will connect directly to Slack's API servers and get to work.

## API Documentation

- Bolt API (from Slack) -> https://slack.dev/bolt-python/tutorial/getting-started
