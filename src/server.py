# imports - server.py, by Mc_Snurtle, based on the magic of Soko010 on GitHub
import socket
import threading
from threading import Thread
from typing import Any

import pyaudio
import queue

from utils import audio, config_reader


# ========== Constants ==========
RUNNING: bool = True
CONFIG: dict[str, Any] = config_reader.Config("server")
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

        self.clients: list[str] = []
        self.threads: list[Thread] = []
        self.buffer = queue.Queue()
        self.playback_thread = audio.play_stream(self.buffer)
        self.threads.append(self.playback_thread)

        # self.next_id: int = 0

    def receive_audio(self):
        """Repeatedly call this to accept chunks over the server socket and handle them accordingly."""

        data, address = self.socket.recvfrom(FRAMES_PER_BUFFER * 2 + 2) # Sock010 numbers
        # data, address = self.socket.recvfrom(8192)
        formatted_data = data[2:]

        # queue chunk to be played when possible:
        self.buffer.put(formatted_data)

    def mainloop(self) -> None:
        while RUNNING:
            self.receive_audio()
            # self.broadcast()

    def terminate(self) -> None:
        """Prepare all class variables for safe termination."""

        global RUNNING

        RUNNING = False
        self.socket.close()
        self.buffer.put(None)   # sigterm to playback thread
        self.playback_thread.join() # wait. ***E I G H T***. *** E I G H T ***. *** * * * E I G H T * * * ***.


if __name__ == "__main__":
    connector = Server()
    connector.mainloop()
