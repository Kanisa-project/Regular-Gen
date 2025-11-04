import socket
import threading

from src.widgets.texioty import texoty, texity
from src.widgets.texioty.helpers.tex_helper import TexiotyHelper
from src.settings import themery as t


class PijunCoop(TexiotyHelper):
    def __init__(self, txo: texoty.TEXOTY, txi: texity.TEXITY, host='127.0.0.1', port=8008):
        super().__init__(txo, txi)
        self.buff_size = 1024
        self.pijun_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.coop_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

        self.coop_address = ("74.1.241.0", 8080)
        self.pijun_address = ("4.20.60.0", 8080)
        self.pijuns = {}
        self.pijun_addresses = {}
        self.helper_commands['pijun'] = [self.connect_pijun, "Setup a pijun to send.",
                                         {}, "PIJN", t.rgb_to_hex(t.PIGEON_GREY), t.rgb_to_hex(t.BLACK)]
        self.helper_commands['coop'] = [self.host_dovecot, "Define a pijun coop.",
                                         {}, "PIJN", t.rgb_to_hex(t.PIGEON_GREY), t.rgb_to_hex(t.BLACK)]

    def handle_pijun(self, pijun):
        while True:
            name = pijun.recv(self.buff_size).decode("utf-8")
            self.txo.priont_string(f"connection from {name}")
            pijun.send(bytes("Welcome to the pijun coop.", "utf-8"))
            self.pijuns[pijun] = name

    def host_dovecot(self, host: str, port: str):
        try:
            port = int(port)
        except ValueError:
            port = 8008
        address = (host, port)
        print(f"trying to bind to {address}")
        self.coop_socket.bind(address)
        self.txo.priont_string(f"coop socket bound to {address}")
        coop_thread = threading.Thread(target=self.coop_receive_data)
        coop_thread.start()
        self.txo.priont_string("coop_thread_started")

    def connect_pijun(self, host: str, port: str):
        try:
            port = int(port)
        except ValueError:
            port = 8008
        address = (host, port)
        self.pijun_socket.sendto(bytes("Hello, I am a pijun.", "utf-8"), address)

    def coop_receive_data(self):
        while True:
            data, addr = self.coop_socket.recvfrom(self.buff_size)
            if not data:
                break
            self.txo.priont_string(data.decode())
            print(data.decode())
