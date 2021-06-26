import discord
import json
from discord.ext import commands

class Help(commands.Cog):

    def __init__(self, client):
        self.client = client

    def get_prefix(client, message):
        with open('prefixes.json', 'r') as f:
            prefixes = json.load(f)

        return prefixes[str(message.guild.id)]


    #events
    @commands.Cog.listener()
    async def on_ready(self):
        print('bot is online')

    #commands

    @commands.group(invoke_without_command=True, aliases=["cmds"])
    @commands.cooldown(1, 3, commands.BucketType.user)
    async def help(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.dark_blue(),
            title="Bot Commands",
            description="List of this Square's command categorys."
        )
        embed.add_field(name="Moderation", value="⠀", inline=False)
        embed.add_field(name="Utilities", value="⠀", inline=False)
        embed.add_field(name="Logging", value="⠀", inline=False)
        embed.add_field(name="⠀", value="To see the commands please type !help <category>", inline=False)

        await ctx.send(embed=embed)

    @help.error
    async def help_error(self, ctx, error):
        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"{ctx.author.mention}, You are using this command too fast. Please wait and then try again.")
    @help.command(aliases=["Moderation", "MODERATION", "moderation"])
    async def bodertation(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.dark_magenta(),
            title="Help Category: `Moderation`",
            description="List of this Square's moderation commands"
        )
        embed.add_field(name="⠀", value="ban", inline=True)
        embed.add_field(name="⠀", value="kick", inline=True)
        embed.add_field(name="⠀", value="warn", inline=True)
        embed.add_field(name="⠀", value="softban", inline=True)
        embed.add_field(name="⠀", value="unban", inline=True)
        embed.add_field(name="⠀", value="clearwarn", inline=True)
        embed.add_field(name="⠀", value="please do !help <command>", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=["Utilities", "UTILITIES", "utilities"])
    async def btilities(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.dark_green(),
            title="Help Category: `Utilities`",
            description="List of this Square's utility commands"
        )
        embed.add_field(name="⠀", value="role", inline=True)
        embed.add_field(name="⠀", value="derole", inline=True)
        embed.add_field(name="⠀", value="ping", inline=True)
        embed.add_field(name="⠀", value="serverinfo", inline=True)
        embed.add_field(name="⠀", value="whois", inline=True)
        embed.add_field(name="⠀", value="purge", inline=True)
        embed.add_field(name="⠀", value="arsetup", inline=True)
        embed.add_field(name="⠀", value="avatar", inline=True)
        embed.add_field(name="⠀", value="please do !help <command>", inline=False)
        await ctx.send(embed=embed)

    @help.command(aliases=["Logging", "LOGGING", "logging"])
    async def bogging(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.dark_purple(),
            title="Help Category: `Logging`",
            description="List of this Square's utility commands"
        )
        embed.add_field(name="⠀", value="alchannel", inline=True)
        embed.add_field(name="⠀", value="mlchannel", inline=True)
        embed.add_field(name="⠀", value="logs", inline=True)
        embed.add_field(name="⠀", value="antilink", inline=True)
        embed.add_field(name="⠀", value="please do !help <command>", inline=False)
        await ctx.send(embed=embed)
    @help.command()
    async def ping(self, ctx):
        await ctx.send(f"Usage: **<prefix>ping** shows discords api latency")

    @help.command()
    async def warn (self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command warn",
            description="Usage: <p>warn @user <reason>"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694180463031353445/development-gen_-_Discord_3_29_2020_12_05_19_AM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def arsetup(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command arsetup",
            description="Usage: <p>arsetup <rolename>"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/697280616709881907/bot-cmds_-_Discord_4_7_2020_11_02_56_PM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def antilink(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command antilink",
            description="Usage: <p>antilink T or F"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/697433668863655997/bot-cmds_-_Discord_4_8_2020_9_11_15_AM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def whois(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command whois",
            description="Usage: <p>whois @member"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694180363693719582/development-gen_-_Discord_3_28_2020_7_55_20_PM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command serverinfo",
            description="Usage: <p>serverinfo "
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694181527189454849/development-gen_-_Discord_3_29_2020_12_40_00_AM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def avatar(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command avatar",
            description="Usage: <p>avatar @member "
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/697283100086108231/bot-cmds_-_Discord_4_7_2020_11_13_25_PM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def alchannel (self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command alchannel",
            description="Usage: <p>alchannel #channel"
        )
        embed.set_image(url="https://cdn.discordapp.com/attachments/694180256176799836/694180307133399050/action-logs_-_Discord_3_28_2020_9_58_01_PM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def mlchannel (self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command mlchannel",
            description="Usage: <p>mlchannel #channel"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694183246396784721/development-gen_-_Discord_3_29_2020_12_28_48_AM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def kick (self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command kick",
            description="Usage: <p>kick @user <reason>"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694180395909906532/development-gen_-_Discord_3_28_2020_11_42_27_PM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def ban (self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command ban",
            description="Usage: <p>ban @user <reason>"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694400038712901642/action-logs_-_Discord_3_31_2020_12_15_49_AM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def unban (self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command unban",
            description="Usage: <p>unban username#tag"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694400010560733274/action-logs_-_Discord_3_31_2020_12_15_49_AM_3.png")
        await ctx.send(embed=embed)

    @help.command()
    async def softban (self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command ban",
            description="Usage: <p>softban @user <reason>"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694384637861953556/bot-cmd-pictures_-_Discord_3_30_2020_11_15_25_PM_2.png")
        await ctx.send(embed=embed)

    @help.command()
    async def mute (self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command mute",
            description="Usage: <p>mute @user <reason>"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694379432613249095/bot-cmd-pictures_-_Discord_3_30_2020_10_52_08_PM_3.png")
        await ctx.send(embed=embed)
    @help.command()
    async def unmute (self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command unmute",
            description="Usage: <p>unmute @user"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694187256919097425/development-gen_-_Discord_3_29_2020_12_16_28_AM_2.png")
        await ctx.send(embed=embed)
    @help.command()
    async def role (self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command role",
            description="Usage: <p>role @user <role>"
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694181421086015498/development-gen_-_Discord_3_29_2020_12_53_45_AM_2.png")
        await ctx.send(embed=embed)
    @help.command()
    async def unrole (self, ctx):
        await ctx.send(f"Usage: **<prefix>unrole <user> <role>** removes the role from the user.")

    @help.command()
    async def clearwarn(self, ctx):
        await ctx.send(f"Usage: **<prefix>clearwarn <user> <amount>** removes specified amount of warns")

    @help.command()
    async def purge(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command purge",
            description="Usage: <p>purge <amount> "
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694187608502173712/unknown.png")
        await ctx.send(embed=embed)
    @help.command()
    async def logs(self, ctx):
        embed = discord.Embed(
            colour=discord.Colour.blurple(),
            title="Instructions for command logs",
            description="Usage: <p>logs @user "
        )
        embed.set_image(
            url="https://cdn.discordapp.com/attachments/694180256176799836/694184221098377277/development-gen_-_Discord_3_29_2020_12_33_35_AM_2.png")
        await ctx.send(embed=embed)
def setup(client):
    client.add_cog(Help(client))