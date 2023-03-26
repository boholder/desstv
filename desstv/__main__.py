"""Main entry point for command line program"""

import signal
from sys import exit, argv

from . import util
from .command import SSTVCommand


def handle_sigint(_, __):
    util.log_info("Received interrupt signal, exiting.")
    exit(0)


def main():
    signal.signal(signal.SIGINT, handle_sigint)
    with SSTVCommand(argv[1:]) as prog:
        prog.start()


if __name__ == "__main__":
    main()
