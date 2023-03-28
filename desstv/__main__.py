"""Main entry point for command line program"""

import signal
from sys import exit, argv

from desstv import util
from desstv.command import SSTVCommand


def handle_sigint(_, __):
    # this line for break recur mode of previous log.
    util.log_info()
    util.log_info("Received interrupt signal, exiting...")
    exit(0)


def main():
    signal.signal(signal.SIGINT, handle_sigint)
    with SSTVCommand(argv[1:]) as prog:
        prog.start()


if __name__ == "__main__":
    main()
