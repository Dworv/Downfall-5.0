
import interactions

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

def gen_review_modal(application_id, applicant_name, applicant_level):
    levels = ['No Level', 'Trial', 'Member', 'Member+']
    return interactions.Modal(
        custom_id = encode_custom_id('applications-review-modal', {'application_id': application_id}),
        title = f'Review of {applicant_name}',
        components = [
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                label=f'Grade (currently {levels[int(applicant_level)]})', 
                custom_id='grade',
                placeholder='eg: "Trial", "Reapp" (no quotes)',
                required=True
            ),
            interactions.TextInput(
                style=interactions.TextStyleType.PARAGRAPH,
                label='Thoughts', 
                custom_id='thoughts',
                placeholder='Remember to start with something positive!',
                min_length=75,
                max_length=1500,
                required=True
            ),
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                label='Pros', 
                custom_id='pros',
                placeholder='Seperate with commas (", "), keep short.',
                min_length=1,
                max_length=100,
                required=True
            ),
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                label='ProCons', 
                custom_id='procons',
                placeholder='Seperate with commas (", "), keep short.',
                min_length=1,
                max_length=100,
                required=True
            ),
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                label='Cons', 
                custom_id='cons',
                placeholder='Seperate with commas (", "), keep short.',
                min_length=1,
                max_length=100,
                required=True
            ),
        ]
    )