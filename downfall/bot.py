
# the bot file :D
# never give up!


import interactions, config, os

# create bot instance
bot = interactions.Client(token=config.KEY)

# get all cog names
cogs = [
    x.replace('.py', '') 
    for x in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cogs")) 
    if x.endswith('.py')
]

# ready confirm
@bot.event
async def on_ready():
    print("Bot is ready!")

for cog in cogs:
    bot.load("cogs." + cog)
bot.start()