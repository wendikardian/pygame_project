import discord
from googletrans import Translator
from textblob import TextBlob

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

# word = "Bonjour"
# translator = Translator()
# translate = translator.translate(word, dest="en")
# result = translate.text
# print(result)

def translate(message):
    translator = Translator()
    translation = translator.translate(message, dest="en")
    return (translation.text)

@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    m = TextBlob(message.content)
    print(message.content)
    if message.content.startswith("!"):
        text = message.content.split("!")
        listToStr = "".join(map(str, text))
        t = translate(listToStr)
        await message.channel.send(t)
    elif m.detect_language() == "en":
        return


# @client.event
# async def on_message(message):
#     if message.content.startswith('$hello'):
#         await message.channel.send('Hello!')

client.run("MTA0ODEzODg2NDEyNjA3ODk5Ng.GfX25a.hlNXdvxv_PvzHeT_YPasBZBjNkhok3AxV6ep8s")