import json
import random
import discord
from urllib.request import urlopen, Request
from discord.ext import commands
from utils import default


class misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def fox(self, ctx):
        """ Posts a random fox. """
        try:
            response=urlopen(Request("https://randomfox.ca/floof/", headers={'User-Agent': 'Mozilla'}))
            data_json = json.loads(response.read())
        except json.JSONDecodeError:
            return await ctx.send("I couldn't contact the api ;-;")
        await ctx.send(data_json['image'])

    @commands.command()
    @commands.cooldown(rate=1, per=5.0, type=commands.BucketType.user)
    async def bunny(self, ctx):
        """ Posts a random bunny. """
        try:
            response=urlopen(Request("https://api.bunnies.io/v2/loop/random/?media=gif", headers={'User-Agent': 'Mozilla'}))
            data_json = json.loads(response.read())
        except json.JSONDecodeError:
            return await ctx.send("I couldn't contact the api ;-;")
        await ctx.send(data_json['media']['gif'])

    @commands.command()
    @commands.guild_only()
    async def colour(self, ctx):
        """ Gives a random hex value. """
        randomHex = random.randint(0, 16777215)
        hexString = str(hex(randomHex))
        hexNumber = hexString[2:]
        embed = discord.Embed(title=f"#{hexNumber}", url=f"https://www.color-hex.com/color/{hexNumber}", colour=randomHex)
        await ctx.reply(embed=embed)


async def setup(bot):
    await bot.add_cog(misc(bot))