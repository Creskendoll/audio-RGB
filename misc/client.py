import socket
import json
import time
from gpiozero import RGBLED, LED

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 37020))
led = RGBLED(16, 20, 21, active_high=True, pwm=True)

BOI_PIN = LED(14)

print("Client started")
prev_data = None
while True:
    data, addr = client.recvfrom(1024)
    data = json.loads(data.decode('utf-8'))
    # led.color = (1,1,0)
    if prev_data is None or prev_data != data:
        led.color = (data['red']/255, data['green']/255, data['blue']/255)
        if data["boi"] == str(True):
            BOI_PIN.on()
        else:
            BOI_PIN.off()
        # print(data)
        prev_data = data
    #server_time = float(data['time'])
    #print("Latency:", time.time() - server_time)
