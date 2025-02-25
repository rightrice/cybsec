sudo nano /etc/systemd/system/unifi_monitor.service


[Unit]
Description=UniFi Network Monitor
After=network.target

[Service]
ExecStart=/usr/bin/python3 /path/to/FILENAME.py
WorkingDirectory=/path/to/
StandardOutput=append:/var/log/unifi_monitor.log
StandardError=append:/var/log/unifi_monitor.log
Restart=always
User=your_username

[Install]
WantedBy=multi-user.target


sudo systemctl daemon-reload
sudo systemctl enable unifi_monitor.service
sudo systemctl start unifi_monitor.service