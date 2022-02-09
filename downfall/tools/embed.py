
from datetime import datetime
import interactions
import config


def create_info_embed(description: str):
    return interactions.Embed(
        description = description, 
        color = config.Color.MAIN,
        timestamp = str(datetime.now()),
        footer = interactions.EmbedFooter(
            text = "Downfall Editing"
        )
    )

def create_error_embed(description: str):
    return interactions.Embed(
        description = description, 
        color = config.Color.ERROR,
        timestamp = str(datetime.now()),
        footer = interactions.EmbedFooter(
            text = "Downfall Editing"
        )
    )