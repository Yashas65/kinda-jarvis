import json 
from memory import store , vector

def get_context(user_message:str):       #gets called every prompt
    print('getting from memory.....')
    mem = store.load()
    
    # build from json
    user = mem["user"]
    facts_str = "\n".join(f"- {f['key']}: {f['value']}" for f in user["facts"])
    traits_str = "\n".join(f"- {t}" for t in user['traits'])

    goals = mem['goals']
    goals_str = "\n".join(
        f"- [{g['status']}] {g['title']}: {g['description']}"
        for g in goals
    ) if goals else "none"


    # fetch relevant summaries from DB
    collection = mem["summaries_index"]["collection"]
    summaries = vector.query_summaries(collection, user_message, n_results=3)
    summaries_str = "\n".join(f"- {s}" for s in summaries) if summaries else "none"
    
    # final str to be injected in the prompt
    context = f"""
## About the user
Name: {user['name']}
Traits:
{traits_str}
Facts:
{facts_str}

## Goals
{goals_str}

## Relevant past context
{summaries_str}
""".strip()

    return context



def save_summary(conversation: str):
    mem = store.load()
    collection = mem["summaries_index"]["collection"]
    from datetime import date
    vector.add_summary(collection, conversation, {"date": str(date.today())})