import discord
from discord.errors import HTTPException
from discord.ext import commands
import urllib.request, urllib.error, urllib.parse, json
import datetime
from asyncio import TimeoutError
import subprocess

from aiohttp import ClientSession
import html2text
import re

from numpy.core.arrayprint import DatetimeFormat

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='serverinfo',
                    brief='Display this server\'s info.',
                    help='With this command you can see various information about this server/guild.',
                    usage='')
    async def serverinfo(self, ctx : commands.Context):
        bot_m = await ctx.guild.fetch_member(self.bot.user.id)
        guild : discord.Guild = ctx.guild
        n_bots = len([member for member in guild.members if member.bot])
        creation_date : datetime = guild.created_at
        embed = discord.Embed(title=f'{guild.name}')
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Members",value=guild.member_count)\
            .add_field(name="Humans",value=f"{guild.member_count - n_bots}")\
            .add_field(name="Bots",value=f"{n_bots}")\
            .add_field(name="Text channels", value=f"{len([x for x in guild.text_channels if x.permissions_for(bot_m).read_messages])}")\
            .add_field(name="Voice channels", value=f"{len(guild.voice_channels)}")\
            .add_field(name="Emojis",value=f"{len([x for x in guild.emojis if not x.animated])}/{guild.emoji_limit}",inline=False)\
            .add_field(name="Region",value=f"{str(guild.region).capitalize()}")\
            .add_field(name="Roles",value=f"{len(guild.roles) - 1}")\
            .add_field(name="Created at",value=f"{creation_date.year}-{str(creation_date.month).rjust(2,'0')}-{creation_date.day}")
        await ctx.send(embed=embed)

    @commands.command(name='avatar',
                    brief='Show your colors!',
                    help='Use this command to show everyone your ugly-ass avatar!',
                    usage='[user|userID] (with no arguments it shows your own avatar)')
    async def avatar(self, ctx : commands.Context , user : str = ""):
        member = None
        if user.isdigit():
            try:
                member = await ctx.guild.fetch_member(user)
            except HTTPException:
                member = await self.bot.fetch_user(user)
        elif len(ctx.message.mentions) >= 1:
            member = ctx.message.mentions[0]
        elif not user:
            member = ctx.author
        else:
            await ctx.send(content='Error - invalid arguments')
        if member:
            embed = discord.Embed(title=f'{member.display_name}\'s avatar',color=member.color)
            embed.set_image(url=member.avatar_url)
            await ctx.send(embed=embed)

    @commands.command(name='time',brief='What time is it?')
    async def time(self, ctx):
        await ctx.send(content=subprocess.Popen("date",shell=True,stdout=subprocess.PIPE).communicate()[0].decode("utf-8"))

    @commands.command(name="urban",brief="Searches for a word's meaning in Urban Dictionary.",
                    aliases=['ud'])
    async def urban(self, ctx):
        word = ' '.join(ctx.message.content.split()[1:])
        url = f"http://api.urbandictionary.com/v0/define?term={'+'.join(word.split())}"
        response = urllib.request.urlopen(url)
        data = json.loads(response.read())
        definitions = data['list']
        if len(definitions) == 0:
            await ctx.send(content=f"No definitions for '{word}' found.")
            return
        n = len(definitions)
        i = 0
        msg = await ctx.send(content="Loading...")
        while True:
            embed = discord.Embed(title=definitions[i]["word"],description=f"{definitions[i]['definition']}",\
                url=definitions[i]['permalink'],timestamp=datetime.datetime.strptime(definitions[i]["written_on"].split('.')[0],"%Y-%m-%dT%H:%M:%S"))
            embed.set_author(name=definitions[i]["author"])
            example = definitions[i]['example'] if definitions[i]['example'] else 'No example given.'
            embed.add_field(name="Example:",value=example)\
                .add_field(name="👍",value=definitions[i]["thumbs_up"])\
                .add_field(name="👎",value=definitions[i]["thumbs_down"])
            embed.set_footer(text=f"Page {i+1} of {n}.")
            await msg.clear_reactions()
            await msg.edit(content=None,embed=embed)
            await msg.add_reaction("◀️")
            await msg.add_reaction("▶️")
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=300.0, check=lambda react,auth: ctx.author == auth\
                                                                                            and str(react.emoji) in ["◀️", "▶️"] and react.message.id == msg.id)
                if str(reaction.emoji) == '▶️' and i < n - 1:
                    i += 1
                elif str(reaction.emoji) == '◀️' and i > 0:
                    i -= 1
            except TimeoutError:
                break
    
    @commands.command(name="define", brief="Searches for a word's definition using Google's dictionary API.",
                    aliases=['def','dict','what_is'],
                    help="Use this command to learn the meaning(s) of a certain word. Supported languages are:\n{}".format('\n'.join(['en','hi','es','fr','ja','ru','de','it','ko','pt','ar','tr'])),
                    usage="word language_abbreviation")
    async def define(self, ctx, word, lang="en"):
        if lang=='pt': lang = 'pt-BR'
        url = f"https://api.dictionaryapi.dev/api/v2/entries/{lang}/{urllib.parse.quote('+'.join(word.split()))}"
        data, error = await get_json(url)
        if error:
            await ctx.send(error)
            return
        i = 0
        n = len(data)
        if not isinstance(data, list):
            await ctx.send(content=f"Error - no definitions found for '{word}'")
            return
        msg = await ctx.send(content="Loading...")
        while True:
            res = data[i]
            embed = discord.Embed(title=res['word'],url=url)
            embed.set_thumbnail(url="https://lh3.googleusercontent.com/R2e7I-0MQgxeJ-dkkGfDxL2PWPcR3DTGhttSloJO70ax2N0TEtcT-AlmLcMAJZyHOhhqRTTpuJjO9qVs24DUDIMYVsk=w128-h128-e365-rj-sc0x00ffffff")
            if 'origin' in res and res['origin']: embed.add_field(name='Word origin:', value=res['origin'],inline=False)
            for meaning in res['meanings']:
                defs = '\n'.join(f"{i+1}) {x['definition']}" + (f"\n`\"{x['example']}\"`" if 'example' in x else '') for i,x in enumerate(meaning['definitions']))
                if len(defs) >= 1024:
                    defs = defs[:1020] + '\n...'
                embed.add_field(name=meaning['partOfSpeech'],value=defs)
            if res['phonetics']: embed.set_author(name=f"{', '.join(x['text'] if x else ' ' for x in res['phonetics'])}")
            if n > 1:
                embed.set_footer(text=f"Page {i+1} of {n}.")
            else:
                await msg.edit(content=None, embed=embed)
                break
            await msg.clear_reactions()
            await msg.edit(content=None, embed=embed)
            await msg.add_reaction("◀️")
            await msg.add_reaction("▶️")
            try:
                reaction, user = await self.bot.wait_for("reaction_add", timeout=300.0, check=lambda react,auth: ctx.author == auth\
                                                                                            and str(react.emoji) in ["◀️", "▶️"] and react.message.id == msg.id)
                if str(reaction.emoji) == '▶️' and i < n - 1:
                    i += 1
                elif str(reaction.emoji) == '◀️' and i > 0:
                    i -= 1
            except TimeoutError:
                break

    @commands.command(name='hoogle',
                      brief="search hoogle")
    async def hoogle(self, ctx, * query : str):
        """Searches Hoggle and returns first two options
        Click title to see full search"""
        parser = html2text.HTML2Text()
        parser.mark_code = True
        url = f"https://hoogle.haskell.org?mode=json&hoogle={'+'.join(query)}&start=1"
        result, error = await get_json(url)
        if error:
            await ctx.send(error)
            return
        embed = discord.Embed(title=f"Definition of {' '.join(query)}", url=f"https://hoogle.haskell.org/?hoogle={'+'.join(query)}")
        embed.set_thumbnail(url = "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Lambda-letter-lowercase-symbol-Garamond.svg/1200px-Lambda-letter-lowercase-symbol-Garamond.svg.png")
        if not result:
            await ctx.send(content = f"No results for {' '.join(query)} found.")
        else:
            i = 0
            n = len(result)
            msg = await ctx.send(content="Loading...")
            while True:
                l = result[i]
                val = "*Module:* " + l["module"]["name"] + "\n"
                val += re.sub(r"\[\/?code\]",r"```",re.sub(r"\n(\w)", r" \1" , re.sub(r'\s{2,}', "\n", parser.handle(l["docs"]))))
                embed.remove_field(0)
                embed.add_field(name= parser.handle(l["item"]), value= val, inline=False)
                if n > 1:
                    embed.set_footer(text=f"Page {i+1} of {n}.")
                else:
                    await msg.edit(content=None, embed=embed)
                    break
                await msg.clear_reactions()
                await msg.edit(content=None, embed=embed)
                await msg.add_reaction("◀️")
                await msg.add_reaction("▶️")
                try:
                    reaction, user = await self.bot.wait_for("reaction_add", timeout=300.0, check=lambda react,auth: ctx.author == auth\
                                                                                                and str(react.emoji) in ["◀️", "▶️"] and react.message.id == msg.id)
                    if str(reaction.emoji) == '▶️' and i < n - 1:
                        i += 1
                    elif str(reaction.emoji) == '◀️' and i > 0:
                        i -= 1
                except TimeoutError:
                    break
        
    @commands.command(name='poll',
        brief="ask a question")
    async def poll(self, ctx, question, *options):
        embed = discord.Embed(title=question)
        embed.set_footer(text=f"by {ctx.author.display_name}")
        emojis = ['🇦', '🇧', '🇨', '🇩', '🇪', '🇫', '🇬', '🇭', '🇮', '🇯', '🇰', '🇱', '🇲', '🇳', '🇴', '🇵', '🇶', '🇷', '🇸', '🇹', '🇺', '🇻', '🇼', '🇽', '🇾', '🇿']
        for i,option in enumerate(options):
            embed.add_field(name=f"{emojis[i]} {option}",value="\u200b",inline=False)
        await ctx.message.delete()
        message = await ctx.send(embed=embed)
        for i in range(len(options)):
            await message.add_reaction(emojis[i])


    @commands.command(name='pi',    
                          brief='Height Calculator',    
                          help="Use this command to learn your height in the new S.I. unit \"Pipinhas\"",
                          hidden=True)    
    async def pipinhas(self, ctx, *args):
        m = re.fullmatch(r"(\d+(?:\.\d+)?)m?",''.join(args).strip())
        if m:
            c = float(m.group(1)) / 1.53
            await ctx.send("You are {:.2f} Pipinhas tall.".format(c))
        else:
            m = re.match(r"(\d+)cm", ''.join(args).strip())
            if m:
                c = float(m.group(1)) / 153.0
                await ctx.send("You are {:.2f} Pipinhas tall.".format(c))
            else:
                await ctx.send("Error - invalid height format")

async def get_json(url):
    try:
        async with ClientSession() as session:
            async with session.get(url) as response:
                result = await response.json()
        return result, None
    except:
        return None, "Something unexpected went wrong."


def setup(bot):
    bot.add_cog(Utils(bot))
