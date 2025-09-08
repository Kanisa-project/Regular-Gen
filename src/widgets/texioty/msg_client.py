import socket
import threading

from src.widgets.texioty import texioty


class MsgClient:
    def __init__(self, txty, host='0.0.0.0', port=5748):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print(host, port)
        self.client_socket.connect((host, port))
        self.server_socket = None
        self.server_address = None
        self.TXTY: texioty.TEXIOTY = txty

        threading.Thread(target=self.receive_data, args=()).start()
        threading.Thread(target=self.send_data, args=()).start()

    def receive_data(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            self.TXTY.texoty.priont_string(data.decode())
            print(data.decode())

    def send_data(self):
        while True:
            message = str(input("What to reply with? _"))
            self.client_socket.sendall(message.encode())


