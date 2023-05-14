import discord

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.content.startswith('$hello'):
        await message.channel.send("""Hello  !
Welcome to meal Recommender System
$breakfast / $lunch / $dinner
1: food / 2:snack
command example : $breakfast 2""")
    elif message.content.startswith('$breakfast'):
        text = message.content.split("$breakfast ")
        listToStr = "".join(map(str, text))
        if int(listToStr) == 1:
            choice = "sandwich"
        elif int(listToStr) == 2:
            choice = "salad"
        recommendation = 'Food Recommendation : ' + choice
        await message.channel.send(recommendation)
        await message.channel.send(file=discord.File(choice + ".png"))
    elif message.content.startswith('$lunch'):
        text = message.content.split("$lunch ")
        listToStr = " ".join(map(str, text))
        if int(listToStr) == 1:
            choice = "spaghetti"
            await message.channel.send(file = discord.File("spaghetti.png"))
        elif int(listToStr) == 2:
            choice = "tacos"
            await message.channel.send(file = discord.File("tacos.png"))
        recommendation = 'Food Recommendation : ' + choice
        await message.channel.send(recommendation)

client.run("MTA0ODEzODg2NDEyNjA3ODk5Ng.GHVjaR.Ijsld4LPwju9QmbtKKG1aoAFQS2oFillCXYO-g")