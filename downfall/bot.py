
# the bot file :D
# never give up!

import interactions
from secret import bot_secret

bot: interactions.Client = interactions.Client(token=bot_secret)



print("Bot started")
bot.start()