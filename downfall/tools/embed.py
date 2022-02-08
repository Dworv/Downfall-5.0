
from datetime import datetime
import interactions
import config


def create_info_embed(description: str):
    embed = interactions.Embed(
        description = description, 
        color = config.Color.MAIN,
        timestamp = datetime.now(),
        footer = interactions.EmbedFooter(
            text = "Downfall Editing Bot · Dworv#0001"
        )
    )
    return embed

def create_error_embed(description: str):
    embed = interactions.Embed(
        description = description, 
        color = config.Color.ERROR,
        timestamp = datetime.now(),
        footer = interactions.EmbedFooter(
            text = "Downfall Editing Bot · Dworv#0001"
        )
    )
    return embed