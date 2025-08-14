# imports - server.py, by Mc_Snurtle, based on the magic of Soko010 on GitHub
import socket
# import threading
from threading import Thread

import pyaudio
import queue

from utils import audio, config_reader

# ========== Constants ==========
RUNNING: bool = True
CONFIG: config_reader.Config = config_reader.Config("server")
FORMAT: int = pyaudio.paInt16
CHANNELS: int = 1
RATE: int = CONFIG["audio"]["sample_rate"]
CHUNK_SIZE: int = CONFIG["audio"]["chunk_size"]
FRAMES_PER_BUFFER: int = CHUNK_SIZE * CONFIG["audio"]["mystery_number"]
HOST: tuple[str, int] = (CONFIG["networking"]["server_ip"], CONFIG["networking"]["server_port"])


class Server:
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(HOST)
        print(f"Server bound and listening on {HOST}")

        self.clients: dict[str, int] = {}    # e.x. "192.168.0.182"
        self.denied: list[str] = [] # to keep track of who has *already* been denied access to prevent log spam.
        self.threads: list[Thread] = []
        self.buffer = queue.Queue()
        if CONFIG["audio"]["hear_audio"] and not CONFIG["networking"]["relay_audio"]:
            self.playback_thread = audio.play_stream(self.buffer)
            self.threads.append(self.playback_thread)

        # self.next_id: int = 0

    def receive_audio(self):
        """Repeatedly call this to accept chunks over the server socket and handle them accordingly."""

        data, client = self.socket.recvfrom(FRAMES_PER_BUFFER * 2 + 2)  # Sock010 numbers
        formatted_data = data[2:]

        if self._register_client(client):
            self._broadcast_data(formatted_data, client)

    def _broadcast_data(self, data: bytes, sender: tuple[str, int]) -> None:
        # queue chunk to be played when possible:
        self.buffer.put(data)

        for addr, port in list(self.clients.items()):
            if addr != sender[0]:
                self.socket.sendto(data, (addr, port))

    def _register_client(self, client: tuple[str, int]) -> bool:
        """Attempts to register the client to accept its transmissions and send future ones to them.

        Params:
            :param client: (tuple[str, int]) the IPv4 / port pair identifying the client to register.

        Returns:
            :returns bool: whether the registration was successful. Returns false if `enforce_whitelist` is `true` and the address is not whitelisted."""

        addr, port = client
        if CONFIG["networking"]["enforce_whitelist"] and addr not in CONFIG.whitelist:
            if addr not in self.denied: # inversion could make this better!
                print(f"Connection attempt was made from {addr, port} but they are not on the whitelist so they were denied. Future attempts from this client will not be logged here.")
                self.denied.append(addr)
            return False

        elif addr not in list(self.clients.keys()):
            print(f"Accepting client {addr, port}! They will receive all future transmissions.")
            self.clients[addr] = port
            return True
        elif addr in list(self.clients.keys()):
            if self.clients[addr] != port:
                print(f"A connection was temporarily interrupted from {addr} and the port was switched from {self.clients[addr]} to {port}.")
                self.clients[addr] = port
        # if addr already connected:
        return True

    def mainloop(self) -> None:
        while RUNNING:
            self.receive_audio()
            # self.broadcast()

    def terminate(self) -> None:
        """Prepare all class variables for safe termination."""

        global RUNNING

        RUNNING = False
        self.socket.close()
        self.buffer.put(None)  # sigterm to playback thread
        self.playback_thread.join()  # wait. ***E I G H T***. *** E I G H T ***. *** * * * E I G H T * * * ***.


if __name__ == "__main__":
    print(f"`hear_audio` will playback on `speaker_id`: {CONFIG['audio']['speaker_id']}")
    if CONFIG["networking"]["enforce_whitelist"]:
        print(f"Using whitelist: {CONFIG.whitelist}")

    connector = Server()
    connector.mainloop()
