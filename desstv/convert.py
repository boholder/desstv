import os
import tempfile
from io import BufferedReader
from typing import Callable, BinaryIO

import pydub

from . import util


def mp3_to_ogg(mp3_file_path: str) -> BufferedReader:
    ogg_file_path = get_temp_ogg_file_path(mp3_file_path)
    return pydub.AudioSegment.from_mp3(mp3_file_path).export(ogg_file_path, format="ogg")


def get_temp_ogg_file_path(ori_file_path: str) -> str:
    d = os.path.dirname(ori_file_path)
    prefix = os.path.basename(ori_file_path)
    suffix = ".ogg"
    return tempfile.NamedTemporaryFile(dir=d, prefix=prefix, suffix=suffix, delete=True)


class AdditionalAudioFormatSupport(object):
    supported: dict[str, Callable[[str], BufferedReader]] = {
        "mp3": mp3_to_ogg,
    }

    @staticmethod
    def formats() -> list[str]:
        """Return list of supported audio file formats"""
        return list(AdditionalAudioFormatSupport.supported.keys())

    @staticmethod
    def handle_audio_file(file_path: str) -> BinaryIO:
        """
        If file is supported, convert it to OGG format and return the new ogg file path,
        otherwise return the original file path.
        Anyway the returned value is always acceptable for audio file processing library.
        """

        file_name = os.path.basename(file_path)
        file_suffix = file_name.split(".")[-1]

        if file_suffix in AdditionalAudioFormatSupport.supported:
            util.log_info(f"Preprocessing [{file_name}]...", recur=True)
            handler = AdditionalAudioFormatSupport.supported[file_suffix]
            ogg_file_stream = handler(file_path)
            util.log_info(f"Preprocessing [{file_name}]... Done!")
            return ogg_file_stream
        else:
            return open(file_path, "rb")
