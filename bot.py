#!/usr/bin/python

import os

import discord
from discord.ext import commands
import string
import time

if discord.version_info.minor >= 5:
    intents = discord.Intents.default()
    intents.members=True
    bot = commands.Bot(command_prefix='?', case_insensitive=True, intents=intents)
else:
    bot = commands.Bot(command_prefix='?', case_insensitive=True)

def main():
    bot.IMAGES_PATH = "./images/"
    bot.GIFS_PATH = "./gifs/"

    bot.imagesMap = dict()
    bot.gifsMap = dict()

    for f in os.listdir(bot.IMAGES_PATH):
        filename, _ = os.path.splitext(f)
        bot.imagesMap[filename.lower()] = (bot.IMAGES_PATH + f)

    for f in os.listdir(bot.GIFS_PATH):
        filename, _ = os.path.splitext(f)
        bot.gifsMap[filename.lower()] = (bot.GIFS_PATH + f)

    for extension in os.listdir("extensions"):
        if extension[-3:] == '.py':
            try:
                bot.load_extension(f"extensions.{extension[:-3]}")
            except Exception as e:
                print(e)
                continue

    bot.cooldowned_users = dict()

    bot.bad_words=dict()

    try:
        with open("./bad_words.txt") as f:
            for line in f.readlines():
                key, value = line.strip().split('->',1)
                bot.bad_words[key] = value
    except FileNotFoundError:
        print("Bad words file not found, feature won't be able to be used.")

    bot.run(open("./auth").readline().rstrip())

@bot.event
async def on_ready():
    print(f'{discord.version_info}')
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name='beep bop, my prefix is ?'))#, emoji=emoji))

@bot.event
async def on_message(message : discord.Message):
    if message.author == bot.user:
        return

    if message.author.id != 1423956774593363979:
        for bad_word in bot.bad_words:
            if bad_word in ''.join(x for x in message.content.lower() if x not in string.whitespace + ".,-|\\/*_()") or bad_word in message.content.lower():
                await message.reply(content=discord.utils.find(lambda e: e.name.lower() == "bruh", bot.emojis) or "bruh")
                await message.delete()
                return

    if message.author.id in bot.cooldowned_users:
        if bot.cooldowned_users[message.author.id] < time.time():
            bot.cooldowned_users.pop(message.author.id)
        else:
            return
    if message.content.startswith(bot.command_prefix):
        content = message.content.lower()[1:]
        if content in bot.imagesMap:
            await message.channel.send(file=discord.File(bot.imagesMap[content]))
            return
        elif content in bot.gifsMap:
            await message.channel.send(file=discord.File(bot.gifsMap[content]))
            return
    index = message.content.lower().find("o covid")
    if index != -1:
        if (len(message.content) == index + 7 or message.content[index+7] in "-1 ") and (index == 0 or message.content[index-1] in " ndl"):
            await message.reply(content=f"Não é ***O*** COVID-19, é ***A*** COVID-19, stop misgendering global pandemics! {[emoji for emoji in bot.emojis if emoji.name == 'angry'][0]}", mention_author=False)

    index_es = message.content.lower().find("el covid")
    if index_es != -1:
        if len(message.content) == index_es + 8 or message.content[index_es+8] in "-1 \n":
            await message.reply(content=f"No es ***EL*** COVID-19, es ***LA*** COVID-19, deja de tratar pandemias globais por el género errado! {[emoji for emoji in bot.emojis if emoji.name == 'angry'][0]}", mention_author=False)

    index_fr = message.content.lower().find("le covid")
    if index_fr != -1:
        if len(message.content) == index_fr + 8 or message.content[index_fr+8] in "-1 \n":
            await message.reply(content=f"Ce n'est pas ***LE*** COVID-19, c'est ***LA*** COVID-19, arrête de traiter pandémies mondiales par le mauvais genre! {[emoji for emoji in bot.emojis if emoji.name == 'angry'][0]}", mention_author=False)

    if ("based " == message.content[:6].lower() or "based" in message.content[-10:].lower()) and "based on" not in message.content.lower():
        await message.reply(content="Based? Based on what? In your dick? Please shut the fuck up and use words properly you fuckin troglodyte, do you think God gave us a freedom of speech just to spew random words that have no meaning that doesn't even correlate to the topic of the conversation? Like please you always complain about why no one talks to you or no one expresses their opinions on you because you're always spewing random shit like poggers based cringe and when you try to explain what it is and you just say that it's funny like what? What the fuck is funny about that do you think you'll just become a stand-up comedian that will get a standing ovation just because you said \"cum\" in the stage? HELL NO YOU FUCKIN IDIOT, so please shut the fuck up and use words properly you dumb bitch", mention_author=False)

    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    await on_message(after)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(content="Nice try bruh")
    else:
        await bot.on_command_error(ctx,error)

@bot.event
async def on_member_remove(member):
    if not member.bot:
        channel = member.guild.system_channel
        embed = discord.Embed(title="User left the server", type="rich", description=f"**Name:** {member.name}\n**Nickname:** {member.display_name}", color=member.color)
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)

@bot.command(name='cooldown',hidden=True)
@commands.is_owner()
async def cooldown(ctx, user, time_in):
    time_converter = {'s':1,'m':60,'h':3600}
    if time_in[-1] in time_converter:
        time_s = int(time_in[:-1]) * time_converter[time_in[-1]]
    else:
        try:
            time_s = int(time_in)
        except:
            await ctx.send(content='Invalid time!')
            return

    user = await ctx.guild.fetch_member(''.join(x for x in user if x.isdigit()))
    if user.id in bot.cooldowned_users:
        bot.cooldowned_users.pop(user.id)
    bot.cooldowned_users[user.id] = time.time() + time_s
    await ctx.send(content=f"{user.mention} has been put on a {time_s}s cooldown.")

@bot.command(name='remove_cooldown',hidden=True,aliases=['rc'])
@commands.is_owner()
async def remove_cooldown(ctx, user):
    user = await ctx.guild.fetch_member(''.join(x for x in user if x.isdigit()))
    if user.id in bot.cooldowned_users:
        bot.cooldowned_users.pop(user.id)
        await ctx.send(content=f"The cooldown for {user.mention} has been removed.")
    else:
        await ctx.send(content=f"This user isn't on a cooldown.")

@bot.command(name='testleave',hidden=True)
@commands.is_owner()
async def testleave(ctx):
    await on_member_remove(ctx.author)

@bot.command(name='addbadword',hidden=True,aliases=['abw'])
@commands.is_owner()
async def addbadword(ctx,word,category):
    category = category.lower()
    bot.bad_words.append(word)
    with open("bad_words.txt",'a') as f:
        f.write(word + '->' + category + '\n')
        await ctx.send(content=f"Word \"{word}\" added to the list of {category} bad words.")

@bot.command(name='popbadword',hidden=True,aliases=['pbw'])
@commands.is_owner()
async def popbadword(ctx):
    with open("bad_words.txt",'w') as f:
        for word in bot.bad_words[:-1]:
            f.write(word + '->' + bot.bad_words[word] + '\n')
    await ctx.send(content=f"Word \"{bot.bad_words.popitem()}\" removed from the list of bad words.")

@bot.command(name='kil',hidden=True)
@commands.is_owner()
async def kil(ctx):
    await bot.logout()

@bot.command(name='disable_quotes')
@commands.is_owner()
async def disable_quotes(ctx):
    await bot.unload_extension("extensions.quotes")

@bot.command(name='enable_quotes')
@commands.is_owner()
async def enable_quotes(ctx):
    await bot.load_extension("extensions.quotes")

@bot.command(name='brrr',hidden=True)
@commands.is_owner()
async def brrr(ctx):
    bot.reload_extension("extensions.quotes")
    bot.reload_extension("extensions.interact")
    bot.reload_extension("extensions.manage")

main()
