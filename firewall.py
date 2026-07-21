import subprocess

REMOTE_IP = "192.81.241.171"


class FirewallManager:
    TABLE = "nosave"
    SET = "blocked_ips"

    def _run(self, *args, root=False):
        cmd = ["nft", *args]

        if root:
            cmd.insert(0, "pkexec")

        return subprocess.run(
            cmd,
            capture_output=True,
            text=True,
        )

    def enabled(self):
        result = self._run(
            "list",
            "set",
            "inet",
            self.TABLE,
            self.SET,
        )

        return REMOTE_IP in result.stdout

    def enable(self):
        self._run(
            "add",
            "element",
            "inet",
            self.TABLE,
            self.SET,
            "{",
            REMOTE_IP,
            "}",
            root=True,
        )

    def disable(self):
        self._run(
            "delete",
            "element",
            "inet",
            self.TABLE,
            self.SET,
            "{",
            REMOTE_IP,
            "}",
            root=True,
        )

    def toggle(self):
        if self.enabled():
            self.disable()
            return False

        self.enable()
        return True
