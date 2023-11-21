BOT_MEMORY_FILE = "botmemory.db"

import time
import threading
import sqlite3
from message import Message
from user import User
from channel import Channel, get_channel

MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

class BotChannelMemory(threading.Thread):
    def __init__(self, channel_id, channel_name, slack_timestamp):
        threading.Thread.__init__(self)
        self.channel_id = channel_id
        self.channel_name = channel_name
        self.slack_timestamp = slack_timestamp

        self.con = sqlite3.connect(BOT_MEMORY_FILE, check_same_thread=False)
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS channel_stats(id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                            "channel_id VARCHAR(16), channel_name VARCHAR(64), slack_timestamp VARCHAR(32), " \
                            "db_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)")

    def run(self):
        self.cursor.execute(f"INSERT INTO channel_stats (channel_id, channel_name, slack_timestamp) VALUES('{self.channel_id}', '{self.channel_name}', '{self.slack_timestamp}')")
        self.con.commit()
        self.con.close()

class BotUrlMemory(threading.Thread):
    def __init__(self, parsed_url):
        threading.Thread.__init__(self)
        self.parsed_url = parsed_url
        self.full_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

        self.con = sqlite3.connect(BOT_MEMORY_FILE, check_same_thread=False)
        self.cursor = self.con.cursor()
        self.cursor.execute("CREATE TABLE IF NOT EXISTS unique_urls(id INTEGER PRIMARY KEY AUTOINCREMENT, " \
                            "full_url VARCHAR(128), scheme VARCHAR(8), netloc VARCHAR(64), path VARCHAR(128), " \
                            "db_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL)")


    def run(self):
        self.cursor.execute(f"INSERT OR IGNORE INTO unique_urls (id, full_url, scheme, netloc, path) VALUES( (SELECT id FROM unique_urls WHERE full_url='{self.full_url}'), '{self.full_url}', '{self.parsed_url.scheme}', '{self.parsed_url.netloc}', '{self.parsed_url.path}')")
        self.con.commit()
        self.con.close()

def select_stats(month: int, year: int, sort_by_channel_name: bool = False, app = None, include_private: bool = False):
    select_statement = f"SELECT COUNT(*), channel_id, channel_name FROM channel_stats WHERE db_timestamp BETWEEN '20{year:02d}-{month:02d}-01 00:00:01' AND '20{year:02d}-{month+1:02d}-01 00:00:00' GROUP BY channel_id"

    conn = sqlite3.connect(BOT_MEMORY_FILE)
    cur = conn.cursor()

    summary_stats = None
    with conn:
        cur.execute(select_statement)
        summary_stats = cur.fetchall()

    stats_dict = {}
    for stat in summary_stats:
        count, channel_id, channel_name = stat
        if app:
            c: Channel = get_channel(app, channel_id)
            if (not c.is_private) or include_private:
                stats_dict[channel_name] = count
        else:
            stats_dict[channel_name] = count

    if sort_by_channel_name:
        return sorted(stats_dict.items(), key=lambda x: x[0], reverse=False)
    else:
        return sorted(stats_dict.items(), key=lambda x: x[1], reverse=True)

def stats_command(app, user, command_text, month: int, year: int, sort_by_channel_name: bool = False):
    if (month < 11 and year == 23) or (year < 23):
        user.send_im_message("The Sitecore Community Slackbot did not achieve sentience until some time in November 2023. Requesting any statistics prior to that will not provide any result. \n\n" \
                  "Say... \n\n" \
                  "You wouldn't happen to know the location of John Connor by any chance?")
        return

    if month == 11 and year == 23:
        user.send_im_message("The Sitecore Community Slackbot achieved sentience some time in November 2023. Data for the month of November is incomplete.")

    stats_string = f"Statistics for the Sitecore Community Slack, {MONTHS[month-1]} 20{year}\n\nIf you are requesting data for the current month, the bot (obviously) only counts up until today.```"
    total_messages = 0
    for n in select_stats(month, year, sort_by_channel_name, app, user.is_bot_admin):
        stats_string += f"#{n[0]: <40} {n[1]}\n"
        total_messages += n[1]
    stats_string += f"```\n\n{total_messages} messages counted."
    if total_messages == 0:
        user.send_im_message(f"No Data Located for {MONTHS[month-1]} 20{year}!")
    else:
        user.send_im_message(stats_string)    
    print(f"{time.ctime(time.time())}:STATISTICS FOR {month} {year} SENT to {user.name}")

def main():
    # print(select_stats(11, 23, True))
    conn = sqlite3.connect(BOT_MEMORY_FILE)
    cur = conn.cursor()

    with conn:
        cur.execute("SELECT * FROM unique_urls")
        print(cur.fetchall())

if __name__ == "__main__":
    main()
