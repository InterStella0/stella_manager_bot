import logging
import sys
import traceback

from discord.ext import commands

from etc.cogs import StellaCog
from etc.types import StellaContext, StellaBot


class ErrorHandler(StellaCog):
    """Minimal Error handler i am lazy"""
    @commands.Cog.listener()
    async def on_command_error(self, ctx: StellaContext, error: commands.CommandError):
        if isinstance(error, commands.CommandNotFound):
            return

        error = getattr(error, 'original', error)
        if isinstance(error, (commands.BadArgument, commands.UserInputError)):
            pass
        else:  # future handling, no time
            err_trace = traceback.format_exception(error)
            printable = ''.join(err_trace)
            self.bot.dpy_logger.error(f"Invoking {ctx.command.qualified_name} resulted in {printable}")

        await ctx.send(str(error))


async def setup(bot: StellaBot):
    await bot.add_cog(ErrorHandler())
