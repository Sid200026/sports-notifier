import os
from sys import platform, exit


def notify(title, text):
    if platform == 'darwin':
        notifyMACOS(title, text)
    elif platform == 'linux':
        notifyLinux(title, text)
    else:
        exit()


def notifyMACOS(title, text):
    os.system(f"""
              osascript -e 'display notification "{text}" with title "{title}"'
              """)


def notifyLinux(title, text):
    os.system(f"""
                notify-send '{title}' '{text}'
                """)
