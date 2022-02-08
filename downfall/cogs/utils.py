
import interactions, config

class Utils(interactions.Extension):

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
    
    @interactions.extension_command(name="ping", description="Pings the bot", scope=[896513855763652669])
    async def ping(self, ctx: interactions.CommandContext):
        await ctx.send("Pong!")

def setup(client: interactions.Client):
    Utils(client)