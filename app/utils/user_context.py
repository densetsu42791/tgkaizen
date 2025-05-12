from collections import defaultdict


user_context = defaultdict(dict)

def set_state(user_id: int, state: str):
    user_context[user_id]['state'] = state

def get_state(user_id: int) -> str | None:
    return user_context[user_id].get('state')

def clear_state(user_id: int):
    user_context[user_id].pop('state', None)
