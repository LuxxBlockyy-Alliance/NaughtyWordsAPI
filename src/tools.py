import re

import aiosqlite
import asyncio
import aiofiles
import os
import time
from rich.console import Console

console = Console()


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


async def get_column(database_name: str, table_name: str, column: str):
    conn = await aiosqlite.connect(database_name)
    cursor = await conn.cursor()
    try:
        await cursor.execute(f'SELECT {column} FROM {table_name}')
    except aiosqlite.OperationalError:
        print("Sqlite get column Failed")
    data = await cursor.fetchall()
    await conn.commit()
    await cursor.close()
    await conn.close()
    if not data:
        return
    else:
        return data


async def write_data(db_path, path: str = "./words/", file_names: list = None):
    if file_names is None:
        file_names = ["ar", "cs", "da", "de", "en", "eo", "es", "fa", "fi", "fil", "fr", "fr-CA-u-sd-caqc", "hi", "hu",
                      "it", "ja", "kab", "ko", "nl", "no", "pl", "pt", "ru", "sv", "th", "tlh", "tr", "zh"]
    countdown = Countdown()
    countdown.count_start()
    file_paths = []
    for file_name in file_names:
        file_paths.append(os.path.join(path, file_name))

    for file_path in file_paths:
        print(file_path)
        async with aiofiles.open(file_path, "r", encoding="utf-8") as file_object:
            while line := await file_object.readline():
                connection = await aiosqlite.connect(db_path)
                cursor = await connection.cursor()
                await cursor.execute("CREATE TABLE IF NOT EXISTS words (word TEXT)")
                await cursor.execute(f"INSERT INTO words VALUES (?)", (line.strip(),))
                await connection.commit()
                await connection.close()
    countdown.count_stop()
    print(countdown.counted_time())


async def scan_db(db_path, message: str):
    connection = await aiosqlite.connect(db_path)
    cursor = await connection.cursor()
    result = None
    for row in await get_column(db_path, "words", "word"):
        try:
            result = re.search(row[0], message)
            if result:
                break
        except Exception as e:
            console.log(e)
    if result:
        return True
    else:
        return False