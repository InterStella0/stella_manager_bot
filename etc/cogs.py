from __future__ import annotations
from typing import TYPE_CHECKING

from discord.abc import Snowflake
from discord.ext import commands

if TYPE_CHECKING:
    from etc.bot import StellaBotHandler
    from typing_extensions import Self


class StellaCog(commands.Cog):
    bot: StellaBotHandler | None

    async def _inject(self, bot: StellaBotHandler, override: bool, guild: Snowflake | None, guilds: list[Snowflake]) -> Self:
        self.bot = bot
        return await super()._inject(bot, override, guild, guilds)


