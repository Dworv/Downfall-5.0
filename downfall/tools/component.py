
def decode_custom_id(custom_id: int) -> tuple:
    split: list = custom_id.split('?')

    entry_count = len(split) - 1
    if not entry_count:
        return {'base': custom_id}
    base = split.pop(0)
    entries = {}
    for entry in split:
        name, value = entry.split('=')
        entries[name] = value
    return base, entries

def encode_custom_id(base, entries: dict) -> str:
    custom = base
    entry_list = [f'?{name}={value}' for name, value in entries.items()]
    for entry in entry_list: custom += entry
    return custom