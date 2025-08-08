# imports
from typing import Any

import webrtcvad

from utils import audio, config_reader


# ========== Variables ==========
config: dict[str, Any] = config_reader.Config("client")
aggression: int = config["audio"]["supression_level"]
speech_detector = webrtcvad.Vad()
speech_detector.set_mode(aggression)


# ========== Functions ==========
def supress(data: bytes, aggression: int = aggression) -> bytes:
    """Returns a silent chunk unless speech is detected.

    Params:
        :param data (bytes): the chunk of data to process & supress.
        :param aggression (int, optional): the level of confidence required to pass as speech. Range 1 - 3.
    Returns:
        :return data (bytes): a chunk of silence if no speech was detected, otherwise returns the original chunk."""

    speech_detector.set_mode(aggression)
    if speech_detector.is_speech(data, sample_rate=config["audio"]["sample_rate"], length=config["audio"]["chunk_size"]):
        return data
    else:
        return audio.bogus_data
