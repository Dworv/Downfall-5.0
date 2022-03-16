
import time
import interactions
import config


def create_info_embed(text: str, items: dict = None) -> interactions.Embed:
    if items:
        return interactions.Embed(
            title = text,
            description='\n```'
                + '\n'.join(f"{k}: {v}" for k, v in items.items())
                + '```',
            color=config.Color.MAIN,
            footer=interactions.EmbedFooter(
                text="Downfall Editing · Dworv#0001", 
                icon_url=config.ICON
            ),
    )
    else:
        return interactions.Embed(
            description=text,
            color=config.Color.MAIN,
            footer=interactions.EmbedFooter(
                text="Downfall Editing · Dworv#0001", 
                icon_url=config.ICON
            ),
        )
    
def create_error_embed(text: str) -> interactions.Embed:
    return interactions.Embed(
        description = f'**{text}**', 
        color = config.Color.ERROR,
        footer = interactions.EmbedFooter(
            text = "Downfall Editing · Dworv#0001",
            icon_url = config.ICON
        )
    )

def create_review_embeds(url, old_level, new_level, applicant_name, reviewer_name, thoughts, pros, procons, cons):

    reapp = old_level == new_level

    images = [
        "https://i.imgur.com/JiNhix7.png",
        "https://i.imgur.com/IqGUuza.png",
        "https://i.imgur.com/o8MxQ5x.png",
        "https://i.imgur.com/l2taa6w.png"
    ]
    header_url = images[0] if reapp else images[new_level]

    titles = ['Reapp', 'Trial', 'Member', 'Member+']
    result = 'Reapp' if reapp else titles[new_level]

    header_embed = interactions.Embed(
        title=f'Review of {applicant_name}',
        description = url,
        color=config.Color.MAIN,
        image=interactions.EmbedImageStruct(url=header_url)._json
    )
    thoughts_embed = interactions.Embed(
        title=f'Result: {result} (Review by {reviewer_name})',
        description=thoughts,
        color=config.Color.MAIN
    )
    procons_embed = interactions.Embed(
        title='+-',
        fields=[
            interactions.EmbedField(
                name='[+]',
                value='\n'.join(pros),
                inline=True
            ),
            interactions.EmbedField(
                name='[+-]',
                value='\n'.join(procons),
                inline=True
            ),
            interactions.EmbedField(
                name='[-]',
                value='\n'.join(cons),
                inline=True
            ),
        ],
        color=config.Color.MAIN
    )
    return [header_embed, thoughts_embed, procons_embed]

def create_user_info_embed(user: interactions.Member, user_db):
    return interactions.Embed(
        title="User Profile",
        color=config.Color.MAIN,
        author=interactions.EmbedAuthor(
            name=f"{user.user.username}#{user.user.discriminator}",
            icon_url=user.user.avatar_url
        ),
        fields=[
            interactions.EmbedField(
                name='Joined',
                value=
                '<t:'+ 
                str(int(time.mktime(user.joined_at.timetuple())))+ 
                ':R>',
                inline=True
            ),
            interactions.EmbedField(
                name='Nick',
                value=str(user.nick),
                inline=True
            ),
            interactions.EmbedField(
                name='Id',
                value=str(user.id),
                inline=True
            ),
            interactions.EmbedField(
                name='Bio',
                value=str(user_db[2]),
                inline=False
            ),
            interactions.EmbedField(
                name='Boosting',
                value=str(bool(user.user.premium_type)),
                inline=True
            ),
            interactions.EmbedField(
                name='Editor Level',
                value=str(user_db[1]),
                inline=True
            ),
            interactions.EmbedField(
                name='YouTube',
                value=str(user_db[3]),
                inline=True
            ),
        ]
    )