import discord
from discord.ext import commands
import random
import asyncio

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='randQuote',
                    brief='Generates a random message.',
                    help='This command uses the recent channel\'s message history to generate a random message based on the given user\'s messages',
                    usage='[user] [channel] (no arguments defaults to the user who sent the command and the channel it was sent on.)')
    async def randomQuoteGenerator(self, ctx : commands.Context):
        user = ctx.author
        channel = ctx.channel
        if len(ctx.message.mentions) == 1:
            user = ctx.message.mentions[0]
        if len(ctx.message.channel_mentions) == 1:
            channel = ctx.message.channel_mentions[0]
        if user:
            dictionary = dict()
            prev_word = ""
            message_sent = await ctx.send(content="Generating random quote...")
            async with ctx.typing():
                messages = await channel.history(limit=2000).flatten()
                for message in reversed(messages):
                    if message.author != user or not message.content or message.content[0] in "*.!?`":
                        if prev_word:
                            dictionary.setdefault(prev_word.capitalize(), list()).append("")
                            prev_word = ""
                        continue
                    for line in message.content.splitlines():
                        if not line or line[0] == '>': continue
                        for word in line.split():
                            if prev_word:
                                dictionary.setdefault(prev_word.capitalize(), list()).append(word)
                            prev_word = word
                if len(dictionary) < 5:
                    await ctx.send(content="Not enough recent message history to generate random quote.")
                else:
                    while True:
                        sentence = list()
                        start = random.choice(list(dictionary.keys()))
                        while start:
                            sentence.append(start)
                            start = random.choice(dictionary[start.capitalize()])
                            if len(sentence) > 100: break
                        # print(sentence)
                        if len(sentence) > 1: 
                            await message_sent.edit(content=f"{' '.join(sentence)} - {user.display_name}")
                            break
        else:
            await ctx.send(content="Wait, that's illegal!")

    @commands.command(name='quoteTheRoom',
                    aliases=['quoteTR'],
                    brief='I DID NOT HIT HER!',
                    help='Outputs a random quote from the movie The Room.',
                    usage='')
    async def quoteTheRoom(self, ctx):
        quotes = read_quotes_file("db/quotes_the_room.txt")
        quote = random.choice(quotes)
        for line in quote.splitlines():
            await ctx.send(content=line)
            await asyncio.sleep(1)

def read_quotes_file(filename):
    with open(filename) as f:
        return [line.strip() for line in f.read().split('-----')]

def setup(bot):
    bot.add_cog(Quotes(bot))
