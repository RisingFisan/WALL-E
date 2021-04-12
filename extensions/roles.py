import discord
from discord.ext import commands
import json
from colour import Color

class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='myrole',
                    brief='create, apply, edit or remove your custom role',
                    usage="(new/apply/remove/edit) [...] - see full usage below",
                    help="""This command allows you to create a unique role for you. It won't have any permissions, just a name and a color.

You can use:
?myrole new [name] [color] - to create a new role with the specified name and color.
?myrole apply - to apply your role, in case you removed it.
?myrole remove - to remove your custom role.
?myrole edit name/color [new_value] - to edit an attribute of your custom role.

NOTE: the color attribute can be a name, like 'blue' or 'red', or an RGB hex code, like "#00ff00" or "#63bb9c."
""")
    async def myrole(self, ctx, argc, *argv):
        guild = ctx.guild.id

        try:
            with open("db/roles.json") as f:
                roles = json.load(f)
        except FileNotFoundError:
            roles = {str(guild): dict()}

        user_id = str(ctx.author.id)

        if argc == "new": # -----------------------------------------------------------------------------------
            if user_id in roles:
                await ctx.send(content="Error - you already have a custom role. If you don't see it, apply it with `?myrole apply`")
                return

            if len(argv) != 2:
                await ctx.send(content="Error - invalid number of arguments. The command's syntax is `?myrole new [name] [color]`")
                return

            try:
                c = Color(argv[1])
            except ValueError:
                await ctx.send(content=f"Error - {argv[1]} is an invalid color")
                return

            if argv[0] in set(r.name for r in ctx.guild.roles).union(r.get('name',"") for r in roles.values()):
                await ctx.send(content=f"Error - A role with that name already exists. Please choose another name.")
                return

            role = await add_role_to_guild(ctx.guild, argv[0], discord.Color(int(c.hex_l[1:],16)))

            roles[user_id] = {'name': argv[0], 'color': role.color.value}

            with open("db/roles.json","w") as f:
                json.dump(roles, f, indent=4)

            await ctx.author.add_roles(role)
            await ctx.send(content=f"Role {argv[0]} created with success!")

        elif argc == "apply": # -----------------------------------------------------------------------------------
            if user_id not in roles:
                await ctx.send(content="Error - you don't have a custom role. Create one first with `?myrole new [name] [color]`")
                return

            role = discord.utils.get(ctx.guild.roles, name=roles[user_id]['name'])

            if not role:
                role = await add_role_to_guild(ctx.guild, roles[user_id]['name'], roles[user_id]['color'])
            elif role in ctx.author.roles:
                await ctx.send(content="Error - you already have your custom role.")
                return

            await ctx.author.add_roles(role)
            await ctx.send(content=f"Role {role.name} added with success!")
        elif argc == "remove" or argc == "rm": # -----------------------------------------------------------------------------------
            if user_id not in roles:
                await ctx.send(content="Error - you don't have a custom role. Create one first with `?myrole new [name] [color]`")
                return

            role = discord.utils.get(ctx.guild.roles, name=roles[user_id]['name'])

            if not role or role not in ctx.author.roles:
                await ctx.send(content="Error - your custom role is not applied to you.")
                return

            await ctx.author.remove_roles(role)
            await ctx.send(content=f"Role {role.name} removed with success!")
        elif argc == "edit": # -----------------------------------------------------------------------------------
            if user_id not in roles:
                await ctx.send(content="Error - you don't have a custom role. Create one first with `?myrole new [name] [color]`")
                return

            if len(argv) != 2:
                await ctx.send(content="Error - invalid number of arguments. The command's syntax is `?myrole edit name/color [new_value]`")
                return
            
            role = discord.utils.get(ctx.guild.roles, name=roles[user_id]['name'])

            if not role:
                role = await add_role_to_guild(ctx.guild, roles[user_id]['name'], roles[user_id]['color'])

            if argv[0] == "name":
                if argv[1] in set(r.name for r in ctx.guild.roles).union(r.get('name',"") for r in roles.values()):
                    await ctx.send(content=f"Error - A role with that name already exists. Please choose another name.")
                    return
                await role.edit(name=argv[1])
                roles[user_id]['name'] = argv[1]
            elif argv[0] == "color" or argv[0] == "colour":
                try:
                    c = Color(argv[1])
                except ValueError:
                    await ctx.send(content=f"Error - {argv[1]} is an invalid color")
                    return

                await role.edit(color=discord.Color(int(c.hex_l[1:],16)))
                roles[user_id]['color'] = role.color.value
            else:
                await ctx.send(content=f"Error - {argv[0]} is an invalid argument. Valid arguments are: name, color.")
                return
        
            with open("db/roles.json","w") as f:
                json.dump(roles, f, indent=4)

            await ctx.send(content=f"Role {role.name} edited with success!")



async def add_role_to_guild(guild : discord.Guild, name, color : discord.Color):
    role = await guild.create_role(name=name, color=color)
    return role

def setup(bot):
    bot.add_cog(Roles(bot))