import socket
import threading
import time


class ConnectionMonitor:
    def __init__(self, ip: str, port: int = 80):
        self.ip = ip
        self.port = port

        self.blocked = None
        self.running = False

    def connected(self):
        try:
            with socket.create_connection(
                (self.ip, self.port),
                timeout=2,
            ):
                return True
        except OSError:
            return False

    def loop(self):
        while self.running:
            blocked = not self.connected()

            if blocked != self.blocked:
                self.blocked = blocked

                print(
                    f"Connection {'BLOCKED' if blocked else 'ACCESSIBLE'}"
                )

            time.sleep(2)

    def start(self):
        if self.running:
            return

        self.running = True

        threading.Thread(
            target=self.loop,
            daemon=True,
        ).start()

    def stop(self):
        self.running = False
