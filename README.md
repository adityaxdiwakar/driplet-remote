Proudly open source, operated by aditya holdings.

# remote

The remote control operator for Driplet's central server, this is what you install to your server.

Keep in mind, the remote is still unstable and may not work consistently, manual restarts **may** be required.

## Usage

There are two methods to install the remote onto your server, the first is easiest but requires ``python3 --version`` to be 3.6 or higher, if not; this will not work.

Before you begin, you will need two pieces of information for either version, these being the ``CLIENT_ID`` and ``ACCESS_TOKEN``.

Make an account and log into ``https://driplet.cf`` and open the developer tools using ``Ctrl+Shift+I``, go to the ``Application`` window to view local storage; there are *two* stored items; ``token`` and ``userid``, these correspond to ``ACCESS_TOKEN`` and ``CLIENT_ID`` respectively.

### Method 1

Run the following commands on your server in any directory:
```bash
wget https://dl.driplet.cf/install.sh
sudo chmod +x install.sh
sudo bash install.sh
```

The installation script will prompt you for the ID and Token metioned above, provide it accordingly.

### Method 2
Manual Installation

If the script above does not work, you may not have ``python3`` mapped to a version ``>= 3.6``, in which case you will need to manually do the following steps.

This guides assumes your system has a version of Python ``>=3.6``

Navigate to the installation directory:
```bash
cd /opt 
```

Clone the repository:
```bash
git clone https://github.com/driplet/remote
```

Change the name of the new directory to something less arbitrary:
```bash
mv remote/ driplet/
```

Navigate into the directory of the downloaded files:
```bash
cd driplet/
```

Install the pre-requisities, this comamnd may differ for people based on what command you need to use Python from (i.e if you built from source, ``python3.7``):
```bash
python3 -m pip install -r requirements.txt
```

You now need to create an environment file by doing ``nano .env`` (or another editor)
```env
CLIENT_ID="<your user id>"
ACCESS_TOKEN="<your access token>"
```
Do not type the angle brackets ``<>`` but make sure you use quotes.

Once you've done that, save the file and close it.

To run the remote, run ``python3 master.py``

You can now run this using a ``tmux`` screen or use a systemd unit as described below

#### Systemd Unit Creation

Run the following command to make your service file in the systemd directory:
```
sudo nano /etc/systemd/system/driplet.service
```

Use the template for making your unit:
```conf
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
```

Your mileage may vary on the ``ExecStart=/usr/bin/env python3...``, this may need to be replaced accordingly.

Once you have finished your file, save and close the file.

Now, restart the systemctl daemon:
```bash
systemctl daemon-reload
```

Next, enable your new service to start on boot:
```bash
systemctl enable driplet
```

Finally, start your service:
```bash
systemctl start driplet
```

## Support

If you need any help with the remote, feel free to open a GitHub issue or email me at ``aditya@diwakar.io``, I'm also available at Discord @ ``aditya#1337``.
