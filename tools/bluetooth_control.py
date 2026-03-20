#   SINCE this file has multiple functions they are exported in a dict present
#       the most bottom of this file
# 
# 
# 

import subprocess

schema = [
    {
        "type":"function",
        "function":{
            "name":"bluetooth_scan",
            "description":"to scan bluetooth nearby devices",
            "parameters":{
                "type":"object",
                "properties":{},
                "required":[],
            },
        },
    },
    {
        "type":"function",
        "function": {
            "name":"bluetooth_list",
            "description":"list paired bluetooth devices",
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
            "name":"bluetooth_connect",
            "description":"connect to a bluetooth device",
            "parameters":{
                "type":"object",
                "properties":{
                    "device_name":{
                        "type":"string",
                        "description":"name of the bluetooth device to be connected",
                    }
                },
                "required":["device_name"]
            }
        }
    },
    {
        "type":"function",
        "function":{
            "name":"bluetooth_disconnect",
            "description":"disconnecct from a bluetooth device",
            "parameters":{
                "type":"object",
                "properties":{
                    "device_name":{
                        "type":"string",
                        "description":"name of the bluetooth device to be disconnected",
                    }
                },
                "required":[]
            }
        }
    }
    
]
def get_mac_by_name(name: str) -> str:
    # Check paired devices first
    result = subprocess.run(["bluetoothctl", "devices"],
                            capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if name.lower() in line.lower():
            parts = line.split()
            return parts[1]

    # ✅ Also check recently scanned devices
    result = subprocess.run(["bluetoothctl", "devices", "Paired"], capture_output=True, text=True)
    for line in result.stdout.splitlines():
        if name.lower() in line.lower():
            parts = line.split()
            return parts[1]

    return ""

def scan():
    result = subprocess.run(
            ["bluetoothctl", "--timeout", "8", "scan", "on"],
            capture_output=True, text=True, timeout=15
        )
    return result.stdout or "no one discorvered check if the bluetooth is on"

def list_devices():
    result = subprocess.run(
            ["bluetoothctl", "devices"],
            capture_output=True, text=True
        )
    return result.stdout or "No devices found."

def connect(device_name):
    result = subprocess.run(
            ["bluetoothctl", "connect", get_mac_by_name(device_name)],
            capture_output=True, text=True, timeout=15
        )
    if "Connection successful" in result.stdout:
        return f"Connected to {device_name}"
    return f" {result.stdout.strip()}"


def disconnect(device_name=""):
    if not device_name:
        # get all connected devices and disconnect each
        result = subprocess.run(["bluetoothctl", "devices", "Connected"],
                                capture_output=True, text=True)
        for line in result.stdout.splitlines():
            parts = line.split()
            if len(parts) >= 2:
                mac = parts[1]
                subprocess.run(["bluetoothctl", "disconnect", mac],
                               capture_output=True, text=True, timeout=15)
        return "Disconnected from all devices"
    
    result = subprocess.run(
        ["bluetoothctl", "disconnect", get_mac_by_name(device_name)],
        capture_output=True, text=True, timeout=15
    )
    return f"Disconnected from {device_name}"

#to be written from init file's prespective
func = {
    "bluetooth_scan"            :       scan,
    "bluetooth_list"     :       list_devices,
    "bluetooth_connect"         :       connect,
    "bluetooth_disconnect"      :       disconnect,
}