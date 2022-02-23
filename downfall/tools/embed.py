
from datetime import datetime
import interactions
import config


def create_info_embed(text: str, items: dict = None) -> interactions.Embed:
    if items:
        description = ('\n```'
        + '\n'.join(f"{k}: {v}" for k, v in items.items())
        + '```')
    return interactions.Embed(
        title = text,
        description = description,
        color=config.Color.MAIN,
        footer=interactions.EmbedFooter(
            text="Downfall Editing · Dworv#0001", 
            icon_url=config.ICON
        ),
    )

def create_error_embed(text: str) -> interactions.Embed:
    return interactions.Embed(
        description = f'ERROR: **{text}**', 
        color = config.Color.ERROR,
        footer = interactions.EmbedFooter(
            text = "Downfall Editing · Dworv#0001",
            icon_url = config.ICON
        )
    )