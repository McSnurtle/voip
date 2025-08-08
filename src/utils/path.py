"""Operations for string paths"""
# imports - path.py, by Mc_Snurtle
import os


# ========== Variables ==========
cache_dir: str = "cache/"
config_dir: str = "usr/conf/"
secrets_dir: str = "usr/"
scripts_dir: str = "src/"
utils_dir: str = "src/utils/"


# ========== Functions ==========
def mkpath(*args: str, absolute: bool = False) -> str:
    """Returns a pathlike style string based on the elements `*args`.

    Params:
        :param *args (str): ordered list of strings to compile as a path.
        :param aboslute (bool): if the absolute path should be resolved before returning.
    Returns:
        :return path (str): the final path derived from `*args`."""

    path: str = os.path.join(*args)
    if absolute: path = os.path.abspath(path)
    return path
