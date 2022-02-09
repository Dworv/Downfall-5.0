
import config
from tools.embed import create_error_embed

def illegal_commmand_channel(channel_id):
    return False if int(channel_id) in config.Channel.ALLOWED else create_error_embed("You can't use that command in this channel!")
    