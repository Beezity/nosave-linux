from evdev import InputDevice, ecodes
import threading


class Listener:
    def __init__(self, device_path, on_press=None, on_release=None):
        self.device = InputDevice(device_path)
        self.on_press = on_press
        self.on_release = on_release
        self.running = True

    def start(self):
        threading.Thread(target=self._loop, daemon=True).start()

    def stop(self):
        self.running = False

    def _loop(self):
        for event in self.device.read_loop():
            if not self.running:
                break

            if event.type != ecodes.EV_KEY:
                continue

            key = ecodes.KEY.get(event.code)

            if event.value == 1:
                if self.on_press:
                    self.on_press(key)

            elif event.value == 0:
                if self.on_release:
                    self.on_release(key)