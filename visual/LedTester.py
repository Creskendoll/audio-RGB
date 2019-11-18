########## LIBRARIES ###########################################################

import json
import socket
from tkinter import *
from threading import Thread


########## SETTINGS ##############################################

########## APPLICATION SETTINGS ################################################

CLIENT = '192.168.0.70' # UDP Client

########## CODE ################################################################

# UDP broadcast
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
server.bind(("", 44444))

########## server ###################################################

def sendData(red_scale,green_scale,blue_scale):
  prev_color = {
      "red": red_scale.get(),
      "green": green_scale.get(),
      "blue": blue_scale.get()
    }
  while True:
    colors = {
      "red": red_scale.get(),
      "green": green_scale.get(),
      "blue": blue_scale.get()
    }
    if prev_color != colors:
      # print(colors)
      prev_color = colors
      msg = json.dumps(colors).encode('utf-8')
      server.sendto(msg, (CLIENT, 37020))

master = Tk()
########## GUI ###################################################
label = Label(master, text="RED")
red_scale = Scale(master, from_=0, to=255, orient=HORIZONTAL, length=500)
label.pack()
red_scale.pack()

label = Label(master, text="GREEN")
green_scale = Scale(master, from_=0, to=255, orient=HORIZONTAL, length=500)
label.pack()
green_scale.pack()

label = Label(master, text="BLUE")
blue_scale = Scale(master, from_=0, to=255, orient=HORIZONTAL, length=500)
label.pack()
blue_scale.pack()

thread = Thread(target=sendData, args=(red_scale, green_scale, blue_scale))
thread.start()

########## VISUALIZATION LOOP ##################################################
mainloop()
