import discord
from discord.ext import commands
import os
import datetime
from datetime import date
from io import BytesIO
from io import StringIO
from dateutil.relativedelta import relativedelta
import json
import random
import requests
import string
import asyncio
from captcha.image import ImageCaptcha
import praw


class cmds(commands.Cog):

  def __init__(self, bot):
    self.bot = bot
    self.cancelled = False
    self.reddit = praw.Reddit(client_id = "UYOisyUnPXu69Q",
                              client_secret = "bgZrI9X25d4IuzTa6X9uBa-NGoMd0w",
                              username = "YousCoding",
                              password = os.environ['praw_pass'],
                              user_agent = "pythonpraw",
                              check_for_async=False)

  # Prints a message if the bots connected and online (ready)
  @commands.Cog.listener()
  async def on_ready(self):
    print("Bot is online")

  # Kicks the user
  @commands.command()
  async def kick(self, ctx, *, member : discord.Member, reason=None):
    await member.kick(reason=reason)
    await ctx.send(f"**{member}** has been kicked from the server.")

  # Bans the user
  @commands.command()
  async def ban(self, ctx, *, member : discord.Member, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"**{member}** has been banned from the server.")

  # Unbans the user
  @commands.command()
  async def unban(self, ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    for ban_entry in banned_users:
      user = ban_entry.user
      usern = user.name + "#" + user.discriminator
      if(user.name, user.discriminator) == (member_name, member_discriminator):
        await ctx.guild.unban(user)
        print(f"{usern} has been unbanned.")
        await ctx.send(f"{usern} has been unbanned.")
        return

  # Says pong and then pings your response time
  @commands.command()
  async def ping(self, ctx):
    await ctx.send(f"Pong! {round(self.bot.latency * 1000)}ms")

  # Generates a random image of a cute fox UwU
  @commands.command()
  async def fox(self, ctx):
    link = "https://randomfox.ca/floof/"
    response = requests.get(link)
    foxob = response.json()
    embed = discord.Embed(title='Look at this fox uWu! :fox:', colour=0xEF7D00)
    embed.set_image(url=foxob['image'])
    await ctx.send(embed = embed)

  # Bot says whatever you input
  @commands.command()
  async def say(self, ctx, *, answ=None):
    answ = answ or "Please provide a message for the bot to say"
    await ctx.message.delete()
    await ctx.send(answ)

  # Plays 8ball game
  @commands.command(aliases=["8ball"])
  async def ball(self, ctx, *, question):
    responses = ["It is certain", "It is decidedly so", "Without a doubt", "Yes, definitely",
                "You may rely on it", "As I see it, yes", "Most Likely", "Outlook Good",
                "Yes", "Signs point to yes", "Reply hazy, try again", "Ask again later",
                "Better not tell you now", "Cannot predict now", "Concentrate and ask again",
                "Don't count on it", "My reply is no", "My sources say no", "Outlook not so good", "Very Doubtful"]
    await ctx.send(f"Question: {question}\nAnswer: {random.choice(responses)}")

  @commands.command()
  async def version(self, ctx):
    myEmbed = discord.Embed(title="Current version", description="The bot is in Version 1.2", color=0x00ff00)
    myEmbed.add_field(name="Version code:", value="v1.2.0", inline=False)
    myEmbed.add_field(name="Date Released:", value="March 3th, 2021", inline=False)
    myEmbed.set_footer(text="This is a sample footer")
    myEmbed.set_author(name="Dw Encry")

    await ctx.send(embed=myEmbed)

  # Purges channel messages
  @commands.command()
  @commands.has_permissions(manage_messages=True)
  async def purge(self, ctx, amount : int):
    await ctx.channel.purge(limit=amount+1)

  @commands.command()
  async def gen(self, ctx, amount : int = None):
    val = ""
    result = ""
    amount = amount or None
    if amount == None:
      amount = 1
    if amount <= 25:
      for n in range(amount):
        for i in range(4):
          val = (random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase) + random.choice(string.ascii_lowercase) + random.choice(string.digits))
          val = list(val)
          random.shuffle(val)
          val.append('-')
          val = ''.join(val)
          result = result + val
        result = result[:-1] + "\n"
      if amount == 1:
        await ctx.send(f'```Generated code:\n\n{result}```')
      else:
        await ctx.send(f'```Generated codes:\n\n{result}```')
    elif amount > 25:
      await ctx.send("**You can't generate more then 25!**")


  @commands.command()
  async def epicgen(self, ctx, amount : int = None):
    val = ""
    result = ""
    amount = amount or None
    if amount == None:
      amount = 1
    if amount <= 25:
      for n in range(amount):
        for i in range(4):
          val = (random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + random.choice(string.ascii_uppercase) + random.choice(string.digits))
          val = list(val)
          random.shuffle(val)
          val.append('-')
          val = ''.join(val)
          result = result + val
        result = result[:-1] + "\n"
      if amount == 1:
        await ctx.send(f'```Epic games code:\n\n{result}```')
      else:
        await ctx.send(f'```Epic games codes:\n\n{result}```')
    elif amount > 25:
      await ctx.send("**You can't generate more then 25!**")

  @commands.command()
  async def iplookup(self, ctx, ip : str):
    try:
      ipurl = f"http://ip-api.com/json/{ip}"
      response = requests.get(ipurl)
      ipinfo = response.json()
      weatherurl = f"http://api.openweathermap.org/data/2.5/weather?q={ipinfo['city']}&appid=32c0db250a32c57d69209dc167edb8a7&units=metric"
      weatherresponse = requests.get(weatherurl)
      weatherinfo = weatherresponse.json()
      temp = int(weatherinfo['main']['temp'])
    except:
      return await ctx.send("**Invalid IP/Hostname given!**")

    embed = discord.Embed(title=f"IP/Host: {ip}", color=0xDB2727)
    embed.add_field(name="country:", value=f"{ipinfo['country']}")
    embed.add_field(name="Region:", value=f"{ipinfo['regionName']}")
    embed.add_field(name=f"Region Code:", value=f"{ipinfo['region']}")
    embed.add_field(name=f"City:", value=f"{ipinfo['city']}")
    embed.add_field(name=f"Zip code:", value=f"{ipinfo['zip']}")
    embed.add_field(name=f"Timezone:", value=f"{ipinfo['timezone']}")
    embed.add_field(name="ISP", value=f"{ipinfo['isp']}", inline=True)
    embed.add_field(name="Temp", value=f"{str(temp)}°C", inline=False)

    await ctx.send(embed=embed)

  @commands.command()
  async def info(self, ctx):
    embed=discord.Embed(title="Server Info", color=0xDB2727)
    embed.add_field(name="ID:", value=f"{self.bot.user.id}", inline=True)
    embed.add_field(name="Avatar:", value=f"[Link]({self.bot.user.avatar_url})", inline=True)
    embed.add_field(name="Released:", value="20/04/2021", inline=True)
    embed.add_field(name="Guild:", value="[Link](https://discord.gg/fXx7qC33bX)", inline=True)
    embed.add_field(name="Version:", value=f"{discord.__version__}", inline=True)
    embed.add_field(name="Ping:", value=f"{round(self.bot.latency * 1000)}", inline=True)
    embed.add_field(name="Member Count:", value=f"{ctx.guild.member_count}", inline=True)
    embed.set_footer(text="Bot made by: C0RRUPT3D#9099")
    await ctx.send(embed=embed)

  @commands.command()
  async def msgcount(self, ctx, channel: discord.TextChannel=None):
    channel = channel or ctx.channel
    count = 0
    async for _ in channel.history(limit=None):
      count += 1
    await ctx.send(f"There were `{count}` messages in {channel.mention}!")

  @commands.command()
  async def showcogs(self, ctx):
    cstr = '\n'
    await ctx.send('All cogs are:\n' + '`' + cstr.join(self.bot.cogs) + '`')

  @commands.command()
  async def verify(self, ctx):
    unverified = discord.utils.get(ctx.guild.roles, name="unverified")
    if unverified in ctx.author.roles:
      try:
        verify = discord.utils.get(ctx.guild.roles, name="Member")
        msg = await ctx.send('Verification has been sent in DMs')
        await msg.add_reaction('✅')

        image = ImageCaptcha(fonts=['mom.ttf'], width=350, height=100)
        resultd = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(6))
        print(resultd)
        with BytesIO() as cap:
          image.write(f"{resultd}", cap, format="png")
          cap.seek(0)
          f = discord.File(cap, filename="captcha.png")
          e = discord.Embed(title="Captcha Verification", color=0xDB2727, description="Please return me the code written on the following image.")
          e.set_image(url="attachment://captcha.png")
          await ctx.author.send(file=f, embed=e)

        def check(m):
          return m.content == resultd
        try:
          msg = await self.bot.wait_for('message', check=check, timeout=60)
        except asyncio.TimeoutError:
          return await ctx.author.send("**Please try again with s.verify**")
        e = discord.Embed(color=0xDB2727)
        await ctx.author.remove_roles(unverified)
        await ctx.author.add_roles(verify)
        e.add_field(name='Thank you for verifying!', value='You now have access to the server.')
        await ctx.author.send(embed=e)
      except Exception as e:
        print(e)
    else:
        await ctx.send('You are already verified!')

  @commands.command()
  async def mycustomstatus(self, ctx):
    for s in ctx.author.activities:
      if isinstance(s, discord.CustomActivity):
        await ctx.send(s)
      else:
        print("not found")

  @commands.command()
  async def whois(self, ctx, user_ : discord.Member=None):
    now = datetime.datetime.now()
    user_ = user_ or ctx.message.author
    usersn = discord.utils.snowflake_time(int(user_.id))

    def _stringify_time_unit(value: int, unit: str) -> str:
      """
      Returns a string to represent a value and time unit, ensuring that it uses the right plural form of the unit.

      >>> _stringify_time_unit(1, "seconds")
      "1 second"
      >>> _stringify_time_unit(24, "hours")
      "24 hours"
      >>> _stringify_time_unit(0, "minutes")
      "less than a minute"
      """
      if value == 1:
          return f"{value} {unit[:-1]}"
      elif value == 0:
          return f"less than a {unit[:-1]}"
      else:
          return f"{value} {unit}"

    def humanize_delta(delta: relativedelta, precision: str = "minutes", max_units: int = 3) -> str:
      """
      Returns a human-readable version of the relativedelta.

      precision specifies the smallest unit of time to include (e.g. "seconds", "minutes").
      max_units specifies the maximum number of units of time to include (e.g. 1 may include days but not hours).
      """
      if max_units <= 0:
          raise ValueError("max_units must be positive")

      units = (
          ("years", delta.years),
          ("months", delta.months),
          ("days", delta.days),
          ("hours", delta.hours),
          ("minutes", delta.minutes),
          ("seconds", delta.seconds),
      )

      # Add the time units that are >0, but stop at accuracy or max_units.
      time_strings = []
      unit_count = 0
      for unit, value in units:
          if value:
              if unit_count == 2:
                time_strings.append(f"{_stringify_time_unit(value, unit)}\n")
                unit_count += 1
              else:
                time_strings.append(_stringify_time_unit(value, unit))
                unit_count += 1

          if unit == precision or unit_count >= max_units:
              break

      # Add the 'and' between the last two units, if necessary
      if len(time_strings) > 1:
          time_strings[-1] = f"{time_strings[-2]} and {time_strings[-1]}"
          del time_strings[-2]

      # If nothing has been found, just make the value 0 precision, e.g. `0 days`.
      if not time_strings:
          humanized = _stringify_time_unit(0, precision)
      else:
          humanized = " ".join(time_strings)

      return humanized

    #This will find the difference between the two dates
    difference = abs(relativedelta(now, usersn))
    differenceg = abs(relativedelta(now, user_.joined_at))
    joined = user_.joined_at.strftime("%d %b %y %H:%M UTC")

    userstat = None
    for status in user_.activities:
      if isinstance(status, discord.CustomActivity):
        userstat=f"Custom status: {status}"

    if userstat == None:
      userstat = "Has no active status, is invisible/offline or is not in the bot's cache."

    async def shownames():
      with open("jsons/usernames.json", "r") as usr:
        usrfile = json.load(usr)

      try:
        if usrfile[str(user_.id) + '_' + '1']:
          lengid = 1
      except KeyError:
        lengid = 0
      try:
        if usrfile[str(user_.id) + '_' + '2']:
          lengid = 2
      except KeyError:
        pass
      try:
        if usrfile[str(user_.id) + '_' + '3']:
          lengid = 3
      except KeyError:
        pass
      try:
        if usrfile[str(user_.id) + '_' + '4']:
          lengid = 4
      except KeyError:
        pass
      try:
        if usrfile[str(user_.id) + '_' + '5']:
          lengid = 5
      except KeyError:
        pass

      if lengid == 0:
        store = "\n\nDid not found any name changes!"
      else:
        lengid = lengid + 1
        store = '\n'.join(usrfile[str(user_.id) + '_' + str(i)] for i in range(1, lengid))

      return store

    e = discord.Embed(title=f"{user_.name}", color=0xDB2727)
    e.set_thumbnail(url=f"{user_.avatar_url}")
    e.add_field(name="ID", value=f"{user_.id}", inline=True)
    e.add_field(name="Avatar", value=f"[Link]({user_.avatar_url})", inline=True)
    acdate = usersn.strftime("%d %b %y %H:%M UTC")
    e.add_field(name="Account Created", value=f"{acdate}", inline=True)
    e.add_field(name="Account Age", value=f"{humanize_delta(difference)}")
    e.add_field(name="Joined at", value=f"{joined}", inline=True)
    e.add_field(name="Join Server Age", value=f"{humanize_delta(differenceg)}", inline=True)
    e.add_field(name="Status", value=f'{userstat}', inline=False)
    e.add_field(name="5 last usernames", value=f"```\n{await shownames()}\n```")

    e.set_footer(text="Design from YAGPDB bot :)")
    await ctx.send(embed=e)

  @commands.command()
  async def showstatus(self, ctx):
    all_status = ctx.author.activities
    cnt = 0
    for status in all_status:
      if isinstance(status, discord.CustomActivity):
        await ctx.send(f'Custom status: {status.name}')
        cnt += 1

    if cnt == 0:
      return await ctx.send("Has no active status, is invisible/offline or is not in the bot's cache.")

  @commands.command()
  async def color(self, ctx, entered_color : str = None):
    try:

      # Available team colors to check
      team_color = ["blue", "yellow", "red", "purple", "green", "orange", "black"]

      # Checks if input from user is provided
      if entered_color == None:
        return await ctx.send("Please input a color!")
        
      # Checks if role exists
      role = discord.utils.get(ctx.guild.roles, name=f"{entered_color}")
      if role == None:
        return await ctx.send("Color isnt available. Our current colors are `blue`, `red`, `yellow`, `purple`, `green`, `orange`, `black`.\nPlease type **tiko color ``your color``**")

      # Checks if role is a color role
      check = False
      for role in team_color:
        print(role)
        if entered_color != role:
          check = False
        elif entered_color == role:
          check = True
          break
        
      # If it's not a color role then say that
      if check == False:
        return await ctx.send("Color isnt available. Our current colors are `blue`, `red`, `yellow`, `purple`, `green`, `orange`, `black`.\nPlease type **tiko color ``your color``**")

      # Loops over the author's roles and checks if the 
      # author already has a role if not then remove his old 
      #color role and give him the new one

      tcheck = False

      for role in ctx.author.roles:
        if str(entered_color) in str(role):
          return await ctx.send("You can't choose the same role twice!")
        for trole in team_color:
          if str(role) in str(trole):
            tcheck = True
            if tcheck == True:
              ir = discord.utils.get(ctx.guild.roles, name=f'{trole}')
              nr = discord.utils.get(ctx.guild.roles, name=f'{entered_color}')
              await ctx.author.remove_roles(ir)
              await ctx.author.add_roles(nr)
              return await ctx.send(f"Successfully added role!")

      if tcheck == False:
        print(f"{entered_color}")
        ir = discord.utils.get(ctx.guild.roles, name=f'{entered_color}')
        await ctx.author.add_roles(ir)
        return await ctx.send(f"Successfully added role!")

    except discord.Forbidden:
      await ctx.send("I don't have perms to add roles.")


  @commands.command()
  async def nitro(self, ctx):
    ncode = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(19))
    await ctx.send(f"discord.gift/{ncode}")

  @commands.command()
  async def gstart(self, ctx, timea, *, prize : str):
    def _stringify_time_unit(value: int, unit: str) -> str:
      """
      Returns a string to represent a value and time unit, ensuring that it uses the right plural form of the unit.

      >>> _stringify_time_unit(1, "seconds")
      "1 second"
      >>> _stringify_time_unit(24, "hours")
      "24 hours"
      >>> _stringify_time_unit(0, "minutes")
      "less than a minute"
      """
      if value == 1:
          return f"{value} {unit[:-1]}"
      elif value == 0:
          return f"less than a {unit[:-1]}"
      else:
          return f"{value} {unit}"

    def humanize_delta(delta: relativedelta, precision: str = "minutes", max_units: int = 2) -> str:
      """
      Returns a human-readable version of the relativedelta.

      precision specifies the smallest unit of time to include (e.g. "seconds", "minutes").
      max_units specifies the maximum number of units of time to include (e.g. 1 may include days but not hours).
      """
      if max_units <= 0:
          raise ValueError("max_units must be positive")

      units = (
          ("years", delta.years),
          ("months", delta.months),
          ("days", delta.days),
          ("hours", delta.hours),
          ("minutes", delta.minutes),
          ("seconds", delta.seconds),
      )

      # Add the time units that are >0, but stop at accuracy or max_units.
      time_strings = []
      unit_count = 0
      for unit, value in units:
          if value:
              if unit_count == 2:
                time_strings.append(f"{_stringify_time_unit(value, unit)}\n")
                unit_count += 1
              else:
                time_strings.append(_stringify_time_unit(value, unit))
                unit_count += 1

          if unit == precision or unit_count >= max_units:
              break

      # Add the 'and' between the last two units, if necessary
      if len(time_strings) > 1:
          time_strings[-1] = f"{time_strings[-2]} and {time_strings[-1]}"
          del time_strings[-2]

      # If nothing has been found, just make the value 0 precision, e.g. `0 days`.
      if not time_strings:
          humanized = _stringify_time_unit(0, precision)
      else:
          humanized = " ".join(time_strings)

      return humanized

    
    if timea == None or timea == str or timea[-2] == int:
      return await ctx.send("**Please give a valid time format: s|m|h|d**")
    if prize == None or prize == int:
      return await ctx.send("**Please specify the prize of the giveaway!**")

    if timea[-1] == 's':
      timef = 1
      if int(timea[:-1]) > 2629744:
        return await ctx.send("**You can't set the time over a month!**")
    elif timea[-1] == 'm':
      timef = 60
      if int(timea[:-1]) > 43830:
        return await ctx.send("**You can't set the time over a month!**")
    elif timea[-1] == 'h':
      timef = 3600
      if int(timea[:-1]) > 731:
        return await ctx.send("**You can't set the time over a month!**")
    elif timea[-1] == 'd':
      timef = 86400
      if int(timea[:-1]) > 31:
        return await ctx.send("**You can't set the time over a month!**")
    elif int(timea[:-1]) < 1:
      return await ctx.send("**Can't have a negative value!**")
    else:
      return await ctx.send("**Please give a valid time format: s|m|h|d**")

    ttime = int(timea[:-1])*timef
    now = datetime.datetime.now()
    end = datetime.datetime.now() + datetime.timedelta(seconds=ttime)
    difference = abs(relativedelta(now, end))

    await ctx.send(":tada:  Giveaway!  :tada:")
    embed = discord.Embed(title=f"**{prize}**", description=f"React with :tada: to enter!\nTime remaining: **{humanize_delta(difference)}**\nHosted by: {ctx.author.mention}", color=0xDB2727)

    embed.timestamp = end
    embed.set_footer(text=f"Ends at")

    my_msg = await ctx.send(embed=embed)
    await my_msg.add_reaction("🎉")
    self.cancelled = False
    await asyncio.sleep(ttime)
    if not self.cancelled:
      new_msg = await ctx.channel.fetch_message(my_msg.id) 

      usersl = await new_msg.reactions[0].users().flatten()
      usersl.pop(usersl.index(self.bot.user))

      try:
        winner = random.choice(usersl)
      except IndexError:
        return await ctx.send("There's no winner!")

      await ctx.send(f"Congratulations! {winner.mention} won **{prize}**")

  # Interactive giveaway creation
  @commands.command()
  async def gcreate(self, ctx):
    def _stringify_time_unit(value: int, unit: str) -> str:
      """
      Returns a string to represent a value and time unit, ensuring that it uses the right plural form of the unit.

      >>> _stringify_time_unit(1, "seconds")
      "1 second"
      >>> _stringify_time_unit(24, "hours")
      "24 hours"
      >>> _stringify_time_unit(0, "minutes")
      "less than a minute"
      """
      if value == 1:
          return f"{value} {unit[:-1]}"
      elif value == 0:
          return f"less than a {unit[:-1]}"
      else:
          return f"{value} {unit}"

    def humanize_delta(delta: relativedelta, precision: str = "minutes", max_units: int = 2) -> str:
      """
      Returns a human-readable version of the relativedelta.

      precision specifies the smallest unit of time to include (e.g. "seconds", "minutes").
      max_units specifies the maximum number of units of time to include (e.g. 1 may include days but not hours).
      """
      if max_units <= 0:
          raise ValueError("max_units must be positive")

      units = (
          ("years", delta.years),
          ("months", delta.months),
          ("days", delta.days),
          ("hours", delta.hours),
          ("minutes", delta.minutes),
          ("seconds", delta.seconds),
      )

      # Add the time units that are >0, but stop at accuracy or max_units.
      time_strings = []
      unit_count = 0
      for unit, value in units:
          if value:
              if unit_count == 2:
                time_strings.append(f"{_stringify_time_unit(value, unit)}\n")
                unit_count += 1
              else:
                time_strings.append(_stringify_time_unit(value, unit))
                unit_count += 1

          if unit == precision or unit_count >= max_units:
              break

      # Add the 'and' between the last two units, if necessary
      if len(time_strings) > 1:
          time_strings[-1] = f"{time_strings[-2]} and {time_strings[-1]}"
          del time_strings[-2]

      # If nothing has been found, just make the value 0 precision, e.g. `0 days`.
      if not time_strings:
          humanized = _stringify_time_unit(0, precision)
      else:
          humanized = " ".join(time_strings)

      return humanized

    chantext = """ 
    :tada: Alright! Let's set up your giveaway! First, what channel do you want the giveaway in?
    You can type `cancel` at any time to cancel creation.

    `Please type the name/id of a channel`
    """

    await ctx.send(f'{chantext}')

    def check1(m):
      global gchan
      global gchant
      try:
        if m.content.startswith("<#") and m.content.endswith(">"):
          msg = m.content[2:-1]
          if self.bot.get_channel(int(msg)):
            gchan = self.bot.get_channel(int(msg))
            gchant = self.bot.get_channel(int(msg))
            return True
          else:
            return False
        elif m.author == ctx.author and discord.utils.get(ctx.guild.text_channels, name=f'{m.content}'):
          gchant = discord.utils.get(ctx.guild.text_channels, name=f'{m.content}')
          gchan = gchan.name
          return True
        elif m.author == ctx.author and self.bot.get_channel(int(m.content)):
          gchan = self.bot.get_channel(int(m.content))
          gchant = self.bot.get_channel(int(m.content))
          return True
        else:
          return False
      except:
        pass

    try:
      await self.bot.wait_for('message', check=check1, timeout=60)
    except asyncio.TimeoutError:
      return await ctx.send("Giveaway has been timeout-ed!")

    timetext = f"""
      :tada: Sweet! The giveaway will be in {gchan}! Next, how long should the giveaway last?

      `Please enter the duration of the giveaway in seconds.`
      `Alternatively, enter a duration in minutes and include`
      `an M at the end, or days and include a D.`
      """

    await ctx.send(f'{timetext}')


    # winnertext = f"""
    # :tada: Neat! This giveaway will last 1 minute! Now, how many winners should there be?

    # `Please enter a number of winners between 1 and 20.`
    # """

    def check2(m):
      global ttime
      try:
        if m.content == str or m.content[-2] == int:
          return False

        if m.author == ctx.author and m.content[-1] == 's':
          timef = 1
          if int(m.content[:-1]) > 2629744:
            return False
          ttime = int(m.content[:-1])*timef
          return True
        elif m.author == ctx.author and m.content[-1] == 'm':
          timef = 60
          if int(m.content[:-1]) > 43830:
            return False
          ttime = int(m.content[:-1])*timef
          return True
        elif m.author == ctx.author and m.content[-1] == 'h':
          timef = 3600
          if int(m.content[:-1]) > 731:
            return False
          ttime = int(m.content[:-1])*timef
          return True
        elif m.author == ctx.author and m.content[-1] == 'd':
          timef = 86400
          if int(m.content[:-1]) > 31:
            return False
          ttime = int(m.content[:-1])*timef
          return True
        elif int(m.content[:-1]) < 1:
          return False
        else:
          return False
      except:
        pass

    try:
      await self.bot.wait_for('message', check=check2, timeout=60)
    except asyncio.TimeoutError:
      return await ctx.send("Giveaway has been timeout-ed!")

    prizetext= f"""
    :tada: Ok! Let's move on next! Finally, what do you want to give away?

    `Please enter the giveaway prize. This will also begin the giveaway.`
    """

    await ctx.send(f'{prizetext}')

    def check3(m):
      global prize
      prize = m.content
      return m.author == ctx.author

    try:
      await self.bot.wait_for('message', check=check3, timeout=60)
    except asyncio.TimeoutError:
      return await ctx.send("Giveaway has been timeout-ed!")

    now = datetime.datetime.now()
    end = datetime.datetime.now() + datetime.timedelta(seconds=ttime)
    difference = abs(relativedelta(now, end))

    await gchant.send(":tada:  Giveaway!  :tada:")
    embed = discord.Embed(title=f"**{prize}**", description=f"React with :tada: to enter!\nTime remaining: **{humanize_delta(difference)}**\nHosted by: {ctx.author.mention}", color=0xDB2727)

    embed.timestamp = end
    embed.set_footer(text=f"Ends at")

    my_msg = await gchant.send(embed=embed)
    await my_msg.add_reaction("🎉")
    self.cancelled = False
    await asyncio.sleep(ttime)
    if not self.cancelled:
      new_msg = await gchant.fetch_message(my_msg.id) 
      usersl = await new_msg.reactions[0].users().flatten()
      usersl.pop(usersl.index(self.bot.user))

      try:
        winner = random.choice(usersl)
      except IndexError:
        return await ctx.send("There's no winner!")

      await gchant.send(f"Congratulations! {winner.mention} won **{prize}**")

  @commands.command()
  async def gstop(self, ctx, id_: int, channel: discord.TextChannel):
    if id_ == None:
      return await ctx.send("`s.gstop <id> <channel>`")
    channel = channel or ctx.channel
    try:
      
      msg = await channel.fetch_message(id_)
      newEmbed = discord.Embed(title="Giveaway Cancelled", description="The giveaway has been cancelled!!", color=0xDB2727)
      #Set Giveaway cancelled
      self.cancelled = True
      await msg.edit(embed=newEmbed) 
    except:
      embed = discord.Embed(title="Failure!", description="Cannot cancel Giveaway", color=0xDB2727)
      await ctx.send(emebed=embed)

  @commands.command()
  async def greroll(self, ctx, id_: int, channel: discord.TextChannel):
    if id_ == None:
      return await ctx.send("`s.greroll <id> <channel>`")
    channel = channel or ctx.channel
    try:
      msg = await channel.fetch_message(id_)
    except:
      await ctx.send("The channel or ID mentioned was incorrect")
    users = await msg.reactions[0].users().flatten()
    if len(users) == 0:
      return await ctx.send("No one won since there's no participants!")
    if len(users) > 0:
      winner = random.choice(users)
      return await channel.send(f"**Congratulations! You won the giveaway {winner.mention}!**")

  @commands.command()
  async def proxies(self, ctx, ptype : str=None, timeout : str=None, country : str=None, anonymity : str=None, ssl : str=None):
    try:
      print(ptype)
      if ptype == None:
        return await ctx.send("`s.proxies <http/socks4/socks5/all> [5000] [US] [elite/anonymous/transparent/all] [yes/no/all]`\n\n<> are required and [] are optional!\n\n> 1. Proxy type\n> 2. Timeout (under 10000ms)\n> 3. Country (2 letters)\n> 4. Anonymity\n> 5. SSL")
      elif ptype not in ('http', 'socks4', 'socks5', 'all'):
        return await ctx.send("**You gave invalid arguments!**\n\nPlease choose from the following: `http`, `socks4` or `socks5`")

      url = 'https://api.proxyscrape.com/?request=getproxies'

      url = url + f'&proxytype={ptype}'

      if timeout != None and timeout != str:
        if int(timeout) <= 10000:
          timeout = str(timeout)
          url = url + f'&timeout={timeout}'
        elif timeout > 10000:
          return await ctx.send("**You gave invalid arguments!**\n\n> Please give a timeout that's under 10000ms")
      elif timeout == str:
        return await ctx.send("**You gave invalid arguments!**\n\n> Please only input digits!")

      if country != None:
        if len(country) == 2:
          url = url + f'&country={country}'
        elif len(country) != 2:
          return await ctx.send("**Please give a 2 lettered country code**")

      if anonymity != None:
        if anonymity in ('elite', 'anonymous', 'transparent', 'all'):
          url = url + f'&anonymity={anonymity}'
        elif anonymity not in ('elite', 'anonymous', 'transparent', 'all'):
          return await ctx.send("**You gave invalid arguments!**\n\nPlease input 1 of the following: `elite`, `anonymous`, `transparent` or `all`")

      if ssl != None:
        if ssl in ('yes', 'no', 'all'):
          url = url + f'&ssl={ssl}'
        elif ssl not in ('yes', 'no', 'all'):
          return await ctx.send("**You gave invalid arguments!**\n\nPlease input 1 of the following: `yes`, `no` or `all`")

      r = requests.get(url)
      buf = StringIO(r.text)
      f = discord.File(buf, filename=f'{ptype}.txt')
      await ctx.send(f"**{ptype}**", file=f)
    except Exception as e:
      print(e)

  @commands.command()
  async def timer(self, ctx, time_ : int):
    if time_ == None:
      return await ctx.send("`Please return an amount of seconds!\n\ns.timer <seconds>`")
    if time_ == float:
      return await ctx.send("Please return a whole number")
    if time_ > 600:
      return await ctx.send("`I am not allowed to go over 1 minutes (600 seconds)`")
    if time_ <= 0:
      return await ctx.send("`I think i can't do that...`")

    emb = discord.Embed(title="Timer", description=f"Timer has been set by {ctx.author.mention}", color=0xDB2727)
    emb.add_field(name='Time', value=f"**Seconds: {time_}**")
    emb.set_thumbnail(url="https://cdn.iconscout.com/icon/premium/png-256-thumb/timer-1572149-1332071.png")

    msg = await ctx.send(embed=emb)
    
    while True:
      time_ -= 1
      new_emb = discord.Embed(title="Timer", description=f"Timer has been set by {ctx.author.mention}", color=0xDB2727)
      new_emb.add_field(name='Time', value=f"**Seconds: {time_}**")
      new_emb.set_thumbnail(url="https://cdn.iconscout.com/icon/premium/png-256-thumb/timer-1572149-1332071.png")
      await asyncio.sleep(1)
      await msg.edit(embed=new_emb)
      if time_ == 0:
        return await ctx.send(f"**Timer rings! {ctx.author.mention}**")


  @commands.command()
  async def wolfram(self, ctx, *, args):
    # Max 2000 queries a month
    api_key = "W5JEE9-AWKY8RGJ2L"
    args = args.split()
    if len(args) > 1:
      for n, item in enumerate(args):
        if '+' in item:
          args[n] = args[n].replace('+', 'plus')
    query = '%20'.join(args)
    link = f"http://api.wolframalpha.com/v2/query?appid={api_key}&input={query}&output=json"
    response = requests.get(link)
    response = response.json()
    try:
      response = response["queryresult"]["pods"][1]["subpods"][0]["plaintext"]
    except KeyError:
      return await ctx.send("`Didn't found that query!`")

    await ctx.send(f"{ctx.author.mention} `Output: {response}`")

  @commands.command()
  async def remind(self, ctx, timea, *, msg):
    if timea == None:
      return await ctx.send("**Please give a valid time format: s|m|h|d**")

    if len(msg) > 100:
      return await ctx.send("**Length of message can't be over 100!**")

    timec = int(timea[:-1])
    if timea[-1] == 's':
      timef = 1
      if timec > 2629744:
        return await ctx.send("**You can't set the time over a month!**")
    elif timea[-1] == 'm':
      timef = 60
      if timec > 43830:
        return await ctx.send("**You can't set the time over a month!**")
    elif timea[-1] == 'h':
      timef = 3600
      if timec > 731:
        return await ctx.send("**You can't set the time over a month!**")
    elif timea[-1] == 'd':
      timef = 86400
      if timec > 31:
        return await ctx.send("**You can't set the time over a month!**")
    elif timec < 1:
      return await ctx.send("**Can't have a negative value!**")
    else:
      return await ctx.send("**Please give a valid time format: s|m|h|d**")
    
    await asyncio.sleep(timec*timef)

    await ctx.send(f":stopwatch: **Reminder - {msg}**\n||{ctx.author.mention}||")

  @commands.command()
  async def reddit(self, ctx, subr: str=None):
    try:
      if subr is None:
        subreddit = self.reddit.subreddit("memes")
      else:
        subreddit = self.reddit.subreddit(f"{subr}")
        if subreddit.over18:
          if not ctx.channel.is_nsfw():
            return await ctx.send("**This type of content isn't allowed here**")
      top = subreddit.top(limit=50)
      all_subs = []

      for submission in top:
        all_subs.append(submission)

      random_sub = random.choice(all_subs)

      if random_sub.url.startswith("https://v") or random_sub.url.startswith("https://redgifs") or random_sub.url.startswith("https://gfycat") or random_sub.url.endswith(".gif") or random_sub.url.endswith(".gifv"):
        cnt = 0
        while True:
          all_subs = []
          top = subreddit.top(limit=50)
          for submission in top:
            all_subs.append(submission)
          random_sub = random.choice(all_subs)
          print(random_sub.url)
          print(random_sub.url.startswith("https://v"))
          print(random_sub.url.startswith("https://redgifs"))
          print(random_sub.url.startswith("https://gfycat"))
          print(random_sub.url.endswith(".gif"))
          print(random_sub.url.endswith(".gifv"))
          if random_sub.url.startswith("https://v") and random_sub.url.startswith("https://redgifs") and random_sub.url.startswith("https://gfycat") and random_sub.url.endswith(".gif") and random_sub.url.endswith(".gifv") == False:
            break
          if cnt == 5:
            return await ctx.send("**Couldn't fetch picture**")
          cnt += 1

      name = random_sub.title
      url = random_sub.url

      embed = discord.Embed(title=name, color=0xDB2727, description=f"Subreddit: {subreddit}")
      embed.set_image(url=url)

      await ctx.send(embed=embed)
    except:
      return await ctx.send("**Couldn't fetch subreddit**")



def setup(bot):
  bot.add_cog(cmds(bot))