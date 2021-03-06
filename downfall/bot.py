
# the bot file :D
# never give up!

import interactions, config, os, logging

# create bot instance
bot = interactions.Client(token=config.KEY)

# logging
# logging.basicConfig(level=logging.DEBUG)

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

# load cogs and begin
for cog in cog_names:
    bot.load(f'cogs.{cog}')

bot.start()