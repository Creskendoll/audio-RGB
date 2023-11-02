import socket
from json import dumps


class SignalTransmitter(object):
    def __init__(self):
        # UDP broadcast
        server = socket.socket(
            socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # Set a timeout so the socket does not block
        # indefinitely when trying to receive data.
        server.settimeout(0.001)
        server.bind(("", 44444))

        self.server = server

    def send(self, package: dict, client_address: str):
        try:
            msg = dumps(package).encode('utf-8')
            self.server.sendto(msg, (client_address, 37020))
        except:
            print(f"Error sending UDP packet to {client_address}")
