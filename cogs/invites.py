import discord
from discord.ext import commands, tasks
# import DiscordUtils


class Invite(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    # self.tracker = DiscordUtils.InviteTracker(bot)

  # @commands.Cog.listener()
  # async def on_ready(self):
  #     await self.tracker.cache_invites()

  # @commands.Cog.listener()
  # async def on_invite_create(self, invite):
  #     await self.tracker.update_invite_cache(invite)

  # @commands.Cog.listener()
  # async def on_guild_join(self, guild):
  #     await self.tracker.update_guild_cache(guild)

  # @commands.Cog.listener()
  # async def on_invite_delete(self, invite):
  #     await self.tracker.remove_invite_cache(invite)

  # @commands.Cog.listener()
  # async def on_guild_remove(self, guild):
  #     await self.tracker.remove_guild_cache(guild)

  # @commands.Cog.listener()
  # async def on_member_join(self, member):
  #     inviter = await self.tracker.fetch_inviter(member) # Is the inviter from the member who joined the invite
  #     data = await self.bot.invites.find(inviter.id)
  #     if data is None:
  #       with open('./other/invites.json', 'r') as file:
  #         file_data = json.load(file)
  #         file_data[str(invited.id)]



def setup(bot):
  bot.add_cog(Invite(bot))