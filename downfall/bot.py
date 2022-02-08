
# the bot file :D
# never give up!


import interactions, config, os
import cogs.utils
import tools.embed

# create bot instance
bot = interactions.Client(token=config.KEY)

# get all cog names
cog_names = [
    x.replace('.py', '') 
    for x in os.listdir(os.path.join(os.path.dirname(os.path.realpath(__file__)), "cogs")) 
    if x.endswith('.py')
]

# ready confirm
@bot.event
async def on_ready():
    print("Bot is ready!")

for cog in cog_names:
    bot.load("cogs." + cog)
bot.start()