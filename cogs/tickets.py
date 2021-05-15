import discord
from discord.ext import commands
import json
import asyncio

class Tickets(commands.Cog):
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  @commands.has_permissions(administrator=True)
  async def createticket(self, ctx, *args):
    format_args = list(args)
    if len(format_args) <= 1:
      return await ctx.send("**Please input a channel/message for the ticket!**")
    if format_args[0].startswith('<#') and format_args[0].endswith('>'):
      format_args[0] = format_args[0].strip('<').strip('>').replace('#', '')
      channel_id = self.bot.get_channel(int(format_args[0].strip('<').strip('>').replace('#', '')))
    if format_args[0] == int:
      channel_id = self.bot.get_channel(int(format_args[0]))
    if format_args[0] == str:
      channel_id = discord.utils.get(ctx.guild.text_channels, name=f'{format_args[0]}')

    guild_id = ctx.message.guild.id
    title = ' '.join(format_args[1:])

    # Create new Embed with reaction
    ticket_emb = discord.Embed(color=0xDB2727)
    ticket_emb.set_thumbnail(url="https://media.giphy.com/media/hpH0sZCDrK7YStM99I/giphy.gif")

    ticket_emb.add_field(name=f"Welcome to {ctx.message.guild}", value=f"{title}")
    send_ticket_emb = await channel_id.send(embed=ticket_emb)

    with open("./jsons/ticket.json", "r") as file:
      ticket_data = json.load(file)
      new_ticket = str(guild_id) + '_msg'
      print(new_ticket)

      # Update existing ticket
      if new_ticket in ticket_data:
        ticket_data[new_ticket] += [send_ticket_emb.id]
        with open("./jsons/ticket.json", "w") as upd_ticket_data:
          json.dump(ticket_data, upd_ticket_data, indent=4)
      else:
        ticket_data[new_ticket] = [send_ticket_emb.id]
        with open("./jsons/ticket.json", "w") as upd_ticket_data:
          json.dump(ticket_data, upd_ticket_data, indent=4)

    await send_ticket_emb.add_reaction(u'\U0001F3AB')

  @commands.command()
  @commands.has_permissions(administrator=True)
  async def closeticket(self, ctx, mentioned_user):
    if mentioned_user.startswith('<@') and mentioned_user.endswith('>'):
      userlist = []
      mentioned_user = mentioned_user[3:-1]
      mentioned_role = self.bot.get_user(int(mentioned_user))
      userlist.append(f"{mentioned_role}")
      useriup = userlist[0][:-5]
      userilo = userlist[0][:-5].lower()
    elif mentioned_user == int:
      try:
        userlist = []
        mentioned_role = self.bot.get_user(int(mentioned_user))
        userlist.append(f"{mentioned_role}")
        useriup = userlist[0][:-5]
        userilo = userlist[0][:-5].lower()
      except:
        return await ctx.send("**Please return a valid ID/username**")
    else:
      useriup = mentioned_user
      userilo = mentioned_user.lower()

    nrole = discord.utils.get(ctx.guild.roles, name=f'{useriup}')
    nchan = discord.utils.get(ctx.guild.text_channels, name=f'{userilo}')

    if nrole is None:
      return await ctx.send("**Member isn't present in tickets!**")
    if nchan is None:
      return await ctx.send("**Channel doesn't exist in tickets!**")

    userlist = []
    await nrole.delete(reason="Removed ticket role")
    await nchan.delete(reason=None)


  @commands.Cog.listener()
  async def on_raw_reaction_add(self, payload):
    with open("./jsons/ticket.json", "r") as file:
      ticket_data = json.load(file)
      ticket_msg = str(payload.member.guild.id) + '_msg'
      try:
        if payload.message_id in ticket_data[ticket_msg]:
          if payload.member.id != self.bot.user.id:
            # Get guild and roles
            find_guild = discord.utils.find(lambda guild: guild.id == payload.guild_id, self.bot.guilds)
            guild_roles = discord.utils.get(find_guild.roles, name=f"{payload.member.name}")

            if guild_roles is None:
              print("New role")
              # Create new role
              permissions = discord.Permissions(send_messages=True, read_messages=True, attach_files=True)
              await find_guild.create_role(name=f"{payload.member.name}", permissions=permissions)

              # Assign new role
              new_user_role = discord.utils.get(find_guild.roles, name=f"{payload.member.name}")
              await payload.member.add_roles(new_user_role, reason=None, atomic=True)

              # Overwrite role permissions
              admin_role = discord.utils.get(find_guild.roles, name="Staff")
              if admin_role is None:
                chan = self.bot.get_channel(payload.channel_id)
                return await chan.send('**Role name "Staff" doesn\'t exist and apply\n it to your staff members so you can continue!**')
              
              overwrite = {
                find_guild.default_role: discord.PermissionOverwrite(read_messages=False),
                new_user_role: discord.PermissionOverwrite(read_messages=True),
                admin_role: discord.PermissionOverwrite(read_messages=True)
              }

              # Create new channel (maybe category)
              ncat = discord.utils.get(payload.member.guild.categories, name='🎫 Tickets')
              print(ncat)
              if ncat == None:
                ncat = await payload.member.guild.create_category(name='🎫 Tickets', overwrites=overwrite, reason=None)
              new_chan = await ncat.create_text_channel(f'{new_user_role}', overwrites=overwrite)
              await new_chan.send(f"**{new_user_role.mention}   your ticket has been created!**\n{admin_role.mention}   `Waiting for response..`")
      except KeyError:
        pass


def setup(bot):
  bot.add_cog(Tickets(bot))