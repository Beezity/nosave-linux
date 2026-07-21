import subprocess

NOTIFY_ID = "6969"

def notify(title: str, message: str):
    subprocess.run([
        "notify-send",
        "-a", "No Save",
        "-r", NOTIFY_ID,
        title,
        message,
    ])
