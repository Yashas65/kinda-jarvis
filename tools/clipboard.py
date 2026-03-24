import pyperclip

schema = [
    {
        "type":"function",
        "function":{
            "name":"read_clipboard",
            "description":'to get to know what is in the clipboard use this as a refference for context for what user is talking about',
            "parameters":{
                "type":"object",
                "properties":{},
                "required":[],
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"write_clipboard",
            "description":"to write something in the clipboard, to help user ease with typing stuff , so the user don't have to copy paste",
            "parameters":{
                "type":"object",
                "properties":{
                    "txt":{
                        "type":"string",
                        "description":"the text which is to be copies into clipboard",
                    },
                },
            },
            "required":["txt"]
        }
    }
]
def _set_clipboard():
    pyperclip.set_clipboard('wl-clipboard')         # for hyprland/wayland setup

def read_clipboard():
    _set_clipboard()
    return pyperclip.paste()
    print("checked clipboard....")      #trust issues
def write_clipboard(txt:str):
    _set_clipboard()
    pyperclip.copy(txt)
    print("thing added to clipboard", txt)              #trust isssues
    return "i've added the text to your clipboard"  # this is the response from the llm

func = {
    "read":read_clipboard,
    "write":write_clipboard,
}