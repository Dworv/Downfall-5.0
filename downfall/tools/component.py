
from logging.config import stopListening


def cid_to_dict(custom_id) -> dict:
    split = custom_id.split('?')
    if len(split) == 1:
        return {'base': custom_id}
    for 

print(cid_to_dict('my man'))
print(cid_to_dict('my man?bruh=hello'))