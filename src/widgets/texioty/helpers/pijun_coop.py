import socket
import threading

from src.widgets.texioty import texoty, texity
from src.widgets.texioty.helpers.tex_helper import TexiotyHelper
from src.settings import themery as t


class PijunCoop(TexiotyHelper):
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY, host='127.0.0.1', port=8008):
        super().__init__(txo, txi)
        self.pijun_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.coop_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.pijun_address = None
        self.helper_commands['pijun'] = [self.connect_pijun, "Setup a pijun to send.",
                                         {}, "PIJN", t.rgb_to_hex(t.PIGEON_GREY), t.rgb_to_hex(t.BLACK)]
        self.helper_commands['coop'] = [self.host_dovecot, "Define a pijun coop.",
                                         {}, "PIJN", t.rgb_to_hex(t.PIGEON_GREY), t.rgb_to_hex(t.BLACK)]

        # threading.Thread(target=self.receive_data, args=()).start()
        # threading.Thread(target=self.send_data, args=()).start()

    def accept_connection(self):
        self.pijun_socket, self.pijun_address = self.pijun_socket.accept()
        self.txo.priont_string(f"connection from {self.pijun_address}")
        self.pijun_socket.sendall(b'Welcome to the pijun.')

    def handle_pijun_socket(self, pijun):
        name = pijun.recv(1024).decode()
        self.txo.priont_string(f"connection from {name}")
        pijun.sendall(b'Welcome to the pijun.')
        threading.Thread(target=self.receive_data, args=(pijun,)).start()
        threading.Thread(target=self.send_data, args=(pijun,)).start()

    def host_dovecot(self, host: str, port: str):
        try:
            port = int(port)
        except ValueError:
            port = 8008
        address = (host, port)
        self.coop_socket.bind(address)
        self.txo.priont_string(f"coop socket bound to {address}")
        self.coop_socket.listen()
        threading.Thread(target=self.accept_connection()).start()
        self.txo.priont_string("waiting for connection...")

    def connect_pijun(self, host: str, port: str):
        try:
            port = int(port)
        except ValueError:
            port = 8008
        address = (host, port)
        self.pijun_socket.connect(address)
        self.txo.priont_string(f"connected to {address}")
        threading.Thread(target=self.handle_pijun_socket, args=(self.pijun_socket,)).start()
        self.txo.priont_string("thread_started")

    def receive_data(self):
        while True:
            data = self.client_socket.recv(1024)
            if not data:
                break
            self.txo.priont_string(data.decode())
            print(data.decode())

    def send_data(self):
        while True:
            message = str(input("What to reply with? _"))
            self.client_socket.sendall(message.encode())

