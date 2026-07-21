# vkit-linux

The nosave exploit for **Big Wheely Stealy the 5th**. Super cool game.

This tool mainly targets Linux systems, especially those running Fedora/Niri, but you can easily adapt the script to work more universally.

## 🚀 Instructions

### 1. Clone the Repository
First, clone the repository to your local machine:

```bash
git clone https://github.com/Beezity/nosave-linux/
```

### 2. Install the Helper Script
This step covers installing and configuring the Python helper script.

Create a new file at `/usr/local/bin/nosave-helper` and paste the following Python code into it:

```python
#!/usr/bin/env python3

import sys
import subprocess


REMOTE_IP = "192.81.241.171"

TABLE = "nosave"
SET = "blocked_ips"


def run_nft(*args):
    return subprocess.run(
        [
            "nft",
            *args
        ],
        capture_output=True,
        text=True,
    )


def enabled():
    """
    Check if the IP already exists in the nftables set.
    """
    result = run_nft(
        "list",
        "set",
        "inet",
        TABLE,
        SET,
    )

    if result.returncode != 0:
        return False

    return REMOTE_IP in result.stdout


def enable():
    """
    Add IP only if it does not exist.
    """
    if enabled():
        return True

    result = run_nft(
        "add",
        "element",
        "inet",
        TABLE,
        SET,
        "{",
        REMOTE_IP,
        "}",
    )

    return result.returncode == 0


def disable():
    """
    Remove IP only if it exists.
    """
    if not enabled():
        return True

    result = run_nft(
        "delete",
        "element",
        "inet",
        TABLE,
        SET,
        "{",
        REMOTE_IP,
        "}",
    )

    return result.returncode == 0


def main():
    if len(sys.argv) != 2:
        print("Usage: nosave-helper <enable|disable>")
        return 1

    action = sys.argv[1]

    if action == "enable":
        return 0 if enable() else 1

    if action == "disable":
        return 0 if disable() else 1

    print("Invalid action")
    return 1


if __name__ == "__main__":
    sys.exit(main())
```

Next, make the script executable by running:

```bash
sudo chmod 755 /usr/local/bin/nosave-helper
```

### 3. Configure Sudoers
To allow the script to modify `nftables` without prompting for a password every time, you need to add a sudoers rule.

Run the following command to create a new sudoers file:

```bash
sudo visudo -f /etc/sudoers.d/nosave
```

Inside the file, paste the following line (replace `YOUR_USERNAME` with your actual Linux username, e.g., `beezity`):

```sudoers
YOUR_USERNAME ALL=(root) NOPASSWD: /usr/local/bin/nosave-helper *
```

## 🎮 Usage

Once installed and configured, you can use the helper script to enable or disable the rule:

- **Add the rule to nftables:**
  ```bash
  /usr/local/bin/nosave-helper enable
  ```
- **Delete the rule from nftables:**
  ```bash
  /usr/local/bin/nosave-helper disable
  ```
Optionally, you may also bind this to a keybind so that you don't need to manually run the helper everytime via the terminal.
