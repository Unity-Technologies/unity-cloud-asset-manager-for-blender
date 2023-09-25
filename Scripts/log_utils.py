import sys
import os
# https://en.wikipedia.org/wiki/ANSI_escape_code#Colors
colors = {
    "reset": "\x1b[0m",
    "red": "\x1b[31m",
    "green": "\x1b[32m",
    "yellow": "\x1b[33m",
    "cyan": "\x1b[36m",
}


def __log(color: str, msg: str):
    print(f"{__c(color, msg)}")


def __is_windows():
    return sys.platform == "win32" and os.name == "nt"


def __c(color: str, msg: str) -> str:
    if __is_windows():
        return msg
    else:
        return colors[color] + msg + colors["reset"]


def log_ok(msg: str):
    __log("green", msg)


def log_warning(msg: str):
    __log("yellow", f"WARNING: {msg}")


def log_error(msg: str):
    __log("red", f"ERROR: {msg}")
