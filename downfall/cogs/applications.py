
import interactions 

import config
from tools.embed import create_info_embed, create_error_embed
from tools import check


class Applications(interactions.Extension):

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
    
    @interactions.extension_command(
        name="apply",
        description="Apply to become a member of the team",
        scope=[config.Guild.ID],
        options=[
            interactions.Option(
                name="url",
                description="The URL to your application",
                type=interactions.OptionType.STRING,
                required=True
            ),
            interactions.Option(
                name="prerecs",
                description="If you used pre-recs, please indicate so",
                type=interactions.OptionType.BOOLEAN,
                required=True
            )
        ]
    )
    async def apply_command(self, ctx: interactions.CommandContext, url: str, prerecs: bool):
        if illegal := check.illegal_commmand_channel(ctx.channel_id):
            await ctx.send(embeds=illegal, ephemeral=True)
            return
        embeds = create_info_embed(
            'Your application has been submitted!',
            items = {
                'URL': url,
                'Pre-recs': str(prerecs),
                'Applicant': f'{ctx.author.user.username}#{ctx.author.user.discriminator}',
            }
        )
        await ctx.send(embeds=embeds)


def setup(client: interactions.Client):
    Applications(client)