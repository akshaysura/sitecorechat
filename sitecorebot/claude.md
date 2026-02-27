# Sitecore Community Slackbot

## Overview

A Python-based Slack bot for managing the Sitecore Community Slack workspace (~10,000 members). Built with Slack Bolt framework using Socket Mode for real-time event processing.

## Tech Stack

- **Python 3.11**
- **Slack Bolt** - Slack app framework
- **SQLite** - Local database (`botmemory.db`)
- **Socket Mode** - Real-time bidirectional Slack connection
- **SendGrid** - Email delivery
- **thefuzz** - Fuzzy string matching for duplicate detection

## Architecture

### Entry Point
- `app.py` - Main application, registers all event handlers

### Core Components
| File | Purpose |
|------|---------|
| `message.py` | Message wrapper class with helper properties |
| `user.py` | User management, admin/coordinator definitions, caching |
| `channel.py` | Channel abstraction |
| `bot_command_handler.py` | Command dispatcher for `/communitybot` |
| `bot_commands.py` | Individual command implementations |
| `bot_memory.py` | SQLite database for stats and URL tracking |

### Feature Modules
| File | Purpose |
|------|---------|
| `crosspost_guardian.py` | Detects duplicate messages across channels (fuzzy matching) |
| `mention_guardian.py` | Warns users who @ mention others (Rule #4) |
| `welcome.py` | New user welcome messages and rules display |
| `new_user_request.py` | Monitors signups, detects duplicate accounts |
| `reaction_handler.py` | Triggers workflows on specific emoji reactions |
| `url_scanner.py` | Logs all URLs shared in messages |
| `invite_requested.py` | Handles workspace invite requests |
| `usergroup_monitor.py` | Meeting URL detection (experimental) |

## Permission System

Defined in `user.py`:
- **Bot Admins** (8 users) - Full access to all commands
- **Community Coordinators** (2 users) - Elevated privileges (user lookup, etc.)
- **Regular Users** - Basic commands only

## Community Rules

1. Engage and share
2. Check Sitecore Stack Exchange first
3. Don't cross-post questions
4. Don't tag people (volunteers)
5. Keep on-topic (Sitecore only)

## Available Commands

| Command | Access | Description |
|---------|--------|-------------|
| `help` | All | List available commands |
| `joke` | All | Random joke |
| `rules` | All | Community guidelines |
| `welcome` | All | Show welcome message |
| `admins` | All | List community admins |
| `feedback` | All | Submit anonymous feedback |
| `channels` | All | Bot's active channels |
| `stats` | All | Message statistics by channel/month |
| `lookup` | Coordinators+ | User info lookup |
| `allchannels` | Admins | Full channel list |
| `changelog` | Admins | Bot version history |

## Configuration

Environment variables (`.env`):
- `SLACK_BOT_TOKEN` - Bot user OAuth token
- `SLACK_APP_TOKEN` - App-level token for Socket Mode
- `SENDGRID_API_KEY` - For sending emails

Key channel IDs are hardcoded in various modules (moderation channel, welcome channel, etc.).

---

## Changelog

### v0.5.1
- **New Feature: `:rules:` Reaction Handler**
  - React with `:rules:` on any message to send the poster a DM with community rules
  - Admins/coordinators/trusted users trigger immediately
  - Regular users need 3+ reactions before it triggers
  - Includes intro message referencing the flagged post, followed by full rules
  - Logs action to carbon copy channel

### v0.5.0
- **New Feature: Mention Guardian** (`mention_guardian.py`)
  - Detects when users @ mention other members in channel messages
  - Sends ephemeral (private) reminder about Rule #4
  - Includes "Show me all the rules" button that triggers full rules display
  - 24-hour cooldown per user to avoid repeated warnings
  - Bot admins and community coordinators are exempt
  - Additional exempt users can be configured via `ADDITIONAL_EXEMPT_USERS`

### v0.4.9 (December 6, 2023)
- Added reaction handler with `:snippets:` workflow

### Previous versions
See `changelog.txt` for earlier history.

---

## Session Notes

### 2026-02-27

**Features implemented:**
- Mention Guardian (v0.5.0) - ephemeral Rule #4 reminders when users @ mention others
- `:rules:` reaction handler (v0.5.1) - sends community rules DM when message flagged

**Infrastructure:**
- Created `claude.md` for project documentation
- Updated `.gitignore` to exclude `botmemory.db` and `.claude/`
- Removed `botmemory.db` from git tracking (file preserved locally)
- Set up local git identity for commits

**Explored but parked:**
- kapa.ai MCP integration (`sitecore.mcp.kapa.ai`) for documentation queries
  - Would require API key from Sitecore's kapa.ai instance
  - Could enable `@communitybot what's the latest version of X?` queries
  - Contact Tamas Varga (U0BAH3W05) for API access if revisiting

**Deployment:**
- Bot runs on Azure VM (`cassidy-ubuntu`) in tmux session
- Path: `~/git/sitecorechat/sitecorebot/`
- Start: `tmux new -s bot` then `python3 app.py`
- Detach: `Ctrl+b d`

**Useful tmux commands:**
- `tmux ls` - list sessions
- `tmux attach -t bot` - reattach
- `Ctrl+b [` - scroll mode (q to exit)

---

## Future Improvements (Parked)

### Automated Deployment via GitHub Actions

Current setup: Manual SSH via Azure Portal CLI, tmux session.

**Recommended approach: Self-hosted GitHub Runner**
1. Install GitHub Actions runner on the Azure VM
2. Jobs run directly on the VM (no SSH/credentials needed)
3. Combined with systemd service for proper process management

**systemd service** (`/etc/systemd/system/sitecorebot.service`):
```ini
[Unit]
Description=Sitecore Community Slackbot
After=network.target

[Service]
Type=simple
User=mark@cassidy.dk
WorkingDirectory=/home/mark@cassidy.dk/git/sitecorechat/sitecorebot
ExecStart=/usr/bin/python3 app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**GitHub Action** (`.github/workflows/deploy.yml`):
```yaml
name: Deploy
on:
  push:
    branches: [master]
    paths: ['sitecorebot/**']

jobs:
  deploy:
    runs-on: self-hosted
    steps:
      - name: Pull and restart
        run: |
          cd ~/git/sitecorechat
          git pull
          sudo systemctl restart sitecorebot
```

**Alternative:** Use `az vm run-command` if self-hosted runner isn't desired (requires Azure service principal credentials in GitHub secrets).
