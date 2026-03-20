import subprocess

schema =   {
        "type":"function",
        "function": {
            "name":"open_app",
            "description": "to open a app ",
            "parameters":{

                "type":"object",
                "properties":{
                    "app_name":{            #properties of the app name
                        "type":"string",        #type in which the name of app recieved
                        "description":"name of the app which is to be open"     #description of the app name
                    },
                    "args":{
                        "type":"string",
                        "description":"arguments with which app will open , e.g. - https://youtube.com",

                    },
                }
            },
            "required": ["app_name"], 
        }
    }

def func(app_name, args=''):
    app_name = app_name.lower()
    subprocess.Popen([app_name,args])
    return f"Opened {app_name}with args {args}"
