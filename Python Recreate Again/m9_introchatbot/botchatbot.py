import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')

client.run("MTA0ODEzODg2NDEyNjA3ODk5Ng.GfX25a.hlNXdvxv_PvzHeT_YPasBZBjNkhok3AxV6ep8s")