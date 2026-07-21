#!/usr/bin/env python3

import os
import sys
import time
import signal
import atexit

from firewall import FirewallManager
from game import Game
from notify import notify


PID_FILE = "/tmp/nosave.pid"

firewall = FirewallManager()
enabled = False


def cleanup():
    """
    Remove firewall rule if we enabled it.
    """
    global enabled

    if enabled:
        firewall.disable()
        notify("No Save", "Disabled")
        enabled = False

    try:
        os.remove(PID_FILE)
    except FileNotFoundError:
        pass


def handle_exit(signum, frame):
    cleanup()
    sys.exit(0)


def already_running():
    """
    Prevent multiple keybind presses from creating multiple watchers.
    """

    if os.path.exists(PID_FILE):
        try:
            with open(PID_FILE, "r") as f:
                pid = int(f.read())

            os.kill(pid, 0)
            return True

        except (ProcessLookupError, ValueError):
            pass

    with open(PID_FILE, "w") as f:
        f.write(str(os.getpid()))

    return False


def main():

    global enabled

    if already_running():
        return

    atexit.register(cleanup)

    signal.signal(signal.SIGTERM, handle_exit)
    signal.signal(signal.SIGINT, handle_exit)


    # If a previous run died unexpectedly,
    # make sure stale firewall state is gone.
    if firewall.enabled():
        firewall.disable()


    notify("No Save", "Waiting for game...")


    while True:

        running = Game.running()


        if running and not enabled:
            if firewall.enable():
                notify("No Save", "Enabled")

            enabled = True


        elif not running and enabled:
            if firewall.disable():
                notify("No Save", "Disabled")

            enabled = False


        time.sleep(1)


if __name__ == "__main__":
    main()
