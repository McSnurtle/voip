# imports - audio.py, by Mc_Snurtle
import threading
import queue
import wave
from typing import Any

import pyaudio

from utils import config_reader

# ========== Variables ==========
config: dict[str, Any] = config_reader.Config("client")
frames_per_buffer: int = config["audio"]["chunk_size"] * config["audio"]["mystery_number"]
interface = pyaudio.PyAudio()
silence_value: int = 0
bogus_data: bytes = silence_value.to_bytes(2, byteorder="little") * config["audio"]["chunk_size"]


# ========== Functions ==========
def format_audio(data: bytes) -> bytes:
    """Returns a magically formatted bytes object based on `data` ready to ship in UDP with PyAudio.

    Params:
        :param data: (bytes) pyaudio captured microphone data.

    Returns:
        :returns: (bytes) magically formatted for sending by Soko101 magic."""
    _: int = 0
    format_bytes = _.to_bytes(2, byteorder="little", signed=False)
    return data + format_bytes


def write_data(data: bytes, path: str) -> None:
    """Saves the `data` as a wavefile at specified `path`.

    Params:
        :param data: (bytes) the audio data to parse and write.
        :param path: (str) the path-like string to save to (overwrites, creates if doesn't exist)."""

    with wave.open(path, "wb") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(interface.get_sample_size(pyaudio.paInt16))
        wav_file.setframerate(config["audio"]["sample_rate"])
        wav_file.writeframes(data)


def play_stream(stream: queue.Queue) -> threading.Thread:
    """Asynchronously plays chunks from a `queue.Queue` of `bytes`.

    Params:
        :param stream: (queue.Queue) the queue to read and play audio data from.
    Returns:
        :returns: (threading.Thread) the thread of the asynchronous playback."""

    playback_stream = interface.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=config["audio"]["sample_rate"],
        output=True,
        frames_per_buffer=frames_per_buffer,
        output_device_index=config["audio"]["speaker_id"]
    )

    def _play():
        while True:
            data = stream.get()
            if data is None:
                break
            playback_stream.write(data)
        playback_stream.stop_stream()
        playback_stream.close()

    thread = threading.Thread(target=_play, daemon=True)
    thread.start()
    return thread


def list_microphones(verbose: bool = True) -> dict[int, str]:
    """Collects all recording devices connected to the host system.

    Params:
        :param verbose: (bool) whether to print the results to the console.
    Returns:
        :return: (dict[int, str]) a dictionary of PyAudio device id to device name."""

    devices: dict[int, str] = {}
    for device_index in range(interface.get_device_count()):
        device_info = interface.get_device_info_by_index(device_index)
        if int(device_info["maxInputChannels"]) > 0:
            devices[device_index] = str(device_info)

    if verbose:
        print("Available recording devices:\n\n")
        for idx, value in devices.items():
            print(f"{idx}: {value}\n")

    return devices


def list_speakers(verbose: bool = True) -> dict[int, str]:
    """Collects all playback devices connected to the host system.

    Params:
        :param verbose: (bool) whether to print the results to the console.
    Returns:
        :return: (dict[int, str]) a dictionary of PyAudio device id to device name."""

    devices: dict[int, str] = {}
    for device_index in range(interface.get_device_count()):
        device_info = interface.get_device_info_by_index(device_index)
        if int(device_info["maxInputChannels"]) == 0:
            devices[device_index] = str(device_info)

    if verbose:
        print("Available playback devices:\n\n")
        for idx, value in devices.items():
            print(f"{idx}: {value}\n")

    return devices
