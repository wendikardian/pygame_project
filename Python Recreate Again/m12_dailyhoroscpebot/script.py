import discord
import pyaztro

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)
horoscope = pyaztro.Aztro(sign="aquarius")
print(horoscope.description)
# @client.event
# async def on_ready():
#     print('We have logged in as {0.user}'.format(client))

# @client.event
# async def on_message(message):
#     if message.content.startswith("Aquarius"):
#         horoscope = pyaztro.Aztro(sign="aquarius")
#         quote = "Current date "+ str(horoscope.current_date) + "\n" + "Horoscope: " + horoscope.description + "\n"+"Lucky color:" + horoscope.color
#         await message.channel.send(quote)

# client.run("MTA0ODEzODg2NDEyNjA3ODk5Ng.GfX25a.hlNXdvxv_PvzHeT_YPasBZBjNkhok3AxV6ep8s")