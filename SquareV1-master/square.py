import discord, datetime
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import time
from itertools import cycle
import json
import os
import random
import dbl
import praw


def get_prefix(client, message):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    return prefixes[str(message.guild.id)]


client: Bot = commands.Bot(command_prefix=get_prefix)
reddit12 = praw.Reddit(client_id='',
                     client_secret='',
                     user_agent='')


@client.event
async def on_guild_join(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "!"

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    for channel in guild.text_channels:
        try:
            embed = discord.Embed(
                colour=discord.Colour.magenta(),
                title="Thanks for inviting me!",
                description="Here's how you can get started with me:"
            )
            embed.add_field(name="Help:", value=f"Please use !help for a list of my commands",
                            inline=True)
            embed.add_field(name="Prefix:",
                            value=f"Please use !prefix <newprefix> to change the prefix for your server.",
                            inline=True)
            embed.set_footer(text=f"You can always re see this prompt again by using the intro command ")
            await channel.send(embed=embed)
            return
        except:
            pass


@client.event
async def on_guild_remove(guild):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)


@client.command()
@commands.has_permissions(ban_members=True)
async def prefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix

    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)
    await ctx.send(f"**Prefix has been changed to:** `{prefix}`")


client.remove_command("help")


@client.event
async def on_ready():
    change_status.start()
    print('I am online')
    
#leave this command 
@client.command()
async def credits(ctx):
  embed = discord.Embed(color=0xf5f5f5, title="Made by python#0001 (533069055784124437)")
  embed.add_field(name="Info", value="[This bot is based off of a public repo made by python#0001](https://github.com/squarediscordbot/SquareV1)")
  await ctx.send(embed=embed)
# or the bot will not boot.
    


token = 'dbltoken'  # set this to your DBL token
dblpy = dbl.DBLClient(client, token,)

@client.event
async def on_dbl_vote(data):
    print(data)
    channel = client.get_channel(id=701575513889701929)
    await channel.send(f"heres the vote data: `{data}`")






@client.command(aliases=["su"])
async def statusupdate(ctx, status, *,arg):
    channel = client.get_channel(id=685464675085058086)
    role =  discord.utils.get(ctx.guild.roles, name="Status")
    if ctx.author.id == 533069055784124437:
         if 'onl' in status:

            await channel.send(f"<@&702889679669821541>")
            embed = discord.Embed(
                colour=discord.Colour.green(),
                title=":green_circle: Online!",
                description=f"{arg}"
            )
            await channel.send(embed=embed)
            await client.change_presence(status = discord.Status.online, activity=discord.Activity(type=3, name=f" 100k+ people!| Square V1.1 ", ))
         if 'minor' in status:
             await channel.send(f"<@&702889679669821541>")
             embed = discord.Embed(
                 colour=discord.Colour.dark_gold(),
                 title=":yellow_circle: Minor outage",
                 description=f"{arg}"
             )
             await channel.send(embed=embed)
             await client.change_presence(status=discord.Status.idle,
                                          activity=discord.Activity(type=3, name=f" 100k+ people | MINOR OUTAGE," ))
         if 'major' in status:
             await channel.send(f"<@&702889679669821541>")
             embed = discord.Embed(
                 colour=discord.Colour.red(),
                 title=":red_circle: Major outage",
                 description=f"{arg}"
             )
             await channel.send(embed=embed)
             await client.change_presence(status=discord.Status.dnd,
                                      activity=discord.Activity(type=3, name=f" 100k+ people!| MAJOR OUTAGE ", ))
         if 'maint' in status:
            await channel.send(f"<@&702889679669821541>")
            embed = discord.Embed(
                colour= discord.Colour.blue(),
                title=":tools: Maintenance",
                description = f"{arg}"
                )
            await channel.send(embed=embed)
            await client.change_presence(status=discord.Status.idle,
                                         activity=discord.Activity(type=3, name=f" 100k+ people!| MAINTENANCE", ))

    elif ctx.author.id == 329035513665290240:
        await channel.send(f"<@&702889679669821541>")
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title=f"{arg}"
        )
        await channel.send(embed=embed)


@client.command(aliases=["ss", "SS", "Ss", "sS"])
async def squarestaff(ctx):
    embed=discord.Embed(
       color= 0x277ecd,
    )
    embed.set_author(name="Square staff team:", icon_url="https://cdn.discordapp.com/attachments/685240359566966885/701648450684715140/aac8ee71dcaba1cd75276e9b8af3ba9a.png")
    embed.add_field(name="⠀", value="Administrators:")
    embed.add_field(name="⠀", value="EditSerious#0001 | Owner ", inline=False)
    embed.add_field(name="⠀", value="notgay#6969 | Lead Developer", inline=False)
    embed.add_field(name="⠀", value="OfficiallyLost#3484 | Community Manager", inline=False)
    embed.add_field(name="⠀", value="⠀", inline=False)
    embed.add_field(name="⠀", value="Developers:")
    embed.add_field(name="⠀", value="No regular developers as of this moment.", inline=False)
    await ctx.send(embed=embed)

@client.command()
async def intro(ctx):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefix = prefixes[str(ctx.guild.id)]
    embed = discord.Embed(
        colour=discord.Colour.magenta(),
        title="Thanks for inviting me!",
        description="Here's how you can get started with me:"
    )
    embed.add_field(name="Intro:", value=f"Please use {prefix}help for a list of my commands", inline=True)
    embed.add_field(name="Prefix:",
                    value=f"Please use {prefix}prefix <newprefix> to change the prefix for your server.",
                    inline=True)
    await ctx.send(embed=embed)







@client.command()
@commands.has_permissions(manage_channels=True)
async def lock(ctx, *, role: discord.Role):
    perms = discord.Permissions()
    perms.send_messages = False
    if role.permissions.send_messages is True:
        await role.edit(permissions=perms)
        await ctx.send(f":white_check_mark: **Chatting has been disabled for `{role.name}`.**")


@client.command()
async def unlock(ctx, *, role: discord.Role):
    perms = discord.Permissions()
    perms.send_messages = True
    if role.permissions.send_messages is False:
        await role.edit(permissions=perms)
        await ctx.send(f":white_check_mark: **Chatting has been enabled for `{role.name}`.**")


@client.command(aliases=['addrole'])
@commands.has_permissions(manage_roles=True)
async def role(ctx, member: discord.Member, *, arg):
    if member.top_role > ctx.author.top_role:
        await ctx.send(f"<:TICKNOSQUARE:692171537498767380> The role {arg} is higher than your highest role ({ctx.author.top_role}) you may not assign this role to others.")
    elif member.top_role == ctx.author.top_role:
        await ctx.send(f"<:TICKNOSQUARE:692171537498767380> The role {arg} is your current highest role therefore you may not assign it to others.")
    else:
        role = discord.utils.get(ctx.guild.roles, name=arg)
        await member.add_roles(role)
        await ctx.send(f"<:TICKYESSQUARE:691812028473540658> **{member.mention} was given the role: `{role}`.**")


@client.command(aliases=['unrole', 'removerole', 'deroll', 'remrole', ])
@commands.has_permissions(manage_roles=True)
async def derole(ctx, member: discord.Member, *, arg):
    if member.top_role > ctx.author.top_role:
        await ctx.send(f"<:TICKNOSQUARE:692171537498767380> The role {arg} is higher than your highest role ({ctx.author.top_role}) you may not remove this role from others.")
    elif member.top_role == ctx.author.top_role:
        await ctx.send(f"<:TICKNOSQUARE:692171537498767380> The role {arg} is your current highest role therefore you may not remove it from others.")
    else:

        role = discord.utils.get(ctx.guild.roles, name=arg)
        await member.remove_roles(role)
        await ctx.send(f"<:TICKYESSQUARE:691812028473540658> **`{role}` was removed from {member.mention}.**")


@role.error
async def role_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f'**<:TICKNOSQUARE:692171537498767380> Hey {ctx.author.mention}, you do not have proper permissions to run this command**')
    else:
        await ctx.send(f'`{error}.` please report this to a developer if you believe that this is wrong.')


@derole.error
async def derole_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send(
            f'**<:TICKNOSQUARE:692171537498767380> Hey {ctx.author.mention}, you do not have proper permissions to run this command**')


@client.command(pass_context=True)
@commands.cooldown(2, 3, commands.BucketType.user)
async def ping(message):
    before = time.monotonic()
    message = await message.send("Calculating ...")
    ping = (time.monotonic() - before) * 1000
    await message.edit(content=f":ping_pong: Pong!  **{int(ping)}ms**")

@ping.error
async def ping_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"{ctx.author.mention}, You are using this command too fast. Please wait a couple of seconds and try again.")




@client.command()
async def status(ctx):
    embed=discord.Embed(
        colour=discord.Colour.dark_magenta(),
        title=""
              "Square's current status:"

    )
    embed.add_field(name="⠀", value="[Status](https://squarediscordbot.wixsite.com/square/status)")
    await ctx.send(embed=embed)

@client.command(aliases= ["av"])
async def avatar(ctx, member: discord.Member):
    embed = discord.Embed(
        colour=discord.Colour.blue()
    )
    embed.set_author(icon_url=member.avatar_url, name=f"{member.name}#{member.discriminator}")
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)




@client.command(aliases=["invite"])
async def server(ctx):
    await ctx.send('https://discord.gg/m2U2r5Q')

@client.command()
async def vote(ctx):
    embed=discord.Embed(
        color = 0x00db02
    )
    embed.add_field(name="Link:", value="[Vote for me by clicking here!](https://top.gg/bot/684919629365510154/vote)")
    await ctx.send(embed=embed)

@client.command(aliases=['talk'])
async def announce(ctx, *, arg):
    role_names = {r.name for r in ctx.author.roles}
    if 'D+ Permissions' not in role_names:
        await ctx.send(
            '**You do not have permission to use the talk command, if you think this is an error please say so in bug reports or message a developer.**')
        return
    elif 'D+ Permissions' in role_names:
        await ctx.channel.purge(limit=1)
        await ctx.send(arg)


@client.command(aliases=['hrsay'])
async def say(ctx, *, arg):
    role_names = {r.name for r in ctx.author.roles}
    if not ctx.author.id == 329035513665290240:
        await ctx.send(
            '**You do not have permission to use the say command as because this is only for the owner of Square, if you think this is an error please say so in bug reports or message a developer.**')
    else:
        await ctx.channel.purge(limit=1)
        await ctx.send(arg)
















@client.command()
async def whois(ctx, member: discord.Member):
    embed1 = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"Who is: `{member.name}`",

    )
    embed1.set_thumbnail(url=member.avatar_url)
    embed1.add_field(name="ID:",
                     value=f"{member.id}",
                     inline=True)
    embed1.add_field(name="Username and tag:",
                     value=f"{member.name}#{member.discriminator}",
                     inline=True)
    embed1.add_field(name="Users status:",
                     value=f"{member.status}",
                     inline=True)
    embed1.add_field(name=f"When  {member.name} joined the server:",
                     value=f"{member.joined_at.date()}",
                     inline=True)
    embed1.add_field(name=f"{member.name} account was created at:",
                     value=f"{member.created_at.date()}",
                     inline=True)

    await ctx.send(embed=embed1)
    return


@whois.error
async def whois_error(ctx, error):
    member = ctx.author
    if isinstance(error, commands.MissingRequiredArgument):
        embed1 = discord.Embed(
            colour=discord.Colour.blue(),
            title=f"Who is: `{member.name}`",

        )
        embed1.set_thumbnail(url=member.avatar_url)
        embed1.add_field(name="ID:",
                         value=f"{member.id}",
                         inline=True)
        embed1.add_field(name="Username and tag:",
                         value=f"{member.name}#{member.discriminator}",
                         inline=True)
        embed1.add_field(name="Users status:",
                         value=f"{member.status}",
                         inline=True)
        embed1.add_field(name=f"When  {member.name} joined the server:",
                         value=f"{member.joined_at.date()}",
                         inline=True)
        embed1.add_field(name=f"{member.name} account was created at:",
                         value=f"{member.created_at.date()}",
                         inline=True)
        await ctx.send(embed=embed1)
        return



@client.command()
async def serverinfo(ctx):
    embed = discord.Embed(
        colour=discord.Colour.blue(),
        title=f"Info for server: `{ctx.guild.name}`",

    )
    embed.set_thumbnail(url=ctx.guild.icon_url)
    embed.add_field(name="Server ID:",
                    value=f"{ctx.guild.id}",
                    inline=False)
    embed.add_field(name="Server Owner",
                    value=f"{ctx.guild.owner}",
                    inline=False)
    embed.add_field(name="Amount of members:",
                    value=f"{ctx.guild.member_count}",
                    inline=False)
    embed.add_field(name="Server created at:",
                    value=f"{ctx.guild.created_at.date()}",
                    inline=False)
    embed.add_field(name="Server Boosters:",
                    value=f"{len(list(ctx.guild.premium_subscribers))}",
                    inline=False)
    embed.add_field(name="Amount of categories:",
                    value=f"{len(list(ctx.guild.categories))}",
                    inline=False)
    embed.add_field(name="Amount of Text channels:",
                    value=f"{len(list(ctx.guild.text_channels))}",
                    inline=False)
    embed.add_field(name="Amount of voice channels:",
                    value=f"{len(list(ctx.guild.voice_channels))}",
                    inline=False)
    await ctx.send(embed=embed)

@client.command()
async def esay(ctx, color, *, arg):
    if 'red' in color   :
        embed = discord.Embed(
            colour=discord.Colour.red(),
            title=f"{arg}"
        )
        await ctx.send(embed=embed)
    elif "blue" in color:
        embed = discord.Embed(
            colour=discord.Colour.blue(),
            title=f"{arg}"
        )
        await ctx.send(embed=embed)
    if "yellow" in color:
        embed = discord.Embed(
            colour=discord.Colour.gold(),
            title=f"{arg}"
        )
        await ctx.send(embed=embed)
    if "green" in color:
        embed = discord.Embed(
            colour=discord.Colour.green(),
            title=f"{arg}"
        )
        await ctx.send(embed=embed)
    if "purple" in color:
        embed = discord.Embed(
            colour=discord.Colour.purple(),
            title=f"{arg}"
        )
        await ctx.send(embed=embed)
    if "orange" in color:
        embed = discord.Embed(
            colour=discord.Colour.orange(),
            title=f"{arg}"
        )
        await ctx.send(embed=embed)
with open('main.py', 'r') as f:
      r = f.read()
      half1 = 'async def '
      half2 = 'credits'
      if not f"{half1}{half2}" in str(r):
          print('Its not cool to steal work, please keep the credits command!')
          await client.close()
          return
@tasks.loop(seconds=5)
async def change_status():
    status = cycle(
        [f'Hi, I am Square! I am listening to : {len(list(client.users))} Users!',
         'Join my official server! || !server'])
    print(len(list(client.users)))
    await client.change_presence(activity=discord.Activity(type=3, name=f" 100k+ people!| Square V1.1 ",))


@client.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 702891581807788062:
        print(payload.emoji.name)
        # Find a role corresponding to the Emoji name.
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        role = discord.utils.find(lambda r : r.name == payload.emoji.name, guild.roles)

        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)
            print("done")
            await member.send(f"You were given the **{role}** role in Square.")
    elif payload.message_id == 703216652849774702:
        print(payload.emoji.name)
        # Find a role corresponding to the Emoji name.
        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)

        role = discord.utils.find(lambda r : r.name == payload.emoji.name, guild.roles)
        role2 = discord.utils.get(guild.roles, name="Not Verified")
        if role is not None:
            print(role.name + " was found!")
            print(role.id)
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.add_roles(role)
            await member.remove_roles(role2)

            print("done")
            await member.send(f"You were given the **{role}** role in Square.")

@client.event
async def on_raw_reaction_remove(payload):
    if payload.message_id == 702891581807788062:
        print(payload.emoji.name)

        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        role = discord.utils.find(lambda r : r.name == payload.emoji.name, guild.roles)

        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)

            print("done")
            await member.send(f"The **{role}** role was removed because you unreacted in Square.")
    elif payload.message_id == 703216652849774702:
        print(payload.emoji.name)

        guild_id = payload.guild_id
        guild = discord.utils.find(lambda g : g.id == guild_id, client.guilds)
        role = discord.utils.find(lambda r : r.name == payload.emoji.name, guild.roles)
        role2 = discord.utils.get(guild.roles, name="Not Verified")
        if role is not None:
            member = discord.utils.find(lambda m : m.id == payload.user_id, guild.members)
            await member.remove_roles(role)
            await member.add_roles(role2)
            print("done")
            await member.send(f"The **{role}** role was removed because you unreacted in Square.")
@client.command()
async def load(ctx, extension):
    if ctx.author.id == 533069055784124437:
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f'**extension: `{extension}` was loaded successfully** ')
    elif ctx.author.id == 329035513665290240:
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f'**extension: `{extension}` was loaded successfully** ')
    else:
        await ctx.send('**Only the head developer and owner may load extensions**')


@client.command()
async def unload(ctx, extension):
    if ctx.author.id == 533069055784124437:
        client.unload_extension(f"cogs.{extension}")
        await ctx.send(f'**extension: `{extension}` was unloaded successfully** ')
    elif ctx.author.id == 329035513665290240:
        client.unload_extension(f"cogs.{extension}")
        await ctx.send(f'**extension: `{extension}` was unloaded successfully** ')
    else:
        await ctx.send('**Only the head developer and owner may unload extensions**')


@client.command()
async def reload(ctx, extension):
    if ctx.author.id == 533069055784124437:
        client.unload_extension(f"cogs.{extension}")
        client.load_extension(f"cogs.{extension}")
        await ctx.send(f'**extension: `{extension}` was reloaded successfully** ')
    elif ctx.author.id == 329035513665290240:
        client.unload_extension(f"cogs.{extension}")
        client.unload_extension(f"cogs.{extension}")
        await ctx.send(f'**extension: `{extension}` was reloaded successfully** ')
    else:
        await ctx.send('**Only the head developer and owner may reload extensions**')




client.run('')
