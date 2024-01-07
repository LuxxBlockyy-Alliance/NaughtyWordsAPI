import re

import aiosqlite
import asyncio
import aiofiles
import os
import time
from rich.console import Console

console = Console()


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
                    console.log(message.lower())
                    if result:
                        break
        except Exception as e:
            console.log(e)
    if result:
        return True
    else:
        return False
