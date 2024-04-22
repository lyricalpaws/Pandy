import gc
import time
import os
import discord
from discord.ext import commands
from utils import default, repo
from subprocess import Popen, PIPE


class admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = default.get("config.json")

    @commands.command(hidden=True)
    @commands.check(repo.is_owner)
    async def cogs(self, ctx):
        """ Gives all loaded extensions. """
        mod = ", ".join(list(self.bot.cogs))
        await ctx.send(f"The current modules are:\n```\n{mod}\n```")

    @commands.command(aliases=["re"], hidden=True)
    @commands.check(repo.is_owner)
    async def reload(self, ctx, name: str):
        """ Reloads an extension. """
        await ctx.message.add_reaction("🔃")
        try:
            await self.bot.unload_extension(f"cogs.{name}")
            await self.bot.load_extension(f"cogs.{name}")
        except ModuleNotFoundError:
            await ctx.message.remove_reaction(
                "🔃", member=ctx.me
            )
            return await ctx.message.add_reaction("❌")
        except SyntaxError:
            await ctx.message.remove_reaction(
                "🔃", member=ctx.me
            )
            return await ctx.message.add_reaction("❌")
        await ctx.message.remove_reaction("🔃", member=ctx.me)
        await ctx.message.add_reaction("✅")

    @commands.command(hidden=True)
    @commands.check(repo.is_owner)
    async def load(self, ctx, name: str):
        """ Loads an extension. """
        await ctx.message.add_reaction("🔃")
        try:
            await self.bot.load_extension(f"cogs.{name}")
        except ModuleNotFoundError:
            await ctx.message.remove_reaction(
                "🔃", member=ctx.me
            )
            return await ctx.message.add_reaction("❌")
        except SyntaxError:
            await ctx.message.remove_reaction(
                "🔃", member=ctx.me
            )
            return await ctx.message.add_reaction("❌")
        await ctx.message.remove_reaction("🔃", member=ctx.me)
        await ctx.message.add_reaction("✅")

    @commands.command(hidden=True)
    @commands.check(repo.is_owner)
    async def unload(self, ctx, name: str):
        """ Unloads an extension. """
        await ctx.message.add_reaction("🔃")
        try:
            await self.bot.unload_extension(f"cogs.{name}")
        except ModuleNotFoundError:
            await ctx.message.remove_reaction(
                "🔃", member=ctx.me
            )
            return await ctx.message.add_reaction("❌")
        except SyntaxError:
            await ctx.message.remove_reaction(
                "🔃", member=ctx.me
            )
            return await ctx.message.add_reaction("❌")
        await ctx.message.remove_reaction("🔃", member=ctx.me)
        await ctx.message.add_reaction("✅")

    @commands.command(hidden=True)
    @commands.check(repo.is_owner)
    async def gc(self, ctx):
        """ Cleans up trash """
        await ctx.message.add_reaction("🔃")
        gc.collect()
        del gc.garbage[:]
        await ctx.message.remove_reaction("🔃", member=ctx.me)
        await ctx.message.add_reaction("✅")

    @commands.command(hidden=True)
    @commands.check(repo.is_owner)
    async def reboot(self, ctx):
        """ Reboot the bot """
        await ctx.send("Rebooting now...")
        time.sleep(1)
        await self.bot.close()

    @commands.command(hidden=True, aliases=["pull"])
    @commands.check(repo.is_owner)
    async def update(self, ctx, silently: bool = False):
        """ Gets latest commits and applies them from git """
        await ctx.message.add_reaction("🔃")

        def run_shell(command):
            with Popen(command, stdout=PIPE, stderr=PIPE, shell=True) as proc:
                return [std.decode("utf-8") for std in proc.communicate()]

        pull = await self.bot.loop.run_in_executor(
            None, run_shell, "git pull"
        )
        msg = await ctx.send(f"```css\n{pull}\n```")
        await ctx.message.remove_reaction("🔃", member=ctx.me)
        for file in os.listdir("cogs"):
            if file.endswith(".py"):
                name = file[:-3]
                await self.bot.unload_extension(f"cogs.{name}")
                await self.bot.load_extension(f"cogs.{name}")
        await ctx.message.add_reaction("✅")

    @commands.command(hidden=True)
    @commands.check(repo.is_owner)
    async def sync(self, ctx):
        await self.bot.tree.sync()
        await ctx.send("Synced")

    @commands.hybrid_command()
    async def badge(self, ctx: commands.Context):
        embed = discord.Embed(title="Program Ran Successfully",
                            description="**+** You have ran the bot correctly and have claimed your Discord Developer Badge. \n\n**+** It may take up to 24 hours or a tiny bit more for your badge to shop up here (https://discord.com/developers/active-developer)",
                            colour=0x00f53d)
        await ctx.send(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(admin(bot))