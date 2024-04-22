import gc
from discord.ext import commands
from utils import default, repo


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


async def setup(bot):
    await bot.add_cog(admin(bot))