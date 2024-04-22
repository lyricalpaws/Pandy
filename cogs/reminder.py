import datetime
from discord.ext import commands, tasks
from utils import default
from zoneinfo import ZoneInfo


class reminder(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")
        self.my_task.start()

    def cog_unload(self):
        self.my_task.cancel()

    time = datetime.time(hour=11, minute=00, tzinfo=ZoneInfo('Europe/London'))

    @tasks.loop(time=time)
    async def my_task(self):
        print("My task is running!")


async def setup(bot):
    await bot.add_cog(reminder(bot))