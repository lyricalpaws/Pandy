import discord
import json
import os
import asyncio
from discord.ext import commands
from discord import Intents

# Get config.json
with open("config.json", "r") as config:
    data = json.load(config)
    prefix = data["prefix"]

# Define the activity then create the bot client
activity = discord.Activity(name=f'for {prefix}help', type=discord.ActivityType.watching)
bot = commands.Bot(prefix, intents=Intents.all(), activity=activity)

# Once ready, print out that it is ready
@bot.event
async def on_ready():
    print(f"We have logged in as {bot.user}")
    print(discord.__version__)

async def main():
    async with bot:
        try:
            print("Logging in...")
            for file in os.listdir("cogs"):
                if file.endswith(".py"):
                    name = file[:-3]
                    await bot.load_extension(f"cogs.{name}")
            await bot.start(data['token'])
        except KeyboardInterrupt:
            bot.close()

asyncio.run(main())