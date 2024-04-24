import datetime
import discord
from discord.ext import commands, tasks
from utils import default, repo
from zoneinfo import ZoneInfo


class reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.medsReminder.start()

    def cog_unload(self):
        self.medsReminder.cancel()

    time = datetime.time(hour=11, minute=17, tzinfo=ZoneInfo('Europe/London'))

    @tasks.loop(time=time)
    async def medsReminder(self):
        for cutie in self.config.reminders:
            try:
                user = self.bot.get_user(cutie)
                embed = discord.Embed(title="Remember to take your medication!!!!",
                      description="If you haven't taken it yet then now is the best time to do it ❤️",
                      colour=0xe11399,
                      timestamp=datetime.datetime.now())
                embed.set_footer(text="Love you dork")
                await user.send(embed=embed)
            except Exception as e:
                print(e)

    @commands.command(hidden=True)
    @commands.check(repo.is_owner)
    async def remindtest(self, ctx):
        for cutie in self.config.reminders:
            try:
                user = self.bot.get_user(cutie)
                embed = discord.Embed(title="Remember to take your medication!!!!",
                      description="If you haven't taken it yet then now is the best time to do it ❤️",
                      colour=0xe11399,
                      timestamp=datetime.datetime.now())
                embed.set_footer(text="Love you dork")
                await user.send(embed=embed)
            except Exception as e:
                print(e)

async def setup(bot):
    await bot.add_cog(reminder(bot))