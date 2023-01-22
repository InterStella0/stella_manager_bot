import asyncio
import glob
import sys
import traceback
from typing import Generator

import discord
import starlight
from discord.ext import commands

from config import Configuration
from etc import utils


class StellaBotHandler(commands.Bot):
    def __init__(self) -> None:
        intents = discord.Intents.all()
        super().__init__("uwu ", intents=intents, help_command=starlight.MenuHelpCommand(with_app_command=True))
        self.config = Configuration

    @staticmethod
    def find_all_extensions(*, ignore=('_', '.')) -> Generator[str, None, None]:
        for file in glob.glob('extensions/**/*.py', recursive=True):
            if file.startswith(ignore):
                continue

            yield file

    async def extension_loader(self):
        async def load(ext):
            try:
                await self.load_extension(utils.fp_extension(ext))
            except Exception:
                print("Failure to load", ext, file=sys.stderr)
                traceback.print_exc()
            else:
                print("Loaded", ext)

        exts = [asyncio.create_task(load(ext))
                for ext in self.find_all_extensions()]
        await asyncio.gather(*exts)

    async def setup_hook(self) -> None:
        await self.extension_loader()

    async def _establishing(self):
        async with self:
            await self.start(self.config.token)

    def establish(self):
        asyncio.run(self._establishing())