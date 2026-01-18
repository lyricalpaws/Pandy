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

    time = datetime.time(hour=11, minute=00, tzinfo=ZoneInfo('Europe/London'))

    @tasks.loop(time=time)
    async def medsReminder(self):
        for cutie in self.config.reminders:
            try:
                user = self.bot.get_user(cutie)
                embed = discord.Embed(title="Remember to take your medication!!!!",
                      description="If you haven't taken it yet then now is the best time to do it ❤️",
                      colour=0xe11399,
                      timestamp=datetime.datetime.now())
                embed.set_image(url="https://cloud.neb.gay/s/Tb7eFSXi5SLeLnC/preview")
                embed.set_footer(text="Love you dork")
                await user.send(embed=embed)
            except Exception as e:
                print(e)
                
    @tasks.loop(time=time)
    async def estrogenReminder(self):
        dt = datetime.datetime.now()
        dt = dt.weekday()
        if dt == 2:
            for owners in self.config.reminders:
                try:
                    user = self.bot.get_user(owners)
                    embed = discord.Embed(title="It's estrogen injection day!",
                        description="If you haven't taken it yet then now is the best time to do it ❤️",
                        colour=0xe11399,
                        timestamp=datetime.datetime.now())
                    embed.set_image(url="https://cloud.neb.gay/s/Tb7eFSXi5SLeLnC/preview")    
                    await user.send(embed=embed)
                except Exception as e:
                    print(e)
        else:
            return

    @commands.command(hidden=True)
    @commands.check(repo.is_owner)
    async def remindtest(self, ctx):
        dt = datetime.datetime.now()
        weekday = dt.isoweekday()
        print(weekday)
        for owners in self.config.reminders:
            try:
                user = self.bot.get_user(owners)
                embed = discord.Embed(title="It's estrogen injection day!",
                    description="If you haven't taken it yet then now is the best time to do it ❤️",
                    colour=0xe11399,
                    timestamp=datetime.datetime.now())
                embed.set_image(url="https://cloud.neb.gay/s/Tb7eFSXi5SLeLnC/preview")
                await user.send(embed=embed)
            except Exception as e:
                print(e)

async def setup(bot):
    await bot.add_cog(reminder(bot))
