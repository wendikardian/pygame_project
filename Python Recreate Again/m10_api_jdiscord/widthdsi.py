import discord
import requests
import json


def get_quote():
    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return quote


intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    elif message.content.startswith('$inspire'):
        quote = get_quote()
        print(quote)
        await message.channel.send(quote)


client.run("MTA0ODEzODg2NDEyNjA3ODk5Ng.GfX25a.hlNXdvxv_PvzHeT_YPasBZBjNkhok3AxV6ep8s")