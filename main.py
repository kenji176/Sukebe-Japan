from discord.enums import TeamMembershipState
import img
import asyncio
from discord import channel
from discord import File
import discord
from pilmoji import Pilmoji


client = discord.Client()
userid = []
f = open("font_text/H.txt", encoding="utf-8")
areas = f.read().split()


@client.event
async def on_ready():
    print("Logged in as")
    print(client.user.name)
    print(client.user.id)
    print("------")


@client.event
async def on_message(message):
    msg = [i for i in areas if i in message.content]
    test = message.content
    if not message.author.bot and not len(msg) == 0 and msg[0] in message.content:
        iconurl = message.author.avatar_url
        channel = client.get_channel(977486251852709888)  # 投稿するチャンネルID
        user = f"{message.author.name}#{message.author.discriminator}"
        img2 = await loop.run_in_executor(None, img.make_image, iconurl, test, user)
        file = discord.File(img2, filename="sukebe.png")
        await channel.send(file=file)


loop = asyncio.get_event_loop()
client.run("token")
