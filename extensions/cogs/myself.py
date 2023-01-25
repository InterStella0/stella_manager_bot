from typing import Literal, Annotated

import discord
import starlight
from discord.ext import commands

from etc.cogs import StellaCog
from etc.static import STELLA_GUILD
from etc.types import StellaContext, StellaBot


class ListenCommand:
    class CommandConverter(commands.Converter[commands.Command]):
        async def convert(self, ctx: StellaContext, argument: str) -> commands.Command:
            command = ctx.bot.get_command(argument)
            if command is None:
                raise commands.BadArgument(f"No command found for `{argument}`")

            return command

    class ValidChannel(commands.TextChannelConverter):
        def __init__(self, *, exist):
            super().__init__()
            self.exist = exist

        async def convert(self, ctx: StellaContext, argument: str) -> discord.TextChannel:
            channel = await super().convert(ctx, argument)
            is_listen = await ctx.bot.db.fetchrow("SELECT * FROM listener WHERE channel_id=$1", channel.id)
            if self.exist and is_listen:
                raise commands.BadArgument(f"{channel} is already listening for {is_listen['command_qualified_name']}")
            elif not self.exist and not is_listen:
                raise commands.BadArgument(f"{channel} is not listening to any command.")

            return channel


class Myself(StellaCog):
    async def cog_check(self, ctx: StellaContext) -> bool:
        if await self.bot.is_owner(ctx.author):
            return True

        raise commands.NotOwner("This is only for command owner.")

    @commands.group(invoke_without_command=True)
    @commands.guild_only()
    async def listen(self, ctx: StellaContext):
        pass

    @listen.command()
    async def add(
            self,
            ctx: StellaContext,
            channel: discord.TextChannel = commands.param(converter=ListenCommand.ValidChannel(exist=True)), *,
            command: Annotated[commands.Command, ListenCommand.CommandConverter]
    ):
        query = "INSERT INTO listener VALUES($1, $2) RETURNING *"
        row = await self.bot.db.fetchrow(query, channel.id, command.qualified_name)
        embed = discord.Embed(
            title="Listener",
            description=f"**{channel}** will now listen for `{command.qualified_name}`",
            timestamp=row['created_at']
        )
        await ctx.send(embed=embed)

    @listen.command()
    async def remove(
            self, ctx: StellaContext, *,
            channel: discord.TextChannel = commands.param(converter=ListenCommand.ValidChannel(exist=False))):
        await self.bot.db.execute('DELETE FROM listener WHERE channel_id=$1', channel.id)
        embed = discord.Embed(
            title="Listener",
            description=f"**{channel}** will no longer be listening.",
            timestamp=discord.utils.utcnow()
        )
        await ctx.send(embed=embed)

    @listen.command()
    async def list(self, ctx: StellaContext):
        rows = await self.bot.db.fetch("SELECT * FROM listener")
        if not rows:
            return await ctx.send("No listener exists.")

        view = starlight.SimplePaginationView(discord.utils.as_chunks(rows, 5), cache_page=True)
        async for item in starlight.inline_pagination(view, ctx):
            item.format(embed=discord.Embed(
                title="Listeners [{0.current_page}/{0.max_pages}]".format(view),
                description="\n".join([f"{self.bot.get_channel(r['channel_id'])}:`{r['command_qualified_name']}`"
                                       for r in item.data])
            ))

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
