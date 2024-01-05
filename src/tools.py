import re

import aiosqlite
import asyncio
from git import Repo
import aiofiles
import os
import time
from rich.console import Console

console = Console()
data_path = "./words/"


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


async def clone_repo(url, destination):
    try:
        repo = Repo.clone_from(url, destination)
        print(f"Successfully cloned the repository: {url}")
    except Exception as e:
        print(f"Error cloning the repository: {e}")


async def update():
    if os.path.exists(data_path):
        os.remove(data_path)
    await clone_repo("https://github.com/blockplacer4/List-of-Dirty-Naughty-Obscene-and-Otherwise-Bad-Words.git", data_path)
    elapsed_time = await write_data("./words.db", data_path, None)
    console.log(f"[[green bold]![/green bold]] Update complete in {elapsed_time}")


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


async def write_data(db_path, path: str = f"{data_path}", file_names: list = None):
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
    return countdown.counted_time()


async def scan_db(db_path, message: str):
    connection = await aiosqlite.connect(db_path)
    cursor = await connection.cursor()
    result = None
    for row in await get_column(db_path, "words", "word"):
        try:
            if row[0] == message:
                if message == "nicht":
                    return False
                else:
                    result = re.search(row[0], message.lower())
                    if result:
                        break
        except Exception as e:
            console.log(e)
    if result:
        return True
    else:
        return False
