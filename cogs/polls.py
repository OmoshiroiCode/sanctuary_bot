import json
import discord
from discord.ext import commands, tasks


class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.emoji = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3',
                      '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3', '\U0001F51F']

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        # Remove poll
        with open('./jsons/poll.json', 'r') as file:
            poll_data = json.load(file)

        # Remove schedule
        with open('./jsons/scheduler.json', 'r') as file:
            scheduler_data = json.load(file)

        if str(message.id) in poll_data:
            poll_data.pop(str(message.id))

            with open('./jsons/poll.json', 'w') as update_poll_data:
                json.dump(poll_data, update_poll_data, indent=4)

            scheduler_data.pop(str(message.channel.id))

            with open('./jsons/scheduler.json', 'w') as update_scheduler_data:
                json.dump(scheduler_data, update_scheduler_data, indent=4)


    @commands.command()
    @commands.has_permissions(administrator=True)
    async def poll(self, ctx, title, *options):
        if len(options) > 10:
            await ctx.send(':no_entry: You can only have **10 options** at maximum!')

        elif len(options) < 1:
          return await ctx.send(':no_entry: You can only have more then 1 option at **minimum**!')

        else:
            with open('./jsons/scheduler.json', 'r') as scheduler_file:
                scheduler_data = json.load(scheduler_file)

                if str(ctx.message.channel.id) not in scheduler_data:
                    polls = [('\u200b',
                              '\n'.join([f'{self.emoji[index]} {option} \n' for index, option in enumerate(options)]),
                              False)]

                    embed = discord.Embed(title=title, colour=0xDB2727)

                    embed.set_thumbnail(
                        url=f'https://cdn.discordapp.com/icons/{ctx.message.guild.id}/{ctx.message.guild.icon}.png')

                    for name, value, inline in polls:
                        embed.add_field(name=name, value=value, inline=inline)

                    message = await ctx.send(embed=embed)

                    for item in self.emoji[:len(options)]:
                        await message.add_reaction(item)

                    # Poll data
                    with open('./jsons/poll.json', 'r') as poll_file:
                        poll_data = json.load(poll_file)
                        new_message = str(message.id)

                        poll_dictionary = dict.fromkeys(list(options), 0)
                        poll_data[new_message] = [poll_dictionary]

                        with open('./jsons/poll.json', 'w') as new_poll_data:
                            json.dump(poll_data, new_poll_data, indent=4)

                    # Poll schedule
                    scheduler_data[message.channel.id] = {'message_id': message.id}

                    with open('./jsons/scheduler.json', 'w') as new_scheduler_data:
                        json.dump(scheduler_data, new_scheduler_data, indent=4)

                else:
                    await ctx.send(f':no_entry: **Channel is currently occupied with poll!**')


def setup(bot):
  bot.add_cog(Poll(bot))