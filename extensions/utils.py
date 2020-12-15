import discord
from discord.ext import commands

class Utils(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='serverinfo',
                    brief='Display this server\'s info.',
                    help='With this command you can see various information about this server/guild.',
                    usage='')
    async def serverinfo(self, ctx : commands.Context , user : str = ""):
        guild : discord.Guild = ctx.guild
        n_bots = len([member for member in guild.members if member.bot])
        creation_date : datetime = guild.created_at
        embed = discord.Embed(title=f'{guild.name}')
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name="Members",value=guild.member_count)\
            .add_field(name="Humans",value=f"{guild.member_count - n_bots}")\
            .add_field(name="Bots",value=f"{n_bots}")\
            .add_field(name="Text channels", value=f"{len(guild.text_channels)}")\
            .add_field(name="Voice channels", value=f"{len(guild.voice_channels)}")\
            .add_field(name="Emojis",value=f"{len(guild.emojis)}/{guild.emoji_limit}",inline=False)\
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
            member = await ctx.guild.fetch_member(user)
        elif len(ctx.message.mentions) == 1:
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

def setup(bot):
    bot.add_cog(Utils(bot))
