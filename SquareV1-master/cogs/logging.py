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

class Logging(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def arsetup(self, ctx, *, arg):
        db = sqlite3.connect('autorole.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT role_name from autorole WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO autorole(role_name, guild_id) VALUES(?,?)")
            val = (arg, ctx.guild.id)
            embed = discord.Embed(
                colour=discord.Colour.dark_green(),
                title=f"Auto role `{ctx.guild.name}`",
                description=f"Your auto role system has been set: `SUCCESSFULLY`"
            )

            embed.add_field(name=f"What was done:", value=f"The role was changed to: {arg}",
                            inline=False)
            await ctx.send(embed=embed)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        elif result is not None:
            sql = ("UPDATE autorole SET role_name = ? WHERE guild_id = ?")
            val = (arg, ctx.guild.id)
            embed = discord.Embed(
                colour=discord.Colour.dark_green(),
                title=f"Auto role `{ctx.guild.name}`",
                description=f"Your auto role system has been set: `SUCCESSFULLY`"
            )

            embed.add_field(name=f"What was done:", value=f"The role was updated to: {arg}",
                            inline=False)
            await ctx.send(embed=embed)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @commands.command()
    @commands.has_permissions(manage_channels=True)
    async def antilink(self, ctx, arg):
        db = sqlite3.connect('antilink.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT status from antilink WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO antilink(status, guild_id) VALUES(?,?)")
            val = (arg, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"Anti-link was set to {arg}")
        elif result is not None:
            sql = ("UPDATE antilink SET status = ? WHERE guild_id = ?")
            val = (arg, ctx.guild.id)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
            await ctx.send(f"Anti-link was set to {arg}")

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mlchannel(self, ctx, channel: discord.TextChannel):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id from main WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO main(channel_id, guild_id) VALUES(?,?)")
            val = (channel.id, ctx.guild.id)
            embed = discord.Embed(
                colour=discord.Colour.dark_green(),
                title=f"Mod logs `{ctx.guild.name}`",
                description=f"Your mod log message system has been set: `SUCCESSFULLY`"
            )

            embed.add_field(name=f"What was done:", value=f"The channel was changed to: {channel.mention}",
                            inline=False)
            await ctx.send(embed=embed)
        elif result is not None:
            sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
            val = (channel.id, ctx.guild.id)
            embed = discord.Embed(
                colour=discord.Colour.dark_green(),
                title=f"Mod logs `{ctx.guild.name}`",
                description=f"Your mod log message system has been updated: `SUCCESSFULLY`"
            )

            embed.add_field(name=f"What was done:", value=f"The channel was changed to: {channel.mention}",
                            inline=False)
            await ctx.send(embed=embed)
        cursor.execute(sql, val)
        db.commit()
        cursor.close()
        db.close()

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def alchannel(self, ctx, channel: discord.TextChannel):
        db = sqlite3.connect('action.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id from action WHERE guild_id = {ctx.guild.id}')
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO action(channel_id, guild_id) VALUES(?,?)")
            val = (channel.id, ctx.guild.id)
            embed = discord.Embed(
                colour=discord.Colour.dark_green(),
                title=f"Action logs `{ctx.guild.name}`",
                description=f"Your action log message system has been set: `SUCCESSFULLY`"
            )

            embed.add_field(name=f"What was done:", value=f"The channel was changed to: {channel.mention}",
                            inline=False)
            await ctx.send(embed=embed)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()
        elif result is not None:
            sql = ("UPDATE action SET channel_id = ? WHERE guild_id = ?")
            val = (channel.id, ctx.guild.id)
            embed = discord.Embed(
                colour=discord.Colour.dark_green(),
                title=f"Action logs `{ctx.guild.name}`",
                description=f"Your action log message system has been updated: `SUCCESSFULLY`"
            )

            embed.add_field(name=f"What was done:", value=f"The channel was changed to: {channel.mention}",
                            inline=False)
            await ctx.send(embed=embed)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()


    @commands.command()
    async def logs(self, ctx, member: discord.Member):
        db = sqlite3.connect('logs.sqlite')
        cursor1 = db.cursor()
        cursor1.execute(f'SELECT warns from logs WHERE member_id = {member.id} AND guild_id = {ctx.guild.id}')
        result1 = cursor1.fetchone()
        db1 = sqlite3.connect('logs.sqlite')
        cursor2 = db1.cursor()
        cursor2.execute(f'SELECT kicks from logs WHERE member_id = {member.id} AND guild_id = {ctx.guild.id}')
        result2 = cursor2.fetchone()
        if result1 is None:
            embed = discord.Embed(
                colour=discord.Colour.blue(),
                title=f"logs for {member.name}#{member.discriminator}",
                description=f"**Kicks: `0` Mutes: `0` Warns: `0`**"
            )
            await ctx.send(embed=embed)
        elif result1 is not None:
            if result2 is None:
                embed = discord.Embed(
                    colour=discord.Colour.blue(),
                    title=f"logs for {member.name}#{member.discriminator}",
                    description=f"**Kicks: `0` Mutes: `0` Warns: `{str(result1[0])}`**"
                )
                await ctx.send(embed=embed)
            elif result2 is not None:
                embed = discord.Embed(
                    colour=discord.Colour.blue(),
                    title=f"logs for {member.name}#{member.discriminator}",
                    description=f"**Kicks: `0` Mutes: `0` Warns: `{str(result1[0])}`**"
                )
                await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.id == 684919629365510154:
            return
        else:
            db = sqlite3.connect('action.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id from action WHERE guild_id = {message.guild.id}')
            result = cursor.fetchone()
            if result is None:
                return
            elif result is not None:

                print(message.content)
                channel = self.client.get_channel(id=int(result[0]))
                embed = discord.Embed(
                    colour=discord.Colour.blue(),
                    title="Message deleted",
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(icon_url=message.author.avatar_url, name=f"{message.author.name}#{message.author.discriminator}")
                embed.add_field(name="Message content:", value=f"{message.content}")
                embed.add_field(name="Channel:", value=f"{message.channel.mention}")
                embed.set_footer(text=f"Time of deletion:",)
                await channel.send(embed=embed)
                return

    @mlchannel.error
    async def mlchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                title=f"Mod logs `{ctx.guild.name}`",
                description=f"Your mod log message system has been updated: `UNSUCCESSFULLY`"
            )

            embed.add_field(name=f"Cause of error:", value=f"No channel mention was provided",
                            inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                title=f"Mod logs `{ctx.guild.name}`",
                description=f"Your mod log message system has been updated: `UNSUCCESSFULLY`"
            )

            embed.add_field(name=f"Cause of error:", value=f"Author missing permissions to run this command",
                            inline=False)
            await ctx.send(embed=embed)
        else:

            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                title=f"Mod logs `{ctx.guild.name}`",
                description=f"Your mod log message system has been updated: `UNSUCCESSFULLY`"
            )

            embed.add_field(name=f"Cause of error:", value=f"Error: `{error}`",
                            inline=False)
            await ctx.send(embed=embed)

    @alchannel.error
    async def alchannel_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                title=f"Action logs `{ctx.guild.name}`",
                description=f"Your action log message system has been updated: `UNSUCCESSFULLY`"
            )

            embed.add_field(name=f"Cause of error:", value=f"No channel mention was provided",
                            inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                title=f"Action logs `{ctx.guild.name}`",
                description=f"Your action log message system has been updated: `UNSUCCESSFULLY`"
            )

            embed.add_field(name=f"Cause of error:", value=f"Author missing permissions to run this command",
                            inline=False)
            await ctx.send(embed=embed)
        else:

            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                title=f"Action logs `{ctx.guild.name}`",
                description=f"Your action log message system has been updated: `UNSUCCESSFULLY`"
            )

            embed.add_field(name=f"Cause of error:", value=f"Error: `{error}`",
                            inline=False)
            await ctx.send(embed=embed)

    @arsetup.error
    async def arsetup_error(self, ctx, error):
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                title=f"Auto-role `{ctx.guild.name}`",
                description=f"Your auto-role system has been updated: `UNSUCCESSFULLY`"
            )

            embed.add_field(name=f"Cause of error:", value=f"No role name  was provided",
                            inline=False)
            await ctx.send(embed=embed)
        elif isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                title=f"Auto-role `{ctx.guild.name}`",
                description=f"Your auto-role system has been updated: `UNSUCCESSFULLY`"
            )

            embed.add_field(name=f"Cause of error:", value=f"Author missing permissions to run this command",
                            inline=False)
            await ctx.send(embed=embed)
        else:

            embed = discord.Embed(
                colour=discord.Colour.dark_red(),
                title=f"Auto-role `{ctx.guild.name}`",
                description=f"Your auto-role system has been updated: `UNSUCCESSFULLY`"
            )

            embed.add_field(name=f"Cause of error:", value=f"Error: `{error}`",
                            inline=False)
            await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == '':
            return
        if before.author.bot:
            return
        if "https://" in before.content:
            return
        elif not before.author.id == 684919629365510154:
            db = sqlite3.connect('action.sqlite')
            cursor = db.cursor()
            cursor.execute(f'SELECT channel_id from action WHERE guild_id = {before.guild.id}')
            result = cursor.fetchone()
            if result is None:
                return
            elif result is not None:


                channel = self.client.get_channel(id=int(result[0]))

                embed = discord.Embed(
                    colour=discord.Colour.blue(),
                    title="Message edited",
                    timestamp=datetime.datetime.utcnow()
                )
                embed.set_author(icon_url=before.author.avatar_url, name=f"{before.author.name}#{before.author.discriminator}")
                embed.add_field(name=f"Pre-edit content:",
                                value=f"{before.content}",
                                inline=True)
                embed.add_field(name=f"Post-edit content:",
                                value=f"{after.content}",
                                inline=True)
                embed.add_field(name=f"Channel edit was made in:",
                                value=f"{before.channel.mention}",
                                inline=False)
                embed.add_field(name=f"Message link:",
                                value=f"[Jump to edited message.]({before.jump_url})",
                                inline=False)
                embed.set_footer(text=f"Time of edit:",
                                )
                await channel.send(embed=embed)
                return


    @commands.Cog.listener()
    async def on_member_join(self, member):

        db1 = sqlite3.connect('autorole.sqlite')
        cursor1 = db1.cursor()
        cursor1.execute(f'SELECT role_name from autorole WHERE guild_id = {member.guild.id}')
        result1 = cursor1.fetchone()
        if result1 is None:
            return
        elif result1 is not None:

            role = discord.utils.get(member.guild.roles, name=f"{str(result1[0])}")
            await member.add_roles(role)




        db = sqlite3.connect('action.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id from action WHERE guild_id = {member.guild.id}')
        result = cursor.fetchone()
        if result is None:
            return
        elif result is not None:

            channel = self.client.get_channel(id=int(result[0]))
            embed = discord.Embed(color=0x02eaf2, title=f"A user has joined the server:",
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="User info",
                            value=f"{member.name}#{member.discriminator} ID `{member.id}`")
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Account creation date",
                            value=member.created_at.strftime("`%A, %B %d %Y, %H:%M:%S %p`"), inline=False)
            embed.add_field(name="Server join date", value=member.joined_at.strftime("`%A, %B %d %Y @ %H:%M:%S %p`"))

            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        db = sqlite3.connect('action.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT channel_id from action WHERE guild_id = {member.guild.id}')
        result = cursor.fetchone()
        if result is None:
            return
        elif result is not None:

            channel = self.client.get_channel(id=int(result[0]))
            embed = discord.Embed(color=0xd10000, title=f"A user has left the server:",
                                  timestamp=datetime.datetime.utcnow())
            embed.add_field(name="User info",
                            value=f"{member.name}#{member.discriminator} ID `{member.id}`")
            embed.set_thumbnail(url=member.avatar_url)
            embed.add_field(name="Account creation date", value=member.created_at.strftime("`%A, %B %d %Y, %H:%M:%S %p`"), inline=False)
            embed.add_field(name="Server join date", value=member.joined_at.strftime("`%A, %B %d %Y @ %H:%M:%S %p`"))

            await channel.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message):
        if self.client.user in message.mentions:
            with open('prefixes.json', 'r') as f:
                prefixes = json.load(f)

            prefix = prefixes[str(message.guild.id)]
            await message.channel.send(
                f'**My prefix currently is `{prefix}` but can be changed using the `prefix` command**')

        db = sqlite3.connect('antilink.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT status from antilink WHERE guild_id = {message.guild.id}')
        result = cursor.fetchone()
        try:
         if str(result[0])  == "T":
            if "https://" in message.content:
                await message.channel.purge(limit=1)
                await message.channel.send(f"Hey, **{message.author.mention}** please refrain from posting links in this server")
                await asyncio.sleep(3)
                await message.channel.purge(limit=1)
                await self.client.process_commands(message)
            elif "discord.gg/" in message.content:
                await message.channel.purge(limit=1)
                await message.channel.send(
                    f"Hey, {message.author.mention} please refrain from posting invites in this server")
                await asyncio.sleep(6.5)
                await message.channel.purge(limit=1)
                await self.client.process_commands(message)
         elif str(result[0])  == "t":


            if "https://"  in message.content:
                await message.channel.purge(limit=1)
                await message.channel.send(f"Hey, {message.author.mention} please refrain from posting links in this server")
                await asyncio.sleep(6.5)
                await message.channel.purge(limit=1)
                await self.client.process_commands(message)
            elif "discord.gg/" in message.content:
                await message.channel.purge(limit=1)
                await message.channel.send(
                    f"Hey, {message.author.mention} please refrain from posting invites in this server")
                await asyncio.sleep(6.5)
                await message.channel.purge(limit=1)
                await self.client.process_commands(message)
        except:
            pass
        if result is None:
            return

        else:
            return
            await self.client.process_commands(message)









def setup(client):
    client.add_cog(Logging(client))