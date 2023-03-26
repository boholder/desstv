"""Main entry point for command line program"""

import signal
from sys import exit

from desstv.command import SSTVCommand
from desstv.util import log_message


def handle_sigint(signal, frame):
    print()
    log_message("Received interrupt signal, exiting.")
    exit(0)


def main():
    signal.signal(signal.SIGINT, handle_sigint)
    with SSTVCommand() as prog:
        prog.start()


if __name__ == "__main__":
    main()
