import numpy as np
import cv2
import socket
import json
from PIL import Image
from mss import mss

CLIENT = '192.168.1.69'  # UDP Client

# UDP broadcast
server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
# Set a timeout so the socket does not block
# indefinitely when trying to receive data.
server.settimeout(0.2)
server.bind(("", 44444))


def getAverageColor(img):
    return [img[:, :, i].mean() for i in range(img.shape[-1])]


region = {'top': 0, 'left': 1920, 'width': 1920, 'height': 1080}

with mss() as sct:
    while True:

        # Alternative
        frame = np.array(sct.grab(region))

        # cv2.imshow("screenshot", frame)
        # if cv2.waitKey(1) == ord("q"):
        #     break

        # Get dominant color
        # img = Image.fromarray(frame)
        # colors = img.getcolors(1920*1080)
        # dominant = max(colors, key=lambda px: px[0])
        # avg_color = dominant[1]

        avg_color = getAverageColor(frame)

        colors = {
            "time": 0,
            "boi": str(True),
            "red": avg_color[2],
            "green": avg_color[1],
            "blue": avg_color[0]
        }
        msg = json.dumps(colors).encode('utf-8')
        server.sendto(msg, (CLIENT, 37020))

    cv2.destroyAllWindows()
