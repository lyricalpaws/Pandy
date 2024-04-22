import time
import discord
from discord.ext import commands
from utils import default, permissions


class info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command()
    async def ping(self, ctx):
        """ Pong! """
        before = time.monotonic()
        message = await ctx.send("*Pokes back*")
        ping = (time.monotonic() - before) * 1000
        await message.edit(
            content=f"*Pokes back*%re\n`MSG :: {int(ping)}ms\nAPI :: {round(self.bot.latency * 1000)}ms`"
        )


async def setup(bot):
    await bot.add_cog(info(bot))