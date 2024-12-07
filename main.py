import discord
import os
import sys
import asyncio
import time
import ezcord
from dotenv import load_dotenv

load_dotenv(dotenv_path="./botconfig/.env")

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

class ShardedBot(ezcord.Bot):
    def __init__(self):
        super().__init__(
            intents=intents,
            language="de",
            auto_shard=True  # Enable auto-sharding
        )
        self.start_time = time.time()
        self.total_guilds = 0
        print("Bot starting with auto-sharding...")

    async def on_ready(self):
        """Wenn der Bot bereit ist, wird die Anzahl der Guilds und der Shard-Status ausgegeben."""
        print(f"\nBot is ready! Connected to {len(self.guilds)} servers")
        print(f"Shard info: {self.shard_count} shards")

        while True:
            server_count = len(self.guilds)
            total_members = sum(guild.member_count for guild in self.guilds)

            if server_count >= 100:
                target_server_count = 100
            elif server_count >= 75:
                target_server_count = 100
            elif server_count >= 50:
                target_server_count = 75
            elif server_count >= 25:
                target_server_count = 50
            else:
                target_server_count = 25

            activity_text = f'{server_count}/{target_server_count}'
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.playing, name="/help"))
            await asyncio.sleep(30)
            await self.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{total_members} 🍀 | {activity_text}🌍 "))
            await asyncio.sleep(30)

if __name__ == "__main__":
    bot = ShardedBot()
    bot.load_cogs(subdirectories=True)
    bot.add_help_command()
    bot.run()
