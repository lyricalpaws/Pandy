import json
import random
import discord
from random import randint
from aiohttp import ClientSession
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
    async def colour(self, ctx):
        """ Gives a random hex value. """
        randomHex = random.randint(0, 16777215)
        hexString = str(hex(randomHex))
        hexNumber = hexString[2:]
        embed = discord.Embed(title=f"#{hexNumber}", url=f"https://www.color-hex.com/color/{hexNumber}", colour=randomHex)
        await ctx.reply(embed=embed)

    @commands.command()
    async def xkcd(self, ctx, number: str = None):
        """
        Fetches xkcd comics.
        If number is left blank, automatically fetches the latest comic.
        If number is set to '?', a random comic is fetched.
        """

        # Creates endpoint URI
        if number is None or number == "?":
            endpoint = "https://xkcd.com/info.0.json"
        else:
            endpoint = f"https://xkcd.com/{number}/info.0.json"

        # Fetches JSON data from endpoint
        async with ClientSession() as session:
            async with session.get(endpoint) as response:
                data = await response.json()

        # Updates comic number
        if number == "?":
            number = randint(1, int(data["num"]))  # noqa: B311
            endpoint = f"https://xkcd.com/{number}/info.0.json"
            async with ClientSession() as session:
                async with session.get(endpoint) as response:
                    data = await response.json()
        else:
            number = data["num"]

        # Creates date object (Sorry, but I'm too tired to use datetime.)
        date = f"{data['day']}/{data['month']}/{data['year']}"

        # Creates Rich Embed, populates it with JSON data and sends it.
        comic = discord.Embed()
        comic.title = data["safe_title"]
        comic.set_footer(text=data["alt"])
        comic.set_image(url=data["img"])
        comic.url = f"https://xkcd.com/{number}"
        comic.set_author(
            name="xkcd",
            url="https://xkcd.com/",
            icon_url="https://xkcd.com/s/0b7742.png",
        )
        comic.add_field(name="Number:", value=number)
        comic.add_field(name="Date:", value=date)
        comic.add_field(name="Explanation:", value=f"https://explainxkcd.com/{number}")

        await ctx.send(embed=comic)

    @commands.command(aliases=["flip", "coin"])
    async def coinflip(self, ctx):
        """ Coinflip! """
        coinsides = ["Heads", "Tails"]
        await ctx.reply(f"**{ctx.author.name}** flipped a coin and got **{random.choice(coinsides)}**!")

async def setup(bot):
    await bot.add_cog(misc(bot))