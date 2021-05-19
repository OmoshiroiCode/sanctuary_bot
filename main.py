import discord
from discord.ext import commands, tasks
from itertools import cycle
import datetime
import googletrans
import os
import json
from dotenv import load_dotenv
from other.languages import LANGUAGES

# Loads .env file
load_dotenv()

# Permission for the bot to manage members.
intents = discord.Intents.all()

# The bot we are referring to
bot = commands.Bot(command_prefix="s.", intents=intents, case_insensitive=True)

# Cycles through the statuses
status = cycle(["Status 1", "Status 2"])

# Links blacklist
blacklist = ["discord.gg", ".gg/", ". gg", ". gg/", ". gg /", "d.gg", "dsc.gg" "https", "http", "www.", "www .", ". com", ".com", ". nl", ".nl", ". org", ".org"]

def get_greeting(bot, message):
  with open("jsons/greeting.json", "r") as f:
    greetingfile = json.load(f)

  return greetingfile[str(message.guild.id)]

def get_leaving(bot, message):
  with open("jsons/leaving.json", "r") as f:
    leavingfile = json.load(f)

  return leavingfile[str(message.guild.id)]

# Checks if the bot is online
@bot.event
async def on_ready():
  change_status.start()
  await bot.change_presence(status=discord.Status.dnd)
  print("Logged in as {0.user}!".format(bot))
  print(discord.__version__)

@bot.event
async def on_message(message):
  if message.author == bot.user:
    return
  if isinstance(message.channel, discord.channel.DMChannel):
      return
  if message.content.startswith('s.play'):
    pass
  else:
    for link in blacklist:
      contents = message.content.split()
      if message.content.startswith(link) or message.content.endswith(link):
        return await message.delete()
      for content in contents:
        if content.startswith(link) or content.endswith(link):
          return await message.delete()
    if message.content.startswith("s.") == False:
      translator = googletrans.Translator()
      langtext = translator.detect(f'{message.content}').lang
      if langtext == "en" or langtext == "nl":
        return
      await message.delete()
      translation = translator.translate(f'{message.content}').text
      langname = LANGUAGES[langtext]
      langname = langname[0].upper() + langname[1:]
      langtext = langtext.upper()
      transEmbed = discord.Embed(title="Translation", description=f"Language: {langname} ({langtext})", timestamp=datetime.datetime.utcnow(), color=0xDB2727)
      transEmbed.add_field(name=f"{message.author.name}#{message.author.discriminator} Says", value=f"```{translation}```")
      transEmbed.set_thumbnail(url=f"{message.author.avatar_url}")
      await message.channel.send(embed=transEmbed)
  await bot.process_commands(message)


@bot.event
async def on_user_update(before, after):
  if str(before) != str(after):
    with open("jsons/usernames.json", "r") as usr:
      usrfile = json.load(usr)

    try:
      if usrfile[str(after.id) + '_' + '1']:
        lengid = 1
    except KeyError:
      lengid = 0
    try:
      if usrfile[str(after.id) + '_' + '2']:
        lengid = 2
    except KeyError:
      pass
    try:
      if usrfile[str(after.id) + '_' + '3']:
        lengid = 3
    except KeyError:
      pass
    try:
      if usrfile[str(after.id) + '_' + '4']:
        lengid = 4
    except KeyError:
      pass
    try:
      if usrfile[str(after.id) + '_' + '5']:
        lengid = 5
    except KeyError:
      pass

    if lengid == 0:
      usrfile[str(after.id) + '_' + '1'] = f"{str(before)}"
      with open("jsons/usernames.json", "w") as usr:
        json.dump(usrfile, usr, indent=4)
    elif lengid == 5:
      with open("jsons/usernames.json", "r") as usr:
        usrfile = json.load(usr)
      lis = []
      for i in range(1,6):
        lis.append(usrfile[str(after.id) + '_' + str(i)])
      lis.pop(-1)
      lis.insert(0, str(before))
      
      for i in range(1,6):
        with open("jsons/usernames.json", "r") as usr:
          usrfile = json.load(usr)
        usrfile[str(after.id) + '_' + str(i)] = f"{lis[i - 1]}"
        with open("jsons/usernames.json", "w") as usr:
          json.dump(usrfile, usr, indent=4)
    else:
      lengid = lengid + 1

      with open("jsons/usernames.json", "r") as usr:
        usrfile = json.load(usr)

      usrfile[str(after.id) + '_' + str(lengid)] = str(before)
      with open("jsons/usernames.json", "w") as usr:
        json.dump(usrfile, usr, indent=4)
  else:
    print("Updated profile picture or discriminator")

# Changes the activity every 10 seconds in a loop
@tasks.loop(seconds=10)
async def change_status():
  await bot.change_presence(activity=discord.Game(next(status)))

@bot.command()
async def showrole(ctx):
  await ctx.send(f"{ctx.guild.roles.name}")

@bot.event
async def on_guild_join(guild):
  with open("jsons/greeting.json", "r") as f:
    greetingfile = json.load(f)

  greetingfile[str(guild.id)] = "has joined the server"

  with open("jsons/greeting.json", "w") as f:
    json.dump(greetingfile, f, indent=4)

  with open("jsons/leaving.json", "r") as f:
    leavingfile = json.load(f)

  leavingfile[str(guild.id)] = "has left the server"

  with open("jsons/leaving.json", "w") as f:
    json.dump(leavingfile, f, indent=4)

  with open("jsons/wlmsg.json", "r") as g:
    wlmsgfile = json.load(g)

  wl = wlmsgfile[str(guild.id)]

  chan = discord.utils.get(guild.text_channels, name=wl)

  mcount = guild.member_count

  cat = discord.utils.get(guild.categories, name='📊 Stats')
  catinv = discord.utils.get(guild.voice_channels, name='discord.gg/fXx7qC33bX')
  unverified = discord.utils.get(guild.roles, name='unverified')

  try:
    if unverified != None:
      pass
    else:
      nrole = await guild.create_role(name='unverified', permissions=None)
      nrole.edit(position=-1, permissions=discord.Permissions(create_instant_invite=True))
      try:
        role2 = discord.utils.get(guild.roles, name="unverified")
        await cat.set_permissions(role2, view_channel=True)
      except:
        pass

    if cat != None:
      pass
    else:
      ncat = await guild.create_category(name='📊 Stats', overwrites=None, reason=None, position=0)
      role1 = discord.utils.get(guild.roles, name="@everyone")
      role2 = discord.utils.get(guild.roles, name="unverified")
      await ncat.set_permissions(role1, connect=False)
      await ncat.set_permissions(role2, view_channel=True)

    cat = discord.utils.get(guild.categories, name='📊 Stats')

    if str(guild.voice_channels).find("Member Count -") > 0:
      pass
    else:
      evc = await cat.create_voice_channel(name=f"Member Count - {mcount}")
      await evc.edit(position=0)

    if catinv != None:
      pass
    else:
      ivc = await cat.create_voice_channel(name="discord.gg/fXx7qC33bX")
      await ivc.edit(position=1)

    for chan in guild.voice_channels:
      if "Member Count -" in chan.name:
        mcount = guild.member_count
        chann = discord.utils.get(guild.voice_channels, name=chan.name)
        await chann.edit(name=f"Member Count - {mcount}")
  except Exception as e:
    print(e)

  await chan.send("""
  ```diff
- Hey thanks for inviting Sanctuary bot! -

Please make sure to check our server out Sanctuary

Prefix: s.

Do s.help for more info!

Setup:
- The welcome-leave channel
- Preferrably a custom welcome message
- Preferrably a custom leave message

Hope you have a good time!

```
https://discord.gg/hEVF5b9F4c
https://cdn.discordapp.com/attachments/534843457056014367/536666736460562443/advertise_light_bar.gif
""")

@bot.event
async def on_guild_remove(guild):
  with open("jsons/greeting.json", "r") as f:
    greetingfile = json.load(f)

  greetingfile.pop(str(guild.id))

  with open("jsons/greeting.json", "w") as f:
    json.dump(greetingfile, f, indent=4)

  with open("jsons/leaving.json", "r") as f:
    leavingfile = json.load(f)

  leavingfile.pop(str(guild.id))

  with open("jsons/leaving.json", "w") as f:
    json.dump(leavingfile, f, indent=4)

  cat = discord.utils.get(guild.categories, name='📊 Stats')
  await cat.delete()


@bot.command()
@commands.has_permissions(administrator=True)
async def changewelcome(ctx, *, greeting):
  guild = ctx.message.guild.id
  with open("jsons/greeting.json", "r") as f:
    greetingfile = json.load(f)

  greetingfile[str(guild)] = greeting

  with open("jsons/greeting.json", "w") as f:
    json.dump(greetingfile, f, indent=4)

  await ctx.send(f"Welcome message changed to!: **{greeting}**")

@changewelcome.error
async def changewelcome_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please specify some text for the bot to apply changes, for ex: s.changewelcome Joined the server!")

@bot.command()
@commands.has_permissions(administrator=True)
async def changeleave(ctx, *, leaving):
  guild = ctx.message.guild.id
  with open("jsons/leaving.json", "r") as g:
    leavingfile = json.load(g)

  leavingfile[str(guild)] = leaving

  with open("jsons/leaving.json", "w") as g:
    json.dump(leavingfile, g, indent=4)

  await ctx.send(f"Leave message changed to!: **{leaving}**")

@changeleave.error
async def changeleave_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please specify some text for the bot to apply changes, for ex: s.changeleave Joined the server!")

@bot.command()
async def jlchannel(ctx, arg1 : str):
  gid = ctx.guild.id
  global setchan
  print(arg1)
  def IntCheck(arg1):
    try: 
      int(arg1)
      return True
    except:
      return False

  try:
    if arg1 == None:
      setchan = ctx.author.channel
    elif arg1[0:2] == "<#":
      arg1 = arg1[2:]
      arg1 = arg1[:-1]
      setchan = await bot.fetch_channel(arg1)
      print(setchan.type)
      print(setchan)
      if "text" in setchan.type:
        pass
      else:
        return await ctx.send("**Specify a text channel!**")
    elif IntCheck(arg1) == True:
      setchan = await bot.fetch_channel(arg1)
      print(setchan)
      if "text" in setchan.type:
        pass
      else:
        return await ctx.send("**Specify a text channel!**")
    else:
      setchan = discord.utils.get(ctx.guild.text_channels, name=arg1)
    if setchan == None:
      return await ctx.send("**Specify a valid channel format!**")

    await ctx.send(f"Join/Leave channel set to: {setchan}")

    with open("jsons/wlmsg.json", "r") as f:
      wlmsgfile = json.load(f)

    try:
      wlmsgfile.pop(str(gid))
      print("Popped")
    except:
      print("Didn't pop")

    wlmsgfile[str(gid)] = str(setchan)

    with open("jsons/wlmsg.json", "w") as f:
      json.dump(wlmsgfile, f, indent=4)
  except Exception as e:
    await ctx.send("Didn't found the channel!")
    print(e)

@jlchannel.error
async def jlchannel_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please specify some text for the bot apply changes, for ex: s.jlchannel general")
  

@bot.command()
async def showchan(ctx):
  with open("jsons/wlmsg.json", "r") as g:
    wlmsgfile = json.load(g)

  wl = wlmsgfile[str(ctx.message.guild.id)]
  await ctx.send(f"{wl}")

# Will send a message if someone joined
@bot.event
async def on_member_join(member):
  unvrole = discord.utils.get(member.guild.roles, name='unverified')
  await member.add_roles(unvrole)
  guildid = member.guild.id

  with open("jsons/wlmsg.json", "r") as g:
    wlmsgfile = json.load(g)

  wl = wlmsgfile[str(guildid)]

  with open("jsons/greeting.json", "r") as f:
    greetingfile = json.load(f)

  gre = greetingfile[str(guildid)]

  channel = discord.utils.get(member.guild.text_channels, name=wl)
  await channel.send(f"**{member}** {gre}")

  mcount = member.guild.member_count

  cat = discord.utils.get(member.guild.categories, name='📊 Stats')
  catinv = discord.utils.get(member.guild.voice_channels, name='discord.gg/fXx7qC33bX')
  unverified = discord.utils.get(member.guild.roles, name='unverified')


  try:
    if unverified != None:
      print("Passed")
    else:
      print("Else")
      nrole=await member.guild.create_role(name='unverified', permissions=discord.Permissions.none())
      print(nrole)
      nrole.edit(position=-1, permissions=discord.Permissions(create_instant_invite=True))
      try:
        role2 = discord.utils.get(member.guild.roles, name="unverified")
        await cat.set_permissions(role2, view_channel=True)
      except:
        pass

    if cat != None:
      pass
    else:
      ncat = await member.guild.create_category(name='📊 Stats', overwrites=None, reason=None, position=0)
      role1 = discord.utils.get(member.guild.roles, name="@everyone")
      role2 = discord.utils.get(member.guild.roles, name="unverified")
      await ncat.set_permissions(role1, connect=False)
      await ncat.set_permissions(role2, view_channel=True)

    member.add_roles(unverified)
    cat = discord.utils.get(member.guild.categories, name='📊 Stats')

    if str(member.guild.voice_channels).find("Member Count -") > 0:
      pass
    else:
      evc = await cat.create_voice_channel(name=f"Member Count - {mcount}")
      await evc.edit(position=0)

    if catinv != None:
      pass
    else:
      ivc = await cat.create_voice_channel(name="discord.gg/fXx7qC33bX")
      await ivc.edit(position=1)

    for chan in member.guild.voice_channels:
      if "Member Count -" in chan.name:
        mcount = member.guild.member_count
        chann = discord.utils.get(member.guild.voice_channels, name=chan.name)
        await chann.edit(name=f"Member Count - {mcount}")

  except Exception as e:
    print(e)

# Will send a message if someone leaved
@bot.event
async def on_member_remove(member):
  guildid = member.guild.id

  with open("jsons/wlmsg.json", "r") as g:
    wlmsgfile = json.load(g)

  wl = wlmsgfile[str(guildid)]

  with open("jsons/leaving.json", "r") as f:
    leavingfile = json.load(f)

  lea = leavingfile[str(guildid)]

  channel = discord.utils.get(member.guild.text_channels, name=wl)
  await channel.send(f"**{member}** {lea}")

  mcount = member.guild.member_count

  cat = discord.utils.get(member.guild.categories, name='📊 Stats')
  catinv = discord.utils.get(member.guild.voice_channels, name='discord.gg/fXx7qC33bX')
  unverified = discord.utils.get(member.guild.roles, name='unverified')
  print(unverified)

  try:
    if unverified != None:
      print("Passed")
    else:
      print("Else")
      nrole=await member.guild.create_role(name='unverified', permissions=discord.Permissions.none())
      print(nrole)
      nrole.edit(position=-1, permissions=discord.Permissions(create_instant_invite=True))
      try:
        role2 = discord.utils.get(member.guild.roles, name="unverified")
        await cat.set_permissions(role2, view_channel=True)
      except:
        pass

    if cat != None:
      pass
    else:
      ncat = await member.guild.create_category(name='📊 Stats', overwrites=None, reason=None, position=0)
      role1 = discord.utils.get(member.guild.roles, name="@everyone")
      role2 = discord.utils.get(member.guild.roles, name="unverified")
      await ncat.set_permissions(role1, connect=False)
      await ncat.set_permissions(role2, view_channel=True)

    cat = discord.utils.get(member.guild.categories, name='📊 Stats')

    if str(member.guild.voice_channels).find("Member Count -") > 0:
      pass
    else:
      evc = await cat.create_voice_channel(name=f"Member Count - {mcount}")
      await evc.edit(position=0)

    if catinv != None:
      pass
    else:
      ivc = await cat.create_voice_channel(name="discord.gg/fXx7qC33bX")
      await ivc.edit(position=1)

    for chan in member.guild.voice_channels:
      if "Member Count -" in chan.name:
        mcount = member.guild.member_count
        chann = discord.utils.get(member.guild.voice_channels, name=chan.name)
        await chann.edit(name=f"Member Count - {mcount}")
  except Exception as e:
    print(e)

@bot.event
async def on_command_error(ctx, error):
  if isinstance(error, commands.CommandNotFound):
    await ctx.send("Command not found! Do s.help for more info")

  elif isinstance(error, commands.NotOwner):
    await ctx.send("You are not the owner so you can't execute this command! Do s.help for more info")

  elif isinstance(error, commands.NoPrivateMessage):
    await ctx.send("You can't use that command in a private message!")

  elif isinstance(error, commands.CommandOnCooldown):
    await ctx.send(error)

  elif isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("`You are missing required arguments! Do s.help for more info`")

  else:
    raise error

# Loads a specified extension
@bot.command()
async def load(ctx, extension):
  try:
    bot.load_extension(f"cogs.{extension}")
  except:
    bot.load_extension(f"{extension}")
    
@load.error
async def load_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please input a filename to run, for ex: s.load example1")

# Unloads a specified extension
@bot.command()
async def unload(ctx, extension):
  try:
    bot.unload_extension(f"cogs.{extension}")
  except:
    bot.unload_extension(f"{extension}")

@unload.error
async def unload_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please input a filename to run, for ex: s.unload commands")

# Reloads a specified extension
@bot.command()
async def reload(ctx, extension):
  try:
    bot.reload_extension(f"cogs.{extension}")
    await ctx.send(f"Cog .{extension} has been reloaded")
  except:
    bot.reload_extension(f"{extension}")
    await ctx.send(f"Cog {extension} has been reloaded")

@reload.error
async def reload_error(ctx, error):
  if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send("Please input a filename to run, for ex: s.reload example1")

# Loops through the cogs folder and runs the cogs
for filename in os.listdir("./cogs"):
  if filename.endswith(".py"):
    bot.load_extension(f"cogs.{filename[:-3]}")


# Run the bot with the given token
bot.run(os.getenv('TOKEN'))