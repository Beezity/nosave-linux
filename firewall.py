import subprocess


REMOTE_IP = "192.81.241.171"


class FirewallManager:
    TABLE = "nosave"
    SET = "blocked_ips"

    HELPER = "/usr/local/bin/nosave-helper"


    def _run_helper(self, action):
        """
        Run the privileged helper.
        """

        result = subprocess.run(
            [
                "sudo",
                self.HELPER,
                action
            ],
            capture_output=True,
            text=True,
        )

        return result.returncode == 0


    def _run_nft(self, *args):
        """
        Read-only nft queries.
        These do not require root.
        """

        return subprocess.run(
            [
                "nft",
                *args
            ],
            capture_output=True,
            text=True,
        )


    def enabled(self):
        """
        Check if the IP is currently in the nftables set.
        """

        result = self._run_nft(
            "list",
            "set",
            "inet",
            self.TABLE,
            self.SET,
        )

        if result.returncode != 0:
            return False

        return REMOTE_IP in result.stdout


    def enable(self):
        """
        Add block rule only if missing.
        """

        if self.enabled():
            return False

        return self._run_helper("enable")


    def disable(self):
        """
        Remove block rule only if present.
        """

        if not self.enabled():
            return False

        return self._run_helper("disable")


    def toggle(self):
        """
        Toggle firewall state.
        """

        if self.enabled():
            self.disable()
            return False

        self.enable()
        return True
