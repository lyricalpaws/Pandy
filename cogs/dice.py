import dndice
from discord.ext import commands
from utils import default


class dice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command(aliases=["r"])
    async def roll(self, ctx, *, dicerolls: str = None):
        """ Rolls dice using the format xdx. """
        if dicerolls is None:
            return await ctx.reply("Please input a dice formula. This bot runs on dndice, find the formatting @ <https://github.com/the-nick-of-time/dndice>")
        result = dndice.verbose(dicerolls)
        await ctx.reply(result)

    @commands.command(aliases=["dndchar"])
    async def randchar(self, ctx):
        """ Rolls 4d6 and keeps the highest 3; does it 6 times. """
        diceResult = []
        for _ in range(6):
            # Roll 4 d6 dice, and keep the highest 3, append each result to diceResult.
            result = dndice.verbose("4d6h3")
            diceResult.append(result)
        # Create a format spec for each item in the input `alist`.
        # E.g., each item will be right-adjusted, field width=3.
        format_list = ['{:>3}' for item in diceResult]

        # Now join the format specs into a single string:
        # E.g., '{:>3}, {:>3}, {:>3}' if the input list has 3 items.
        s = '\n'.join(format_list)

        # Now unpack the input list `alist` into the format string. Done!
        finalResult = s.format(*diceResult)
        await ctx.reply(finalResult)

    @commands.command(aliases=["rrr"])
    async def iterroll(self, ctx, iterations: int = None, *, dicerolls: str = None):
        """ Roll but iteratable, format like 3 1d20. """
        if iterations is None:
            return
        diceResult = []
        for _ in range(iterations):
            # Roll 4 d6 dice, and keep the highest 3, append each result to diceResult.
            result = dndice.verbose(dicerolls)
            diceResult.append(result)
        # Create a format spec for each item in the input `alist`.
        # E.g., each item will be right-adjusted, field width=3.
        format_list = ['{:>3}' for item in diceResult]

        # Now join the format specs into a single string:
        # E.g., '{:>3}, {:>3}, {:>3}' if the input list has 3 items.
        s = '\n'.join(format_list)

        # Now unpack the input list `alist` into the format string. Done!
        finalResult = s.format(*diceResult)
        await ctx.reply(f'Rolling {iterations} iterations...\n{finalResult}')


async def setup(bot):
    await bot.add_cog(dice(bot))