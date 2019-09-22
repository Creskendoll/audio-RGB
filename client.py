import socket
import json
from gpiozero import RGBLED

# UDP receiver
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # UDP
client.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
client.bind(("", 37020))    

# RGB led
led = RGBLED(16, 20, 21, active_high=False, pwm=True)

while True:
    data, addr = client.recvfrom(1024)
    data = json.loads(data.decode('utf-8'))
    
    led.color = (data['red']/255, data['green']/255, data['blue']/255)
    print(data)