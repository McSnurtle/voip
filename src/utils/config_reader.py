"""Reads config stuffs from `usr/conf/<name>.json`"""
# imports - config_reader.py, by Mc_Snurtle
import json
from typing import Any

from utils import path


# ========== Classes ==========
class Config(dict):
    def __init__(self, id: str, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.data: dict[str, Any] = {}

        if self._is_valid_id(id):
            self.id: str = id
        else:
            raise ValueError(f"parameter `id` should be either `'client'` or `'server'`. Got: `'{id}'`")

        with open(path.mkpath(path.config_dir, f"{self.id}.json"), "r") as file:
            config: dict = json.load(file)
            self._validate_config(config)
            for key, value in config.items():
                self[key] = value

    def __getitem__(self, key: str) -> Any:
        return self.data[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.data[key] = value

    def _validate_config(self, config: dict[str, Any]) -> None:
        """Checks if config values are invalid in some way.

        Params:
            :param dict[str, Any] config: the config derived from `usr/conf/<name>.json`.
        Returns:
            :returns bool: whether the config is valid or not
        Raises:
            :raises ValueError: if something's not right."""
        if self.id == "server":
            if config["networking"]["relay_audio"] == config["audio"]["hear_audio"]:
                raise ValueError( "Your `server.json` config is invalid! Parameter `audio/hear_audio` and `networking/relay_audio` are mutually exclusive values!" )

    def _is_valid_id(self, id: str) -> bool:
        return any(word is id for word in ["client", "server"])
