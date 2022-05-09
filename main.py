import discord.ext.commands
import json

intents = discord.Intents.all()
bot = discord.ext.commands.Bot(command_prefix='$', intents=intents)


@bot.event
async def on_ready():
    print('Ready!')


@bot.event
async def on_message(message):
    if message.channel.id == "your channel_id here":
        with open('counter.json', 'r') as f:
            counter = json.load(f)

        message_content = message.content.split(' ')
        try:
            number = int(message_content[0])
            print(message_content)
            if counter['counter'] == (number - 1):
                if str(message.author) != counter['last_message_author']:
                    await message.add_reaction('✅')
                    counter['counter'] += 1
                    counter['last_message_author'] = str(message.author)
                    if counter['counter'] > counter['highscore']:
                        counter['highscore'] = counter['counter']
                        counter['highscore_author'] = str(message.author)
                else:
                    pass
            else:
                await error(message, counter['highscore'], counter['highscore_author'])
                counter['counter'] = 0
                counter['last_message_author'] = ''

            with open('counter.json', 'w') as f:
                json.dump(counter, f)
        except ValueError:
            print('Ignoring message!')


@bot.slash_command(name="credits", description='Credits for the creator.', guild_ids=["your guild_ids here"])
async def credits(ctx):
    embed = discord.Embed(colour=discord.Colour.dark_gold(), title="Made By: Krasimir Lukanov")
    await ctx.respond('Ok!')
    await ctx.send(embed=embed)


@bot.slash_command(name="counter", description='Check the counter.', guild_ids=["your guild_ids here"])
async def counter(ctx):
    with open('counter.json', 'r') as f:
        counter = json.load(f)

    embed = discord.Embed(colour=discord.Colour.green(), title=f"Current number: {counter['counter']}")
    embed.add_field(name='Highscore:', value=f"{counter['highscore']} - set by {counter['highscore_author']}")
    await ctx.respond('Ok!')
    await ctx.send(embed=embed)


async def error(message, highscore, highscore_author):
    embed = discord.Embed(colour=discord.colour.Colour.red(), title=f"{message.author} ruined everything!",
                          description='The next valid number is 1!')
    embed.add_field(name='Highscore:', value=f"{str(highscore)} - set by {highscore_author}")
    await message.add_reaction("❌")
    await message.channel.send(embed=embed)

bot.run('your token here')
