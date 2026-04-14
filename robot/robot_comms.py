#// this is used for UART communication with the ESP 32 chip , and later i can also move to a websocket
#but since this is easier for now , i'll just communicate like this for  now and later try switching to 
#a websocket

import serial 
import threading
class UART :
    def __init__(self, port="/dev/ttyUSB0", baud=115200):
        self.ser = serial.Serial(port, baud, timeout=1)

    def send(self, command: str):
        self.ser.write((command + "\n").encode())

    def listen(self, callback):
        def _read():
            while True:
                line = self.ser.readline().decode(errors="ignore").strip()
                if line:
                    callback(line)
        threading.Thread(target=_read, daemon=True).start()


# Usage
link = UART()
link.listen(lambda msg: print(f"Robot: {msg}"))
link.send("HELLO")

if __name__ == "__main__":
    try:
        while True:
            import time
            time.sleep(1) 
    except KeyboardInterrupt:
        print("\nClosing connection...")

""" 
    the format for commands to control servos is somthing like 

    it sends mood and the esp32 just perform math and move servos
    even tho the model just has to send moods raw servo angle access is available 
    to the python side too for debugging

    multiple commands are seperated by ";" and keywords and values are seperated by ":"and 
    sub-values are seperated my "-"

    here's the example
    ges:lkdn:20;           -->> gesture:look_down:20; means gesture lookdown by how much (the value will be subracted from the servo angle)
    agl:nklf:90;         -->> angle:neckleft:90; means set neck servo to 90 degrees means look straight
    pos:lkst        -->> pose:look straight
"""