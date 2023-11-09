BOT_MEMORY_FILE = "botmemory.db"

import threading
import sqlite3

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

def main():
    conn = sqlite3.connect(BOT_MEMORY_FILE)
    cur = conn.cursor()

    with conn:
        cur.execute("SELECT * FROM channel_stats")
        print(cur.fetchall())

if __name__ == "__main__":
    main()
