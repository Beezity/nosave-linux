from __future__ import annotations

import json
import subprocess

import psutil

GAME_EXE = "GTA5_Enhanced.exe"
GAME_APP_ID = "steam_app_3240220"


class Game:
    @staticmethod
    def process():
        """Return the GTA process or None."""
        for proc in psutil.process_iter(["pid", "name", "cmdline"]):
            try:
                name = proc.info["name"] or ""
                cmdline = " ".join(proc.info["cmdline"] or [])

                if (
                    name.startswith("GTA5_Enhanced")
                    or GAME_EXE in cmdline
                ):
                    return proc

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return None

    @staticmethod
    def running() -> bool:
        return Game.process() is not None

    @staticmethod
    def focused() -> bool:
        try:
            output = subprocess.check_output(
                ["niri", "msg", "-j", "focused-window"],
                text=True,
            )

            window = json.loads(output)

            return window.get("app_id") == GAME_APP_ID

        except Exception:
            return False

    @staticmethod
    def ready() -> bool:
        return Game.running() and Game.focused()
