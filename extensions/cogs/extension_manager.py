import os.path

import discord
from discord.ext import commands

from etc import utils
from etc.cogs import StellaCog
from etc.types import StellaContext, StellaBot


class ExtensionManager(StellaCog, name="Extension Manager"):
    """Manages all extension on this bot."""
    STATIC_FOLDER: str = "extensions/dynamic"

    async def cog_check(self, ctx: StellaContext) -> bool:
        if await self.bot.is_owner(ctx.author):
            return True

        raise commands.NotOwner("This is only for command owner.")

    @commands.group(aliases=['ext'])
    async def extension(self, ctx: StellaContext) -> None:
        pass

    @extension.command()
    async def load(self, ctx: StellaContext, *, name: str):
        await self.bot.load_extension(utils.fp_extension(name))
        await ctx.send(f"Loaded {name}")

    @extension.command()
    async def reload(self, ctx: StellaContext, *, name: str):
        await self.bot.reload_extension(utils.fp_extension(name))
        await ctx.send(f"Reloaded {name}")

    @extension.command()
    async def unload(self, ctx: StellaContext, *, name: str):
        await self.bot.unload_extension(utils.fp_extension(name))
        await ctx.send(f"Unloaded {name}")

    @extension.command()
    async def upload(self, ctx: StellaContext, file: discord.Attachment):
        filepath = await self.store(file)
        fp = utils.fp_extension(filepath)
        name = self.bot._resolve_name(fp, None)
        if name in self.bot.extensions:
            await self.bot.reload_extension(fp)
            response = "Reloaded"
        else:
            await self.bot.load_extension(fp)
            response = "Loaded"

        await ctx.send(f'{response} {fp}')

    async def store(self, attachment: discord.Attachment) -> str:
        fp = os.path.join(self.STATIC_FOLDER, attachment.filename)
        await attachment.save(fp)
        return fp


async def setup(bot: StellaBot):
    await bot.add_cog(ExtensionManager())
