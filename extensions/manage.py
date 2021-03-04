import discord
from discord.ext import commands

class Manage(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='castigo',
                    brief='Punish someone for their sins. [ADMIN ONLY]',
                    help='This command gives the role "castigo" to the specified user(s).',
                    usage='user1[, user2[, ...]] [reason]')
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def castigo(self, ctx : commands.Context):
        castigo = discord.utils.get(ctx.guild.roles, name="castigo")
        if not castigo:
            castigo = discord.utils.get(ctx.guild.roles, name="sudoers")
        for member in ctx.message.mentions:
            await member.add_roles(castigo, reason=(' '.join([x for x in ctx.message.content.split()[2:] if '<@!' not in x])))

    @commands.command(name='perdoar',
                    brief='Forgive someone for their sins. [ADMIN ONLY]',
                    help='This command removes the role "castigo" from the specified user(s).',
                    usage='user1[, user2[, ...]] [reason]')
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def perdoar(self, ctx : commands.Context):
        castigo = discord.utils.get(ctx.guild.roles, name="castigo")
        if not castigo:
            castigo = discord.utils.get(ctx.guild.roles, name="sudoers")
        for member in ctx.message.mentions:
            await member.remove_roles(castigo, reason=(' '.join([x for x in ctx.message.content.split()[2:] if '<@!' not in x])))

    @commands.command(name='add_role',
                    brief='Gives a specific role to one or more users. [ADMIN ONLY]',
                    help='This command gives the role "role_name" to the specified user(s).',
                    usage='role_name user1[, user2[, ...]]',
                    aliases=['ar','addrole'])
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def add_role(self, ctx : commands.Context, rolename : str):
        role_a = [x for x in ctx.guild.roles if x.name.lower() == rolename.lower()]
        if role_a:
            role = role_a[0]
            for member in ctx.message.mentions:
                await member.add_roles(role)
        else:
            await ctx.send(content=f"Error - role {rolename} not found")

    @commands.command(name='remove_role',
                    brief='Removes a specific role from one or more users. [ADMIN ONLY]',
                    help='This command removes the role "role_name" from the specified user(s).',
                    usage='role_name user1[, user2[, ...]]',
                    aliases=['rr','removerole'])
    @commands.check_any(commands.is_owner(), commands.has_permissions(administrator=True))
    async def remove_role(self, ctx : commands.Context, rolename : str):
        role_a = [x for x in ctx.guild.roles if x.name.lower() == rolename.lower()]
        if role_a:
            role = role_a[0]
            for member in ctx.message.mentions:
                await member.remove_roles(role)
        else:
            await ctx.send(content=f"Error - role {rolename} not found")

    @commands.command(name='mute_everyone',aliases=['me'],
                    brief='Makes everyone STFU! [ADMIN ONLY]',
                    help='This command can be used to server mute every user in the voice channel of the user who types the command.',
                    usage='')
    @commands.check_any(commands.is_owner(), commands.has_permissions(mute_members=True))
    async def mute_everyone(self, ctx : commands.Context):
        vc = ctx.author.voice.channel
        if vc:
            for member in vc.members:
                await member.edit(mute=True, reason="They're probably playing Among Us")
        else:
            await ctx.send(content="Error - User must be in a voice channel.")


    @commands.command(name='unmute_everyone',aliases=['ue'],
                    brief='Everyone can talk now! [ADMIN ONLY]',
                    help='This command can be used to server unmute every user in the voice channel of the user who types the command.',
                    usage='')
    async def unmute_everyone(self, ctx : commands.Context):
        vc = ctx.author.voice.channel
        if vc:
            if ctx.author.id == 423956774593363979 or vc.permissions_for(ctx.author).mute_members == True:
                for member in vc.members:
                    await member.edit(mute=False, reason="They're probably playing Among Us")
            else:
                await ctx.send(content="Nice try bruh")
        else:
            await ctx.send(content="Error - User must be in a voice channel.")

            
def extra_info(entry : discord.AuditLogEntry):
    if entry.action == discord.AuditLogAction.message_delete:
        return f"{entry.extra.count} messages deleted in {entry.extra.channel}."

def diff_info(entry : discord.AuditLogEntry, before : bool):
    if "role" in str(entry.action):
        if before:
            return f"Permissions: {list(iter(entry.before.permissions))}"
        else:
            return f"Permissions: {list(iter(entry.after.permissions))}"
    return ""


def setup(bot):
    bot.add_cog(Manage(bot))
