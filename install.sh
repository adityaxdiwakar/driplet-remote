#!/bin/bash
# This script MUST be run as root.
if [[ $EUID -ne 0 ]]; then
   echo "This script must be run as root" 
   exit 1
fi

(apt-get update -y && apt-get upgrade -y)  >> install.log
apt-get install python3-pip -y  >> install.log

git clone https://github.com/driplet/remote /opt/driplet
cd /opt/driplet

pip3 install -r requirements.txt >> install.log

echo ""
read -p "Client ID: " clientid
read -p "Auth Token: " authtoken
echo "CLIENT_ID=\"$clientid\"" >> .env
echo "ACCESS_TOKEN=\"$authtoken\"" >> .env
echo ""
echo "Creating systemd service"

read -r -d '' unit << EOM
[Unit]
Description=Driplet Systemd Manager
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
ExecStart=/usr/bin/env python3 /opt/driplet/main.py

[Install]
WantedBy=multi-user.target
EOM

echo "$unit" >> /etc/systemd/system/driplet.service
systemctl enable driplet
systemctl start driplet

echo "Driplet service started"
echo "Cleaning up..."
cd ..
rm install.log install.sh
