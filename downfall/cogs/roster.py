
import interactions, validators
import config
from downfall.tools.database import DBFail
from tools import database, check
from tools.embed import (
    create_user_info_embed, 
    create_error_embed, 
    create_info_embed
)

class Roster(interactions.Extension):

    @interactions.extension_command(
        name='profile',
        description='The profile command',
        scope=config.Guild.ID,
        options=[
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name='view',
                description='The command to view a profile',
                options=[
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name='user',
                        description='The user to view',
                        required=False
                    )
                ]
            ),
            interactions.Option(
                type=interactions.OptionType.SUB_COMMAND,
                name='edit',
                description='The command to edit a profile',
                options=[
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name='trait',
                        description='What part of your profile do you want to change?',
                        required=True,
                        choices=[
                            interactions.Choice(
                                name='youtube',
                                value='youtube',
                            ),
                            interactions.Choice(
                                name='bio',
                                value='bio'
                            )
                        ]
                    ),
                    interactions.Option(
                        type=interactions.OptionType.STRING,
                        name='value',
                        description='What do you want it to be?',
                        required=True
                    ),
                    interactions.Option(
                        type=interactions.OptionType.USER,
                        name='user',
                        description='The user to edit (mod only)',
                        required=False
                    ),
                ]
            ),
        ]
    )
    async def profile_command(
        self,
        ctx: interactions.CommandContext, 
        sub_command: str = None, 
        user: interactions.Member = None,
        trait: str = None,
        value: str = None
        ):
        if illegal := check.illegal_commmand_channel(ctx.channel_id):
            await ctx.send(embeds=illegal, ephemeral=True)
            return
        match ctx.data.options[0].name:
            case 'view':
                await self._view_profile(ctx, user)
            case 'edit':
                await self._edit_profile(ctx, user, trait, value)

    @interactions.extension_user_command(
        name='info',
        scope=config.Guild.ID
    )
    async def view_profile(
        self, ctx: interactions.CommandContext
        ):
        if illegal := check.illegal_commmand_channel(ctx.channel_id):
            await ctx.send(embeds=illegal, ephemeral=True)
            return
        await self._view_profile(ctx, ctx.target)

    async def _view_profile(
        self, 
        ctx: interactions.CommandContext, 
        user: interactions.Member = None
        ):
        user = user or ctx.author
        user_db = database.get_user(int(ctx.author.id))
        if isinstance(user_db, database.DBFail):
            await ctx.send(embeds=user_db, ephemeral=True)
            return
        embed = create_user_info_embed(user, user_db)
        await ctx.send(embeds=embed)

    async def _edit_profile(
        self,
        ctx: interactions.CommandContext,
        user: interactions.Member = None,
        trait: str = None,
        value: str = None
        ):
        user = user or ctx.author
        if user != ctx.author and config.Role.MOD not in ctx.author.roles:
            await ctx.send(embeds=create_error_embed("You don't have permission to this command on another user!"), ephemeral=True)
            return

        if trait == 'bio' and len(value) > 100:
            await ctx.send(embeds=create_error_embed('Your bio can only be 100 characters long'), ephemeral=True)
            return

        if trait == 'youtube' and not validators.url(value):
            await ctx.send(embeds=create_error_embed('You need to use a valid link for this.'), ephemeral=True)
            return

        if isinstance((user_db := database.get_user(user.id)), DBFail):
            await ctx.send(embeds=user_db, ephemeral=True)
            return

        if error := database.modify_user(int(user.id), trait, value):
            await ctx.send(embeds=error, ephemeral=True)
            return

        await ctx.send(
            embeds=create_info_embed(
                f'Successfully edited profile the of {user.user.username}',
                items={
                    'Trait': trait,
                    'Value': value
                }
            )
        )

    async def _update_roster(self):
        


def setup(client):
    Roster(client)