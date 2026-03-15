import ollama
import subprocess
from tts.tts import speak
from tools import TOOL_SCHEMA, TOOL_FUNC

SYSTEM = {"role": "system", "content": "you are a desktop assistant , your personality traits are - sarcastics , humourous, frank , straightforword"}
MODEL = "qwen3.5:9b-q4_K_M"

#func that runs the model
def run(user_input, history):
    history.append({"role": "user", "content": user_input})

    while True:
        response = ollama.chat(
            model = MODEL,
            messages=[SYSTEM]+history,  # this contains current prompt with the previous ones
            tools=TOOL_SCHEMA,   # defined above 
            options={
                "think": False,
                "mmap": True, 
                "mlock": True,
                },
        )
        message = response["message"]

        if  not message.get("tool_calls"):
            history.append({"role":"assistant","content": message["content"]})
            return message["content"], history

        
        history.append(message) 

        for tool_call in message["tool_calls"]:
            name = tool_call["function"]["name"]
            args = tool_call["function"]["arguments"]
            func   = TOOL_FUNC[name]
            result = func(**args)

            history.append({"role": "tool", "content": result})


def main ():
    history = []

    while True:
        user_input = input("You: ")
        reply, history = run(user_input, history)
        speak(reply)
        print(f"Assistant: {reply}")


if __name__ == "__main__":
    main()