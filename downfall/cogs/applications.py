
import interactions

import config
from tools.embed import create_info_embed, create_error_embed
from tools import check, database



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
    async def apply_command(self, ctx: interactions.CommandContext, url: str, prerecs: bool = False):
        ### Checks and database
        # Checks for legality
        if illegal := check.illegal_commmand_channel(ctx.channel_id):
            await ctx.send(embeds=illegal, ephemeral=True)
            return
        # Adds to database
        app_return = database.new_application(ctx.author.id, url, prerecs)
        if isinstance(app_return, database.DBFail):
            await ctx.send(embeds=app_return.embeds, ephemeral=True)
            return
        application_id = app_return
        level = database.get_user(ctx.author.id)[1]
        if isinstance(level, database.DBFail):
            await ctx.send(embeds=level.embeds, ephemeral=True)
            return
        if level == 3:
            await ctx.send(embeds=create_error_embed("You are already at the maximum level."), ephemeral=True)
            return

        ### Confirms application
        # Creates the embed
        embeds = create_info_embed(
            'Your application has been submitted!',
            items = {
                'URL': url,
                'Pre-recs': str(prerecs),
                'Applicant': f'{ctx.author.user.username}#{ctx.author.user.discriminator}',
                'Level': str(level),
                'Application ID': str(application_id)
            }
        )
        # Confirms the application
        await ctx.send(embeds=embeds)

        ### Sends a report in the reviewing channel
        # Creates the embed
        rev_embed = create_info_embed(
            'A new application has been submitted!',
            items = {
                'Pre-recs': str(prerecs),
                'Applicant': f'{ctx.author.user.username}#{ctx.author.user.discriminator}',
                'Level': str(level),
                'Application ID': str(application_id)
            }
        )
        # Creates the button
        rev_button = interactions.Button(
            label='Review',
            style=interactions.ButtonStyle.PRIMARY,
            custom_id=f'applications-review?id={application_id}'
        )
        rev_components = interactions.models.component._build_components(rev_button)
        await self.client._http.create_message( #TODO MAKE BETTER WHEN FIXED
            {
                'content': url,
                'embeds': [rev_embed._json],
                'components': rev_components
            },
            config.Channel.REVIEWING
        )

def setup(client: interactions.Client):
    Applications(client)
    