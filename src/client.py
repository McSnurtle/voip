"""Client script to connect to a matching server script running UDP VoIP."""
# imports - client.py, by Mc_Snurtle, based on Soko101's AudioStreamer
import socket
import pyaudio
import time
import threading
import queue

from utils import config_reader, audio, path
from typing import Any

# ========== Constants ==========
RUNNING: bool = True  # program sigterm
CONFIG: dict[str, Any] = config_reader.Config("client")
FORMAT: int = pyaudio.paInt16
CHANNELS: int = 1  # mono, all that works D:
RATE: int = CONFIG["audio"]["sample_rate"]  # 44100 Hz, or 16000 Hz
CHUNK_SIZE: int = CONFIG["audio"]["chunk_size"]  # 10 ms somehow?
FRAMES_PER_BUFFER: int = CHUNK_SIZE * CONFIG["audio"][
    "mystery_number"]  # huh? Oh I get now (2 hours later I'm not even kidding)
DEVICE_ID: int = CONFIG["audio"]["microphone_id"]


# ========== Classes ==========
class Client:
    def __init__(self, destination: tuple[str, int]):
        """To communicate with an audio server.

        Params:
            :param destination (tuple[str, int]): the IPv4 + port pair to connect with."""

        # playback
        self.playback_buffer: queue.Queue = queue.Queue()
        self.playback_thread = audio.play_stream(self.playback_buffer)

        # networking
        self.destination: tuple[str, int] = destination
        print("attempting to connect to: " + str(destination))
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_audio(self, data: bytes):
        self.socket.sendto(
            audio.format_audio(data),
            self.destination
        )  # the UDP way

    def listen(self):
        while RUNNING:
            try:
                packet, origin = self.socket.recvfrom(FRAMES_PER_BUFFER * 2 + 2)
                print(f"PLAYBACK DATA CAME FROM {origin}")
                formatted_data = packet[2:]
                self.playback_buffer.put(formatted_data)
            except OSError:
                pass

    def terminate(self) -> None:
        global RUNNING

        RUNNING = False
        self.playback_buffer.shutdown()
        self.socket.close()


class Recorder:
    def __init__(self):
        # recording
        self.device = pyaudio.PyAudio()
        self.buffer: queue.Queue[bytes] = queue.Queue()
        self.stream = self.device.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=FRAMES_PER_BUFFER,
            stream_callback=self.callback
        )

    def callback(self, data: bytes, *args):
        """A callback for PyAudio streams, registers the recorded chunk of audio to the recording buffer"""

        self.buffer.put(data)
        return audio.bogus_data, pyaudio.paContinue

    def terminate(self) -> None:
        """Prepare all class variables for safe termination."""
        self.buffer.task_done()
        self.stream.stop_stream()
        self.stream.close()
        self.device.terminate()

    @property
    def history(self) -> bytes:
        """The entire cannon of what was recorded since the PyAudio stream was initialized"""

        return b"".join(list(self.buffer.queue))


def blocker() -> None:
    time.sleep(3)
    audio.write_data(recorder.history, path.mkpath(path.secrets_dir, "output.wav"))


if __name__ == "__main__":
    target: tuple[str, int] = CONFIG["networking"]["server_ip"], CONFIG["networking"]["server_port"]

    audio.list_microphones(True)

    connector = Client(target)
    recorder = Recorder()

    listener_thread: threading.Thread = threading.Thread(target=connector.listen, daemon=True)
    listener_thread.start()

    while RUNNING:
        connector.send_audio(recorder.buffer.get())
