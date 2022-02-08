
import interactions, config

class Utils(interactions.Extension):

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
    
    @interactions.extension_command(name="ping", description="Pings the bot", scope=[config.Guild.ID])
    async def ping(self, ctx: interactions.CommandContext):
        await ctx.send("Pong!")

def setup(client: interactions.Client):
    Utils(client)