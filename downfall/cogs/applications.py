
import interactions

import config
from tools.embed import (
    create_info_embed, 
    create_error_embed, 
    create_review_embeds)
from tools import check, database, component



class Applications(interactions.Extension):

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
    async def apply_command(
        self, 
        ctx: interactions.CommandContext, 
        url: str, 
        prerecs: bool = False
        ):
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
            custom_id=component.encode_custom_id('applications-review-button', {'application_id': str(application_id)}))
        rev_components = interactions.models.component._build_components(rev_button)
        await self.client._http.create_message( #TODO MAKE BETTER WHEN FIXED
            {
                'content': url,
                'embeds': [rev_embed._json],
                'components': rev_components
            },
            config.Channel.REVIEWING
        )
    
    @interactions.extension_listener()
    async def on_component(self, ctx):
        name, entries = component.decode_custom_id(ctx.data.custom_id)
        if name == 'applications-review-button':

            application_id = int(entries['application_id'])
            app = database.get_application(application_id)

            _applicant = await self.client._http.get_member(config.Guild.ID, int(app[2]))
            applicant = interactions.Member(**_applicant)
            applicant_level = database.get_user(int(app[2]))[1]

            modal = component.gen_review_modal(application_id, applicant.user.username, int(applicant_level))
            await ctx.popup(modal)

    @interactions.extension_listener()
    async def on_modal(self, ctx: interactions.CommandContext):
        name, entries = component.decode_custom_id(ctx.data.custom_id)
        if name == 'applications-review-modal':
            
            # info
            application_id = entries['application_id']
            new_level, thoughts, pros, procons, cons = [value['components'][0]['value'] for value in ctx.data.components]

            # get database entries for
            if not isinstance(application := database.get_application(int(application_id)), (tuple, list)):
                await ctx.send(
                    embeds=create_error_embed('It appears there was a problem getting the application from the database.'), 
                    ephemeral=True
                )
                return
            if not isinstance(applicant := database.get_user(int(application[2])), (tuple, list)):
                await ctx.send(
                    embeds=create_error_embed('It appears there was a problem getting the applicant from the database.'), 
                    ephemeral=True
                )
                return
            
            # get applicant user object
            try:
                applicant_discord = interactions.User(**await self.client._http.get_user(int(applicant[0])))
            except:
                await ctx.send(
                    embeds=create_error_embed("That user doesn't exist."), 
                    ephemeral=True
                )
                return

            # check for illegal level name
            name2level = {
                'reapp': 0,
                'trial': 1,
                'member': 2,
                'member+': 3
            }
            if not (new_level := name2level.get(new_level.lower())):
                await ctx.send(
                    embeds=create_error_embed("Invalid rank (check your spelling)"), 
                    ephemeral=True
                )
                return
            
            # check for illegal assigning and adjust for reapp
            old_level = int(applicant[1])
            if old_level > 0 and new_level == 0:
                new_level = old_level
            if old_level > new_level:
                await ctx.send(
                    embeds=create_error_embed("You can't give a user a rank lower than what they had before!"), 
                    ephemeral=True
                )
                return

            # give role
            if new_level > old_level:
                try:
                    await self.client._http.add_member_role(config.Guild.ID, int(applicant_discord.id), config.Role.LEVELS[new_level])
                except:
                    channel = await ctx.get_channel()
                    await channel.send(embeds=create_error_embed('It seems that the applicant has left the server or is unable to be given the role. Continuing...'))
            
            # update database
            if database.modify_application(int(application_id), database.ApplicationTrait.STATUS, new_level):
                await ctx.send(
                    embeds=create_error_embed('It appears there was a problem updating the application in the database. Alert authorities immediatly.'), 
                    ephemeral=True
                )
                return
            if database.modify_user(int(applicant_discord.id), database.UserTrait.EDITOR_LEVEL, new_level):
                await ctx.send(
                    embeds=create_error_embed('It appears there was a problem updating the user in the database. Alert authorities immediatly.'), 
                    ephemeral=True
                )
                return

            # confirm review
            await ctx.send(embeds=create_info_embed('The review was successful'))

            # send review
            embeds = create_review_embeds(
                url=application[3],
                old_level=old_level,
                new_level=new_level,
                applicant_name=applicant_discord.username,
                reviewer_name = ctx.author.user.username,
                thoughts=thoughts,
                pros=pros.split(', '),
                procons=procons.split(', '),
                cons = cons.split(', ')
            )
            channel = interactions.Channel(**await self.client._http.get_channel(config.Channel.REVIEWS))
            channel._client = self.client._http
            await channel.send(
                embeds=embeds
            )
            

def setup(client: interactions.Client):
    Applications(client)