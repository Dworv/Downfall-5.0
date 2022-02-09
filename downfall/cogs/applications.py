
import interactions 

import config
from tools.embed import create_info_embed, create_error_embed


class Applications(interactions.Extension):

    def __init__(self, client: interactions.Client):
        self.client: interactions.Client = client
    
    

def setup(client: interactions.Client):
    Applications(client)