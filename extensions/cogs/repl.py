import discord
import jishaku
from discord import app_commands
from discord.ext import commands

from etc.cogs import StellaCog
from etc.static import STELLA_GUILD
from etc.types import StellaBot, StellaContext

REPL_CHANNEL = 1066547634497658992

class ReplCog(StellaCog, name="Repl"):
    ctx_menu_jsk: app_commands.ContextMenu | None = None

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        if message.channel.id != REPL_CHANNEL:
            return

        ctx = await self.bot.get_context(message)
        ctx.prefix = await self.bot.get_prefix(message)
        await self.jishaku_repl(ctx, message)

    async def runner_callback(self, interaction: discord.Interaction, message: discord.Message):
        ctx = await self.bot.get_context(interaction)
        await self.jishaku_repl(ctx, message)

    def cog_load(self) -> None:
        guild_id = [guild := discord.Object(STELLA_GUILD)]
        self.ctx_menu_jsk = app_commands.ContextMenu(name="run", callback=self.runner_callback, guild_ids=guild_id)
        self.bot.tree.add_command(self.ctx_menu_jsk, guild=guild)

    def cog_unload(self) -> None:
        self.bot.tree.remove_command(self.ctx_menu_jsk, guild=discord.Object(STELLA_GUILD))

    async def jishaku_repl(self, ctx: StellaContext, message: discord.Message):
        cb = jishaku.codeblocks.codeblock_converter(message.content)  # type: ignore
        cmd = self.bot.get_command('jsk py')
        await ctx.invoke(cmd, argument=cb)


async def setup(bot: StellaBot):
    await jishaku.setup(bot)
    await bot.add_cog(ReplCog())

