"""Nerdy shit stop talking to me"""
from __future__ import annotations

from discord.ext import commands

from etc.bot import StellaBotHandler

StellaContext = commands.Context[StellaBotHandler]
StellaBot = StellaBotHandler
