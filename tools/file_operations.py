import os 

schema = [
    {
        "type":"function",
        "function":{
            "name" : "read_file",
            "description":"to read the contents of a file",
            "parameters":{
                "type":"object",
                "properties":{
                    "path":{
                        "type":"string",
                        "descriptioni": "absolute or relative path to file",
                    },
                },
                "required":["path"],
            }

        }
    },
    {   
        "type":"function",
        "function":{
            "name": "write_file",
            "description":"to write or overwrite a file, or to create a file if it doesn't exist, but first check if the file exists if it exists then ask user permission to overwrite, if the response to a question or task is too long use this and tell user that it's writen the file",
            "parameters":{
                "type":"object",
                "properties":{
                    "path":{
                        "type":"string",
                        "description":"absolute or relative path where the file is to be written",
                    },
                    "content":{
                        "type":"string",
                        "description": " the overall file content of a the file"
                    }
                },
                "required":["path","content"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"list_directory",
            "description":"used to list files and folders in a directory , you can use this to nevigate throught the file system",
            "parameters":{
                "type":"object",
                "properties":{
                    "path":{
                        "type":"string",
                        "description":"path of the directory of which contents are to be listed, default is . meaning current working directory",
                        "default":".",
                    }
                },
                "required":[],
            }
        }
    },
]


def read_file(path:str):
    try:
        path = os.path.expanduser(path)
        with open (path,"r",encoding="utf-8") as f:
            content = f.read()
        return content if content else "file is empty"
    except FileNotFoundError:
        return f"file not found {path}"
    except PermissionError:
        return f"you cannot read {path}"
    except Exception as e :
        return f"something's not write {e}"

def write_file(path:str, content:str):
    try:
        path = os.path.expanduser(path)
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote {len(content)} characters to {path}"
    except PermissionError:
        return f"Error: Permission denied — {path}"
    except Exception as e:
        return f"Error writing file: {e}"

def list_directory(path: str = ".") -> str:
    try:
        path = os.path.expanduser(path)
        entries = os.listdir(path)
        if not entries:
            return f"(directory is empty: {path})"
        lines = []
        for name in sorted(entries):
            full = os.path.join(path, name)
            tag = "/" if os.path.isdir(full) else ""
            lines.append(f"  {name}{tag}")
        return f"Contents of {path}:\n" + "\n".join(lines)
    except FileNotFoundError:
        return f"Error: Directory not found — {path}"
    except PermissionError:
        return f"Error: Permission denied — {path}"
    except Exception as e:
        return f"Error listing directory: {e}"
 

func = {
    "read_file":read_file,
    "write_file":write_file,
    "list_directory":list_directory,

}