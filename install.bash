#!/bin/bash

chmod +x main.py
sudo apt install python3-pip
pip3 install -r requirements.txt

cat > /etc/systemd/system/cloudwebcamera.service <<EOF
[Unit]
Description=CloudWebCamera By Reques6e
After=network.target

[Service]
User=root
WorkingDirectory=$(pwd)
ExecStart=python main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable cloudwebcamera
systemctl start cloudwebcamera

echo "Установка завершена."
