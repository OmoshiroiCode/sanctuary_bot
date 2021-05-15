import discord
from discord.ext import commands, tasks


class Invite(commands.Cog):
  def __init__(self, bot):
    self.bot = bot



def setup(bot):
  bot.add_cog(Invite(bot))