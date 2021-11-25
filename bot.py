#!/usr/bin/python

import os

import discord
from discord.ext import commands
import string
import time
from unidecode import unidecode
import re
import json
from random import choice

intents = discord.Intents.all()
# intents.members=True
bot = commands.Bot(command_prefix=('?','*'), case_insensitive=True, intents=intents)

based_copypastas = [
    "Based? Based on what? In your dick? Please shut the fuck up and use words properly you fuckin troglodyte, do you think God gave us a freedom of speech just to spew random words that have no meaning that doesn't even correlate to the topic of the conversation? Like please you always complain about why no one talks to you or no one expresses their opinions on you because you're always spewing random shit like poggers based cringe and when you try to explain what it is and you just say that it's funny like what? What the fuck is funny about that do you think you'll just become a stand-up comedian that will get a standing ovation just because you said \"cum\" in the stage? HELL NO YOU FUCKIN IDIOT, so please shut the fuck up and use words properly you dumb bitch",
    "Based on fucking what? BASED ON FYCKING WHAT? You fucking cunt, you notherfucker. All I read is \"based based based cringe cringe based\", can't you fucking come up with anything else? It feels as if I'm talking to people with fuckijng dementia or something and they keep repeating the same fucking words on loop. BASEd ON FUCKING WHAT??? THE BIBLE? THE OXFORD DICITONARY? MY HAIRY ASSHOLE? OH my God just shut the fuck up it's like you can't form a coherent sentence without using one of these saturated, retarded words that lost all meaning overtime. BASED BASED BASED CRINGE CRINGE WOKE REDPILL CRIMGE WOKE GO FUCK YOURSELF YOU LITTLE BITCH YOU CUNT YOU FUCking asshole you bitch you cunt little shit",
    "\"Based\"? Are you fucking kidding me? Your only response to this is \"Based\"? Are you so mentally handicapped that the only word you can comprehend is \"Based\" - or are you just some fucking asshole who thinks that with such a short response, they can make a statement about how meaningless what was written was? Well, I'll have you know that this was NOT meaningless, in fact, it was proof-read by several professors of literature. Don't believe me? I doubt you would, and your response to this will probably be \"Based\" once again. Do I give a fuck? No, does it look like I give even the slightest fuck about five fucking letters? I bet you took the time to type those five letters too, I bet you sat there and chuckled to yourself for 20 hearty seconds before pressing \"send\". You're so fucking pathetic. I'm honestly considering directing you to a psychiatrist, but I'm simply far too nice to do something like that. You, however, will go out of your way to make a fool out of someone by responding to a well-thought-out, intelligent, or humorous statement that probably took longer to write than you can last in bed with a chimpanzee. What do I have to say to you? Absolutely nothing. I couldn't be bothered to respond to such a worthless attempt at a response. Do you want \"Based\" on your gravestone?"
]

def main():
    bot.owner_id = 423956774593363979
    bot.IMAGES_PATH = "./images/"
    bot.GIFS_PATH = "./gifs/"

    bot.imagesMap = dict()
    bot.gifsMap = dict()
    bot.imagesMap["common"] = dict()

    for f in os.listdir(bot.IMAGES_PATH):
        if f.isdigit():
            subpath = bot.IMAGES_PATH + f + "/"
            bot.imagesMap[f] = dict()
            for ff in os.listdir(subpath):
                filename, _ = os.path.splitext(ff)
                bot.imagesMap[f][filename.lower()] = (subpath + ff)
        else:
            filename, _ = os.path.splitext(f)
            bot.imagesMap["common"][filename.lower()] = (bot.IMAGES_PATH + f)

    for f in os.listdir(bot.GIFS_PATH):
        filename, _ = os.path.splitext(f)
        bot.gifsMap[filename.lower()] = (bot.GIFS_PATH + f)

    for extension in os.listdir("extensions"):
        if extension[-3:] == '.py':
            try:
                bot.load_extension(f"extensions.{extension[:-3]}")
            except Exception as e:
                print(f"Error - Couldn't load extension {extension}\n{e}")
                continue

    bot.cooldowned_users = dict()

    try:
        with open("db/bad_words.json") as f:
            bot.bad_words = json.load(f)
    except FileNotFoundError:
        print("Bad words file not found, feature won't be able to be used.")

    bot.covidre = re.compile(r"(?:[\sdl]|^)[o0] c[o0][bv][il]de?(?:[\W\d]|$)")

    bot.run(open("./auth").readline().rstrip())

@bot.event
async def on_ready():
    print(f'{discord.version_info}')
    print(f'{bot.user} has connected to Discord!')
    await bot.change_presence(activity=discord.Game(name='My prefixes are ?/*, beep bop'))#, emoji=emoji))

@bot.event
async def on_message(message : discord.Message):
    if message.author == bot.user:
        return

    decoded = unidecode(message.content.lower())

    for bad_word in bot.bad_words:
        if bad_word == "allowlist": continue
        if message.author.id not in bot.bad_words["allowlist"].get(bot.bad_words[bad_word],list()) and (bad_word in unidecode(''.join(x for x in message.content.lower() if x not in string.whitespace + ":.,-|\\/*_()\u200a")) or bad_word in decoded):
            await message.channel.send(content=f'{message.author.mention} {discord.utils.find(lambda e: e.name.lower() == "bruh", bot.emojis) or "bruh"} sit yo\' {bot.bad_words[bad_word]} ass down')
            await message.delete()
            return

    if message.author.id in bot.cooldowned_users:
        if bot.cooldowned_users[message.author.id] < time.time():
            bot.cooldowned_users.pop(message.author.id)
        else:
            return
    if message.content.startswith(bot.command_prefix):
        content = message.content.lower()[1:]
        if content in bot.imagesMap.get(str(message.guild.id), set()):
            await message.channel.send(file=discord.File(bot.imagesMap[str(message.guild.id)][content]))
            return
        elif content in bot.imagesMap["common"]:
            await message.channel.send(file=discord.File(bot.imagesMap["common"][content]))
            return
        elif content in bot.gifsMap:
            await message.channel.send(file=discord.File(bot.gifsMap[content]))
            return

    if re.search(bot.covidre,decoded) is not None:
        await message.reply(content=f"Não é ***O*** COVID-19, é ***A*** COVID-19, stop misgendering global pandemics! {[emoji for emoji in bot.emojis if emoji.name == 'angry'][0]}", mention_author=False)

    #index_es = message.content.lower().find("el covid")
    #if index_es != -1:
    #    if len(message.content) == index_es + 8 or message.content[index_es+8] in "-1 \n":
    #        await message.reply(content=f"No es ***EL*** COVID-19, es ***LA*** COVID-19, deja de tratar pandemias globais por el género errado! {[emoji for emoji in bot.emojis if emoji.name == 'angry'][0]}", mention_author=False)

    #index_fr = message.content.lower().find("le covid")
    #if index_fr != -1:
    #    if len(message.content) == index_fr + 8 or message.content[index_fr+8] in "-1 \n":
    #        await message.reply(content=f"Ce n'est pas ***LE*** COVID-19, c'est ***LA*** COVID-19, arrête de traiter pandémies mondiales par le mauvais genre! {[emoji for emoji in bot.emojis if emoji.name == 'angry'][0]}", mention_author=False)

    if message.content.lower() == "based" or ("based " == message.content[:6].lower() and message.content[6:8].lower() not in ("on","in")) or " based" in message.content[-8:].lower():
        await message.reply(content=choice(based_copypastas), mention_author=False)

    await bot.process_commands(message)

@bot.event
async def on_message_edit(before, after):
    await on_message(after)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send(content="Nice try bruh")
    elif isinstance(error, commands.errors.MissingRequiredArgument):
        await ctx.send(content="Error - missing one or more arguments.")
    else:
        raise error
        # await bot.get_channel(id=787067233016217620).send(content=error)

@bot.event
async def on_member_remove(member):
    if not member.bot:
        channel = member.guild.system_channel
        embed = discord.Embed(title="User left the server", type="rich", description=f"**Name:** {member.name}\n**Nickname:** {member.display_name}", color=member.color)
        embed.set_thumbnail(url=member.avatar_url)
        await channel.send(embed=embed)

@bot.command(name='cooldown',hidden=True,usage="userID time(s/m/h)")
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
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

@bot.command(name='remove_cooldown',hidden=True,aliases=['rc'],usage="userID")
@commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
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
    bot.bad_words[word] = category
    with open("bad_words.txt",'a') as f:
        f.write(word + '->' + category + '\n')
        await ctx.send(content=f"Word \"{word}\" added to the list of {category} bad words.")

@bot.command(name='popbadword',hidden=True,aliases=['pbw'])
@commands.is_owner()
async def popbadword(ctx, word):
    bot.bad_words.pop(word)
    with open("bad_words.txt",'w') as f:
        for word in bot.bad_words:
            f.write(word + '->' + bot.bad_words[word] + '\n')
    await ctx.send(content=f"Word \"{word}\" removed from the list of bad words.")

@bot.command(name='kil',hidden=True)
@commands.is_owner()
async def kil(ctx):
    await bot.close()

@bot.command(name='brrr',hidden=True)
@commands.is_owner()
async def brrr(ctx):
    for extension in os.listdir("extensions"):
        if extension[-3:] == '.py':
            bot.reload_extension(f"extensions.{extension[:-3]}")

main()
