"""Parsing arguments and starting program from command line"""

import argparse
import os.path
from sys import exit
from typing import BinaryIO

from PIL import Image
from soundfile import available_formats as available_audio_formats

from . import util
from .convert import AdditionalAudioFormatSupport
from .decode import SSTVDecoder
from .spec import VIS_MAP


class SSTVCommand(object):
    """Main class to handle the command line features"""

    examples_of_use = """
examples:
  Decode local SSTV audio file named 'audio.ogg' to 'result.png':
    $ desstv -d audio.ogg

  Decode SSTV audio file in /tmp to './image.jpg':
    $ desstv -d /tmp/signal.wav -o ./image.jpg

  Start decoding SSTV signal at 50.5 seconds into the audio
    $ desstv -d audio.ogg -s 50.50"""

    def __init__(self, shell_args):
        """Handle command line arguments"""

        self.args = self.parse_args(shell_args)
        self._output_file: str = self.args.output_file
        self._skip = self.args.skip

        audio_file = self.args.audio_file
        if not os.path.exists(audio_file):
            util.log_error("No such file or directory: [{}]".format(audio_file))
            exit(2)
        self._audio_file: BinaryIO = AdditionalAudioFormatSupport.handle_audio_file(audio_file)

    def parse_args(self, shell_args):
        """Parse command line arguments"""

        parser = self.build_parser()
        args = parser.parse_args(shell_args)

        if args.list_modes:
            self.list_supported_modes()
            exit(0)
        if args.list_audio_formats:
            self.list_supported_audio_formats()
            exit(0)
        if args.list_image_formats:
            self.list_supported_image_formats()
            exit(0)
        if args.audio_file is None:
            parser.print_help()
            exit(2)

        return args

    def build_parser(self):
        """Initialise argparse parser"""

        version = "desstv 0.1"

        parser = argparse.ArgumentParser(
            prog="desstv", formatter_class=argparse.RawDescriptionHelpFormatter, epilog=self.examples_of_use
        )

        parser.add_argument("-d", "--decode", type=str, help="decode SSTV audio file", dest="audio_file")
        parser.add_argument(
            "-o",
            "--output",
            type=str,
            help="save output image to custom location",
            default="result.png",
            dest="output_file",
        )
        parser.add_argument(
            "-s", "--skip", type=float, help="time in seconds to start decoding signal at", default=0.0, dest="skip"
        )
        parser.add_argument("-V", "--version", action="version", version=version)
        parser.add_argument("--list-modes", action="store_true", dest="list_modes", help="list supported SSTV modes")
        parser.add_argument(
            "--list-audio-formats",
            action="store_true",
            dest="list_audio_formats",
            help="list supported audio file formats",
        )
        parser.add_argument(
            "--list-image-formats",
            action="store_true",
            dest="list_image_formats",
            help="list supported image file formats",
        )
        return parser

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, traceback):
        self.close()

    def __del__(self):
        self.close()

    def start(self):
        """Start decoder"""

        with SSTVDecoder(self._audio_file) as sstv:
            img = sstv.decode(self._skip)
            if img is None:
                util.log_error(f"No SSTV signal found in [{self._audio_file}]")
                exit(2)

            try:
                img.save(self._output_file)
            except (KeyError, ValueError):
                util.log_error("Error saving file, saved to [./result.png] instead")
                img.save("result.png")

    def close(self):
        """Closes any input/output files if they exist"""
        try:
            if self._audio_file is not None and not self._audio_file.closed:
                self._audio_file.close()
        except AttributeError:
            pass

    @staticmethod
    def list_supported_modes():
        modes = ", ".join([fmt.NAME for fmt in VIS_MAP.values()])
        print("Supported modes: {}".format(modes))

    @staticmethod
    def list_supported_audio_formats():
        additional_formats = [e.upper() for e in AdditionalAudioFormatSupport.formats()]
        audio_formats = ", ".join(available_audio_formats().keys() + additional_formats)
        print("Supported audio formats: {}".format(audio_formats))

    @staticmethod
    def list_supported_image_formats():
        Image.init()
        image_formats = ", ".join(Image.SAVE.keys())
        print("Supported image formats: {}".format(image_formats))
