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
try:
    while True:
        import time
        time.sleep(1) 
except KeyboardInterrupt:
    print("\nClosing connection...")