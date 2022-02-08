
# the bot file :D
# never give up!

# python packages
import random
# site packages
import interactions
# local imports
import config
from secret import bot_secret

bot = interactions.Client(token=bot_secret)



print("Bot started")
bot.start()