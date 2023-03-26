"""Shared methods"""
import os
import sys


def log_error(message):
    print(f"[desstv] ERROR | {message}", file=sys.stderr)


def log_warn(message=""):
    print(f"[desstv] WARN  | {message}", file=sys.stderr)


def log_info(message="", recur=False):
    end = "\n"
    if recur:
        end = "\r"
        if sys.platform == "win32":
            message = "".join(["\r[desstv] INFO | ", message])
        cols = os.get_terminal_size().columns
        if cols < len(message):
            message = message[:cols]

    print(f"[desstv] INFO  | {message}", file=sys.stderr, end=end)


def progress_bar(progress, complete, message="", show=True):
    """Dynamic refreshing loading bar"""

    if not show:
        return

    message_size = len(message) + 18  # prefix size of "[desstv] INFO  | "
    cols = os.get_terminal_size().columns
    percent_on = True
    level = progress / complete
    bar_size = min(cols - message_size - 10, 100)
    bar = ""

    if bar_size > 5:
        fill_size = round(bar_size * level)
        bar = "[{}]".format("".join(["#" * fill_size, "." * (bar_size - fill_size)]))
    elif bar_size < -3:
        percent_on = False

    percent = ""
    if percent_on:
        percent = "{:4d}%".format(int(level * 100))

    align = cols - message_size - len(percent)
    not_end = progress != complete
    log_info("{}{:>{width}}{}".format(message, bar, percent, width=align), recur=not_end)
