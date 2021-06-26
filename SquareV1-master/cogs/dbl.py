import dbl
import discord
from discord.ext import commands


class TopGG(commands.Cog):

    def __init__(self, client):
        self.client = client
        self.token = '' # set this to your DBL token
        self.dblpy = dbl.DBLClient(self.client, self.token, autopost=True) # Autopost will post your guild count every 30 minutes


    async def on_dbl_vote(self, data):
        print(data)
        channel = self.client.get_channel(id=701575513889701929)
        await channel.send(f"heres the vote data: `{data}`")



def setup(client):
    client.add_cog(TopGG(client))
