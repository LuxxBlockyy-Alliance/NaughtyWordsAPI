import aiosqlite
import asyncio
import aiofiles
import os
import time
import json


# ["ar", "cs", "da", "de", "en", "eo", "es", "fa", "fi", "fil", "fr", "fr-CA-u-sd-caqc", "hi", "hu", "it", "ja",
# "kab", "ko", "nl", "no", "pl", "pt", "ru", "sv", "th", "tlh", "tr", "zh"]

class Countdown:
    def __init__(self):
        self.start_time = None
        self.end_time = None

    def count_start(self):
        self.start_time = time.time()

    def count_stop(self):
        self.end_time = time.time()

    def counted_time(self):
        if self.end_time is None:
            return "Countdown was never started or completed."
        else:
            return self.end_time - self.start_time


async def write_data(db_path, path: str = "./words/", file_names: list = None):
    countdown = Countdown()
    countdown.count_start()

    with open('build.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

        for key in data:
            for word in data[key]:
                print(word)
                connection = await aiosqlite.connect(db_path)
                cursor = await connection.cursor()
                await cursor.execute("CREATE TABLE IF NOT EXISTS words (word TEXT)")
                await cursor.execute(f"INSERT INTO words VALUES (?)", (word.strip(),))
                await connection.commit()
                await connection.close()

    countdown.count_stop()
    print(countdown.counted_time())


asyncio.run(write_data("words.db"))
