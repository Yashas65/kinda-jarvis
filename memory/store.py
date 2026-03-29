import json 
from pathlib import Path
from datetime import datetime

MEMORY_PATH = Path(__file__).parent/"memory.json"

def load() -> dict:
    with open(MEMORY_PATH,"r") as file:
        return json.load(file)

def save(data:  dict):
    data["last_updated"] = datetime.now().isoformat()
    with open(MEMORY_PATH,"w") as file:
        json.dump(data, file ,indent=2)

def add_fact(key:str , value:str):
    data = load()
    facts = data["user"]["facts"]
    for fact in facts:
        if fact["key"] == key:
            fact['value'] = value
            save(data)
            print("saved to memory")
    
    facts.append(
        {
            "key": key,
            "value":value,
            "added": datetime.now().date().isoformat()
        }
    )
    save(data)

def add_goal(id:str , title:str, description:str):
    data = load()
    data['goals'].append(
        {
            "id" : id,
            "title" : title,
            "description": description,
            "status": "active",
            "created":datetime.now().date().isoformat,
            "milestone":[]

        }
    )
    save(data)



