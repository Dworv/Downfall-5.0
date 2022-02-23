
def custom_to_dict(custom_id) -> dict:
    split: list = custom_id.split('?')
    entry_count = len(split) - 1
    if not entry_count:
        return {'base': custom_id}
    entries = {'base': split.pop(0)}
    for entry in split:
        name, value = entry.split('=')
        entries[name] = value
    return entries