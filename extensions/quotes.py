import discord
from discord.ext import commands
import random
import asyncio
import json

class Quotes(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='quote',
                    brief='Allows users to interact with quotes.',
                    help='',
                    usage='')
    async def quote(self, ctx, argc=None, *opt):
        guild_id = str(ctx.guild.id)
        try:
            with open("db/quotes.json") as f:
                quotes = json.load(f)
            if guild_id not in quotes:
                quotes[guild_id] = dict()
        except FileNotFoundError:
            quotes = {'blocklist': list(), guild_id: dict()}
        if not argc:
            if len(quotes[guild_id]) == 0:
                await ctx.send(content="There are no quotes to show.")
                return
            random_quote = random.choice(list(quotes[guild_id].values()))
            await ctx.send(content=f"{random_quote['content']} - {random_quote['nick']}")
            pass
        elif argc == "add":
            if self.bot.owner_id != ctx.message.author.id and str(ctx.message.author.id) not in quotes['allowlist']:
                await ctx.send(content="Nice try bruh.")
                return
            if not opt:
                msg = ctx.message.reference
                if not msg:
                    await ctx.send(content="Error - could not find quote to add")
                    return
                m_id = msg.message_id
                guild = msg.guild_id
                message = await ctx.fetch_message(m_id)
                content = message.content
                nick = message.author.display_name
                user = message.author.id
            else:
                content = ""
                user = None
                m_id = opt[0]
                for i,n in enumerate(opt):
                    message = await ctx.fetch_message(int(n))
                    content += ("\n" if content else "") + message.content
                    if i == 0:
                        user = message.author.id
                        nick = message.author.display_name
                        guild = message.guild.id
                    if user != message.author.id:
                        await ctx.send(content="Error - quotes must be said by only one person")
                        return
            if m_id in quotes[guild_id]:
                await ctx.send(content="Error - this quote already exists.")
                return
            if user == self.bot.user.id:
                await ctx.send(content="Error - not a user quote.")
                return
            quotes[guild_id][m_id] = {'content': content, 'nick': nick, 'user': user ,'guild': guild}
            with open("db/quotes.json", "w") as f:
                json.dump(quotes, f, indent=4)
            await ctx.send(content=f"Quote {m_id} added successfully!\n\n{content} - {nick}")

        elif argc == "manual":
            if self.bot.owner_id != ctx.message.author.id and str(ctx.message.author.id) not in quotes['allowlist']:
                await ctx.send(content="Nice try bruh.")
                return
            content = opt[0].replace("\\n","\n")
            converter = commands.MemberConverter()
            user = await converter.convert(ctx, opt[1])
            m_id = str(ctx.message.id)
            quotes[guild_id][m_id] = {'content': content, 'nick': user.display_name, 'user': user.id ,'guild': ctx.guild.id}
            with open("db/quotes.json", "w") as f:
                json.dump(quotes, f, indent=4)
            await ctx.send(content=f"Quote {m_id} added successfully!\n\n{content} - {user.display_name}")
        elif argc == "me":
            if len(quotes[guild_id]) == 0:
                await ctx.send(content="There are no quotes to show.")
                return

            user_quotes = [x for x in quotes[guild_id].values() if x['user'] == ctx.message.author.id]
            if len(user_quotes) == 0:
                await ctx.send(content="Sorry, you don't have any quotes. :(")
                return

            random_quote = random.choice(user_quotes)
            await ctx.send(content=f"{random_quote['content']} - {random_quote['nick']}")
        elif argc == "rand":
            if len(quotes[guild_id]) == 0:
                await ctx.send(content="There are no quotes to show.")
                return

            user_quotes = [x for x in quotes[guild_id].values() if x['user'] == self.bot.user.id]
            if len(user_quotes) == 0:
                await ctx.send(content="Sorry, WALL-E doesn't have any quotes. :(")
                return

            random_quote = random.choice(user_quotes)
            await ctx.send(content=f"{random_quote['content']} - {random_quote['nick']}")
        elif argc == "number":
            await ctx.send(content=f"There are {len(quotes[guild_id])} quotes on this server.")
        elif argc == "search":
            if len(quotes[guild_id]) == 0:
                await ctx.send(content="There are no quotes to search for.")
                return

            matches = list()
            match = ' '.join(opt)
            for quote in quotes[guild_id].values():
                if match.lower() in quote['content'].lower():
                    matches.append(quote)

            if len(matches) == 0:
                await ctx.send(content="Sorry, no matches found for your search.")

            quote = random.choice(matches)
            await ctx.send(content=f"{quote['content']} - {quote['nick']}")
        elif argc == "pop":
            if self.bot.owner_id == ctx.message.author.id:
                if len(quotes[guild_id]) == 0:
                    await ctx.send(content="There are no quotes to remove.")
                    return
                m_id = next(reversed(quotes[guild_id]))
                quotex = quotes[guild_id].pop(m_id)
                with open("db/quotes.json", "w") as f:
                    json.dump(quotes, f, indent=4)
                await ctx.send(content=f"Quote {m_id} removed successfully!\n\n{quotex['content']} - {quotex['nick']}")
            else:
                await ctx.send(content="Nice try bruh.")
        elif argc == "remove":
            if self.bot.owner_id == ctx.message.author.id:
                if len(quotes[guild_id]) == 0:
                    await ctx.send(content="There are no quotes to remove.")
                    return
                m_id = opt[0]
                quotex = quotes[guild_id].pop(m_id)
                with open("db/quotes.json", "w") as f:
                    json.dump(quotes, f, indent=4)
                await ctx.send(content=f"Quote {m_id} removed successfully!\n\n{quotex['content']} - {quotex['nick']}")
            else:
                await ctx.send(content="Nice try bruh.")
        elif argc == "allow":
            if self.bot.owner_id == ctx.message.author.id:
                for user in opt:
                    if user not in quotes['allowlist']:
                        quotes['allowlist'].append(user)
                with open("db/quotes.json", "w") as f:
                    json.dump(quotes, f, indent=4)
                await ctx.send(content=f"User(s) {' '.join(opt)} allowed from adding quotes with success.")
            else:
                await ctx.send(content="Nice try bruh.")
        elif argc == "block":
            if self.bot.owner_id == ctx.message.author.id:
                for user in opt:
                    if user in quotes['allowlist']:
                        quotes['allowlist'].remove(user)
                with open("db/quotes.json", "w") as f:
                    json.dump(quotes, f, indent=4)
                await ctx.send(content=f"User(s) {' '.join(opt)} blocked from adding quotes with success.")
            else:
                await ctx.send(content="Nice try bruh.")
        elif argc == "fromrand" or argc == "from_rand":
            msg = ctx.message.reference
            if not msg:
                await ctx.send(content="Error - could not find quote to add")
                return
            m_id = msg.message_id
            guild = msg.guild_id
            message = await ctx.fetch_message(m_id)
            user = message.author.id
            if user != self.bot.user.id:
                await ctx.send(content="Error - not a bot quote.")
                return
            content, nick = message.content.rsplit(" - ", 1)
            nick += " (generated)"
            quotes[guild_id][m_id] = {'content': content, 'nick': nick, 'user': user ,'guild': guild}
            with open("db/quotes.json", "w") as f:
                json.dump(quotes, f, indent=4)
            await ctx.send(content=f"Quote {m_id} from randQuote added successfully!\n\n{content} - {nick}")

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
