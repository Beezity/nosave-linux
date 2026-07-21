import time

from firewall import FirewallManager
from game import Game
from notify import notify

REMOTE_IP = "192.81.241.171"


def main():
    firewall = FirewallManager()

    enabled = False

    while True:
        running = Game.running()

        if running and not enabled:
            firewall.enable()
            notify("No Save", "Enabled")
            enabled = True

        elif not running and enabled:
            firewall.disable()
            notify("No Save", "Disabled")
            enabled = False

        time.sleep(1)


if __name__ == "__main__":
    main()
