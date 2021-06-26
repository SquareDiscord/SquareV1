import discord, datetime, time
from discord.ext import commands, tasks
from discord.ext.commands import Bot
import time
from itertools import cycle
import sqlite3
import json
import asyncio
import os
import random

class Moderation(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def warn(self, ctx, member: discord.Member, *, arg):
     if member.top_role > ctx.author.top_role:
            await ctx.send(f"<:TICKNOSQUARE:692171537498767380> That user is also a moderator/administrator.")
     elif member.top_role == ctx.author.top_role:
            await ctx.send(f"<:TICKNOSQUARE:692171537498767380> That user is also a moderator/administrator.")
     else:
      try:

        await member.send(
                 f'Hey there {member.name}, you have been warned in **{ctx.guild.name}** for: **{arg}****')

        await ctx.send(
                 f'**<:TICKYESSQUARE:691812028473540658>  {member.name}#{member.discriminator} has been warned for: {arg}.**')
      except:
        await ctx.send(f'**<:TICKYESSQUARE:691812028473540658>  {member.name}#{member.discriminator} has been warned for: {arg} but they have there dms off.**')


        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id from main WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()

        if result is None:
            return
        else:
            print(result)
            channel = self.client.get_channel(id=int(result[0]))
            embed = discord.Embed(
                colour=discord.Colour.blue(),
                title="Warning",
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(icon_url=member.avatar_url, name=f"{member.name}#{member.discriminator}")
            embed.add_field(name="Moderator:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
            embed.add_field(name="Reason for warning:", value=f"{arg}", inline=True)
            embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/684919629365510154/b2b483d4c9fe8dddb1f9639e15b4f617.webp?size=1024", text="Warned at:")
            await channel.send(embed=embed)
            cursor.close()
            db.close()
            logs = sqlite3.connect('logs.sqlite')
            cursor1 = logs.cursor()
            cursor1.execute(f'SELECT warns from logs WHERE member_id = {member.id} AND guild_id = {ctx.guild.id}')
            result1 = cursor1.fetchone()
            if result1 is None:
                w = 1
                sql = ("INSERT INTO logs(warns, member_id, guild_id) VALUES(?,?,?)")
                val = (w, member.id, ctx.guild.id)
                cursor1.execute(sql, val)
                logs.commit()
                cursor1.close()
                logs.close()
            elif result1 is not None:
                w = int(result1[0]) + 1
                print(w)
                sql = ("UPDATE logs SET warns = ? WHERE member_id = ? and guild_id = ?")
                val = (w, member.id, ctx.guild.id)
                cursor1.execute(sql, val)
                logs.commit()
                cursor1.close()
                logs.close()

    @commands.command(aliases=['clearwarns', 'cw'])
    @commands.has_permissions(kick_members=True)
    async def clearwarn(self, ctx, member: discord.Member, amount: int):
        logs = sqlite3.connect('logs.sqlite')
        cursor1 = logs.cursor()
        cursor1.execute(f'SELECT warns, member_id from logs WHERE member_id = {member.id}')
        result1 = cursor1.fetchone()
        if int(result1[0]) == 0:
            await ctx.send('<:TICKNOSQUARE:692171537498767380> **User has no warnings to clear.**')
        elif result1 is not None:
            w = int(result1[0]) - amount
            print(w)
            sql = ("UPDATE logs SET warns = ? WHERE member_id = ? and guild_id = ?")
            val = (w, member.id, ctx.guild.id)
            cursor1.execute(sql, val)
            logs.commit()
            cursor1.close()
            logs.close()
            await ctx.send(
                f'<:TICKYESSQUARE:691812028473540658> **Removed `{amount}`warn(s) from {member.name}#{member.discriminator}.** ')

    @warn.error
    async def warn_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380> Hey {ctx.author.mention}, please make sure to mention a member you want to warn. If your rules state you need a reason please attach a reason.**')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380> Hey {ctx.author.mention}, you do not have proper permissions to run this command.**')
        else:
            await ctx.send(f'`{error}.` please report this to a developer if you believe that this is wrong.')

    @commands.command(aliases=['pur'])
    @commands.has_permissions(kick_members=True)
    async def purge(self, ctx, *, amount: int):
        await ctx.channel.purge(limit=1)
        await ctx.channel.purge(limit=amount)
        await ctx.send(f"<:TICKYESSQUARE:691812028473540658> **{amount} messages was cleared!**")
        await asyncio.sleep(2)
        await ctx.channel.purge(limit=1)
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id from main WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()
        if result is None:
            return
        else:
            print(result)
            channel = self.client.get_channel(id=int(result[0]))
            embed = discord.Embed(
                colour=discord.Colour.blue(),
                title="Purge",
            )
            embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.author.name}#{ctx.author.discriminator}")
            embed.add_field(name="Moderator:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
            embed.add_field(name="Messages cleared:", value=f"{amount}", inline=True)
            embed.add_field(name="Channel that was purged:", value=f"{ctx.message.channel.mention}", inline=False)
            await channel.send(embed=embed)

    @purge.error
    async def purge_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'<:TICKNOSQUARE:692171537498767380> **Hey {ctx.author.mention}, please provide the amount of messages you would like to delete**')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380> Hey {ctx.author.mention}, you do not have proper permissions to run this command.**')
        else:
            await ctx.send(f'`{error}.` please report this to a developer if you believe that this is wrong.')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason: str = ('NO GIVEN REASON')):
        if not member:
            await ctx.send(
                f'<:TICKNOSQUARE:692171537498767380> **Hey {ctx.author.mention}, please make sure to mention a member you want to mute. If your rules state you need a reason please attach a reason.**')
            return
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.add_roles(role)
        await ctx.send(f"<:TICKYESSQUARE:691812028473540658>  **{member.name}#{member.discriminator} has been muted.**")
        embed = discord.Embed(
            colour=discord.Colour.red(),
            title="MUTED",
            description=f"You have been muted in {ctx.guild.name} for: {reason}"
        )
        await member.send(embed=embed)
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id from main WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()
        if result is None:
            return
        else:
            print(result)
            channel = self.client.get_channel(id=int(result[0]))
            embed = discord.Embed(
                colour=discord.Colour.gold(),
                title="Mute",
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(icon_url=member.avatar_url, name=f"{member.name}#{member.discriminator}")
            embed.add_field(name="Moderator:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
            embed.add_field(name="Reason for Mute:", value=f"{reason}", inline=True)
            embed.set_footer(
                icon_url="https://cdn.discordapp.com/avatars/684919629365510154/b2b483d4c9fe8dddb1f9639e15b4f617.webp?size=1024",
                text="Muted at:")
            await channel.send(embed=embed)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, member: discord.Member = None, *, reason: str = ('NO GIVEN REASON')):
        role = discord.utils.get(ctx.guild.roles, name="Muted")
        if not member:
            await ctx.send(
                f'<:TICKNOSQUARE:692171537498767380> **Hey {ctx.author.mention}, please make sure to mention a member you want to unmute. If your rules state you need a reason please attach a reason.**')
            return
        await member.remove_roles(role)
        await ctx.send(
            f"<:TICKYESSQUARE:691812028473540658> **{member.name}#{member.discriminator} has been unmuted.**")
        embed = discord.Embed(
            colour=discord.Colour.green(),
            title="UNMUTED",
            description="Welcome back."
        )

        embed.set_thumbnail(
            url="https://cdn.discordapp.com/emojis/502701211041005579.png")
        embed.add_field(name="Punishment over",
                        value=f"You've been unmuted in {ctx.guild.name} by user {ctx.author.name}",
                        inline=False)
        await member.send(embed=embed)
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id from main WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()
        if result is None:
            return
        else:
            print(result)
            channel = self.client.get_channel(id=int(result[0]))
            embed = discord.Embed(
                colour=discord.Colour.green(),
                title="Unmute",
                timestamp=datetime.datetime.utcnow()
            )
            embed.set_author(icon_url=member.avatar_url, name=f"{member.name}#{member.discriminator}")
            embed.add_field(name="Moderator:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
            embed.add_field(name="Reason for Unmute:", value=f"{reason}", inline=True)
            embed.set_footer(
                icon_url="https://cdn.discordapp.com/avatars/684919629365510154/b2b483d4c9fe8dddb1f9639e15b4f617.webp?size=1024",
                text="Unmuted at:")
            await channel.send(embed=embed)

    @mute.error
    async def mute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'<:TICKNOSQUARE:692171537498767380> **Hey {ctx.author.mention}, please make sure to mention a member you want to mute and give a reason for the mute.**')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380> Hey {ctx.author.mention}, you do not have proper permissions to run this command.**')

        else:
            await ctx.send(f"`{error}` Please report this in the support server if this is wrong. **NOTE:** Role must be named Muted in order to work.")

    @unmute.error
    async def unmute_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'<:TICKNOSQUARE:692171537498767380> **Hey {ctx.author.mention}, please make sure to mention a member you want to unmute and a reason for the unmute.**')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380> Hey {ctx.author.mention}, you do not have proper permissions to run this command.**')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason: str = ('NO GIVEN REASON')):
        if member.top_role > ctx.author.top_role:
            await ctx.send(f"<:TICKNOSQUARE:692171537498767380> That user is also a moderator/administrator.")
        elif member.top_role == ctx.author.top_role:
            await ctx.send(f"<:TICKNOSQUARE:692171537498767380> That user is also a moderator/administrator.")
        else:
            try:

                await member.send(
                    f'Hey there {member.name}, you have been kicked from **{ctx.guild.name}** for: **{reason}****')
                await member.kick()
                await ctx.send(
                    f'**<:TICKYESSQUARE:691812028473540658>  {member.name}#{member.discriminator} has been kicked for: {reason}.**')
            except:
                await member.kick()
                await ctx.send(
                    f'**<:TICKYESSQUARE:691812028473540658>  {member.name}#{member.discriminator} has been kicked for: {reason} but they have there dms off.**')

            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id from main WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if result is None:
                return
            else:
                print(result)
                channel = self.client.get_channel(id=int(result[0]))
                embed = discord.Embed(
                    colour=discord.Colour.orange(),
                    title="Kick",
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(icon_url=member.avatar_url, name=f"{member.name}#{member.discriminator}")
                embed.add_field(name="Moderator:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
                embed.add_field(name="Reason for kick:", value=f"{reason}", inline=True)
                embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/684919629365510154/b2b483d4c9fe8dddb1f9639e15b4f617.webp?size=1024" ,text="Kicked at:")
                await channel.send(embed=embed)
                logs = sqlite3.connect('logs.sqlite')
                cursor1 = logs.cursor()
                cursor1.execute(
                    f'SELECT kicks, member_id from logs WHERE member_id = {member.id} AND guild_id = {ctx.guild.id}')
                result1 = cursor1.fetchone()
                if result1 is None:
                    w = 1
                    sql = ("UPDATE logs SET kicks = ? WHERE member_id = ? and guild_id = ?")
                    val = (w, member.id, ctx.guild.id)
                    cursor1.execute(sql, val)
                    logs.commit()
                    cursor1.close()
                    logs.close()
                elif result1 is not None:
                    w = int(result1[0]) + 1
                    print(w)
                    sql = ("UPDATE logs SET kicks = ? WHERE member_id = ? and guild_id = ?")
                    val = (w, member.id, ctx.guild.id)
                    cursor1.execute(sql, val)
                    logs.commit()
                    cursor1.close()
                    logs.close()

    @kick.error
    async def kick_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380>  Hey {ctx.author.mention}, please make sure to mention a member you want to kick. If your rules state you need a reason please attach a reason.**')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380>  Hey {ctx.author.mention}, you do not have proper permissions to run this command.**')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason: str = ('NO GIVEN REASON')):

        if member.top_role > ctx.author.top_role:
            await ctx.send(f"<:TICKNOSQUARE:692171537498767380> That user is also a moderator/administrator.")
        elif member.top_role == ctx.author.top_role:
            await ctx.send(f"<:TICKNOSQUARE:692171537498767380> That user is also a moderator/administrator.")

        else:
            try:

                await ctx.send(
                    f'**<:TICKYESSQUARE:691812028473540658> {member.name}#{member.discriminator} has been banned for {reason}.**')
                await member.send(
                    f"Hey there {member.name}, you've been banned from **{ctx.guild.name}** for: **{reason}**")
            except:
                pass
                await ctx.send(
                    f'**<:TICKYESSQUARE:691812028473540658> {member.name}#{member.discriminator} has been banned for {reason} but they turned off direct messages.**')



            await member.ban(reason=reason)
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id from main WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if result is None:
                return
            else:
                print(result)
                channel = self.client.get_channel(id=int(result[0]))
                embed = discord.Embed(
                    colour=discord.Colour.dark_red(),
                    title="Ban",
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(icon_url=member.avatar_url, name=f"{member.name}#{member.discriminator}")
                embed.add_field(name="Moderator:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
                embed.add_field(name="Reason for Ban:", value=f"{reason}", inline=True)
                embed.set_footer(icon_url="https://cdn.discordapp.com/avatars/684919629365510154/b2b483d4c9fe8dddb1f9639e15b4f617.webp?size=1024", text="Banned at:")
                await channel.send(embed=embed)

    @ban.error
    async def ban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380>  Hey {ctx.author.mention}, please make sure to mention a member you want to ban. If your rules state you need a reason please attach a reason.**')
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380>  Hey {ctx.author.mention}, you do not have proper permissions to run this command.**')
        else:
            await ctx.send(f'`{error}.` please report this to a developer if you believe that this is wrong.')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_discriminator = member.split('#')

        for ban_entry in banned_users:
            user = ban_entry.user

            if (user.name, user.discriminator) == (member_name, member_discriminator):
                await ctx.guild.unban(user)
                await ctx.send(
                    f'<:TICKYESSQUARE:691812028473540658> **{user.mention} has been unbanned successfully.** ')

                db = sqlite3.connect('main.sqlite')
                cursor = db.cursor()
                cursor.execute(f'SELECT channel_id from main WHERE guild_id = {ctx.guild.id}')
                result = cursor.fetchone()
                if result is None:
                    return
                else:
                    print(result)
                    channel = self.client.get_channel(id=int(result[0]))
                    embed = discord.Embed(
                        colour=discord.Colour.dark_green(),
                        title="Unban",

                    )
                    embed.set_author(icon_url=ctx.author.avatar_url, name=f"{ctx.author.name}#{ctx.author.discriminator}")
                    embed.add_field(name="Moderator:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
                    embed.add_field(name="User who was unbanned:", value=f"{member}",
                                    inline=True)
                    await channel.send(embed=embed)

    @commands  .command(aliases=['sb', 'softb'])
    async def softban(self, ctx, member: discord.Member, reason: str = 'No given reason.'):
        if member.top_role > ctx.author.top_role:
            await ctx.send(f"<:TICKNOSQUARE:692171537498767380> That user is also a moderator/administrator.")
        elif member.top_role == ctx.author.top_role:
            await ctx.send(f"<:TICKNOSQUARE:692171537498767380> That user is also a moderator/administrator.")
        else:
            try:
                await ctx.send(
                    f'**<:TICKYESSQUARE:691812028473540658> {member.name}#{member.discriminator} has been banned for {reason}.**')
                await member.send(
                    f"Hey there {member.name}, you've been banned from **{ctx.guild.name}** for: **{reason}**")
                await member.ban()
            except:
                pass
                await ctx.send(
                    f'**<:TICKYESSQUARE:691812028473540658> {member.name}#{member.discriminator} has been banned for {reason} but they turned off direct messages.**')
                await member.ban()

            await ctx.guild.unban(member)
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id from main WHERE guild_id = {ctx.guild.id}')
            result = cursor.fetchone()
            if result is None:
                return
            else:
                print(result)
                channel = self.client.get_channel(id=int(result[0]))
                embed = discord.Embed(
                    colour=discord.Colour.dark_orange(),
                    title="Softban",
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(icon_url=member.avatar_url, name=f"{member.name}#{member.discriminator}")
                embed.add_field(name="Moderator:", value=f"{ctx.author.name}#{ctx.author.discriminator}", inline=True)
                embed.add_field(name="Reason for soft ban:", value=f"{reason}", inline=True)
                embed.add_field(name="Reason for Mute:", value=f"{reason}", inline=True)
                embed.set_footer(
                    icon_url="https://cdn.discordapp.com/avatars/684919629365510154/b2b483d4c9fe8dddb1f9639e15b4f617.webp?size=1024",
                    text="Soft banned at:")
                await channel.send(embed=embed)
    @softban.error
    async def softban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"**<:TICKNOSQUARE:692171537498767380>  Hey {ctx.author.mention}, please make sure to provide a member you want to softban.**")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380>  Hey {ctx.author.mention}, you do not have proper permissions to run this command.**')
        else:
            await ctx.send(f'`{error}.` please report this to a developer if you believe that this is wrong.')

    @unban.error
    async def unban_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                f"**<:TICKNOSQUARE:692171537498767380>  Hey {ctx.author.mention}, please make sure to to type out a member you want to unban's FULL NAME AND TAG  ..**")
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                f'**<:TICKNOSQUARE:692171537498767380>  Hey {ctx.author.mention}, you do not have proper permissions to run this command.**')
        else:
            await ctx.send(f'`{error}.` please report this to a developer if you believe that this is wrong.')

def setup(client):
    client.add_cog(Moderation(client))