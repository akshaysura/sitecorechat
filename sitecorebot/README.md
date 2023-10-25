# How to run

## If you've never done any Python

1. Install Python -> `winget install -e --id Python.Python.3.11`
2. Restart your shell

Done. That's all the steps.

## Install requirements
1. Install required modules -> `pip install -r requirements.txt`
2. Create .env file

        SLACK_BOT_TOKEN= Copy this from OAuth Tokens for Your Workspace on https://api.slack.com/apps/A062D72K36J/oauth?
        SLACK_APP_TOKEN= Copy this from App-Level Tokens -> sitecore_community_slackbot_token on https://api.slack.com/apps/A062D72K36J/general

3. And then run the bot. Either directly -> `python app.py` or open `code app.py` and run it via the "Play" button top right. F5 probably also works.

## Profit!

# API Documentation

- Bolt API (from Slack) -> https://slack.dev/bolt-python/tutorial/getting-started