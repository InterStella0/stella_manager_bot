from typing import Literal

import discord
from discord.ext import commands

from etc.cogs import StellaCog
from etc.static import STELLA_GUILD
from etc.types import StellaContext, StellaBot


class Myself(StellaCog):
    async def cog_check(self, ctx: StellaContext) -> bool:
        if await self.bot.is_owner(ctx.author):
            return True

        raise commands.NotOwner("This is only for command owner.")

    @commands.command()
    async def sync(self, ctx: StellaContext, guild: Literal['guild'] | None):
        tree = self.bot.tree
        guild_id = None
        if guild:
            guild_id = discord.Object(STELLA_GUILD)
            tree.copy_global_to(guild=guild_id)

        cmds = await tree.sync(guild=guild_id)
        await ctx.send(f"Synced {len(cmds)}")


async def setup(bot: StellaBot):
    await bot.add_cog(Myself())
