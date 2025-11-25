## AGL (Automotive Grade Linux) initial setup and configurations

This documentation describes the process to setup configurations in our system such as (WIFI, Camera, Environnment variables, etc...)

This documentation is being updated regularly as we progress with the necessary configurations.

---

## 🧭 Summary
- [1️⃣ Enable Wifi](#1️⃣-enable-wifi)
- [2️⃣ Enable Wifi](#2️⃣-autostart-qt)

## 1️⃣ Enable Wifi

Follow these steps to connect your **AGL** (Automotive Grade Linux) system to **Wi-Fi** using connmanctl:

---

### Connection Steps

*  **Unblock wireless devices**
    ```bash
    rfkill unblock all
    ```

*  **Bring up the Wi-Fi interface**
    ```bash
    ip link set up wlan0
    ```

*  **Enter connmanctl**
    ```bash
    connmanctl
    ```

---

### Commands Inside `connmanctl`

Inside the `connmanctl` prompt, run the following commands:

* **Scan for available Wi-Fi networks**
    ```bash
    scan wifi
    ```

* **List available services**
    ```bash
    services
    ```

* **Connect to your network**
    ```bash
    connect <network_name>
    ```
    (Enter the **Wi-Fi password** when prompted.)

---

### Verify Connection

* **Check your IP address** (exit `connmanctl` first)
    ```bash
    ip addr show
    ```

## 2️⃣ Autostart QT


This guide explains how to create, configure, and enable a systemd service (car-start.service) that automatically launches our Qt application (appcar_cluster) on a Raspberry Pi

📁 **1. Create the Startup Script /usr/bin/car-start.sh**

Create the startup script:

```
vim /usr/bin/car-start.sh
```

Insert:

```
#!/bin/bash

# Environment variables required for Wayland
export XDG_RUNTIME_DIR=/run/user/0
export WAYLAND_DISPLAY=/run/wayland-0

# Go to the directory containing the binary
cd /home

# Execute the binary
./appcar_cluster
```

Save and exit.

Make it executable:
```
chmod +x /usr/bin/car-start.sh
```

⚙️ 2. **Create the systemd service /etc/systemd/system/car-start.service**

Create the service file:

```
vim /etc/systemd/system/car-start.service
```


Insert the following:

```
[Unit]
Description=Car AutoStart Qt
After=graphical-session.target

[Service]
Type=simple
Environment=WAYLAND_DISPLAY=wayland-0
Environment=XDG_RUNTIME_DIR=/run/user/0
ExecStart=/usr/bin/car-start.sh
Restart=always
RestartSec=5

[Install]
WantedBy=default.target
```


Save and exit.

🔄 **3. Reload systemd**

Whenever you create or edit a service:

```
systemctl daemon-reload
```

▶️ **4. Test the Service**

Start manually:

```
systemctl start car-start.service
```

Check logs:

```
journalctl -u car-start.service -f
```

🔐 **5. Enable the Service at Boot**
```
systemctl enable car-start.service
```


🧹 **6. Useful Commands**

Stop the service:

```
systemctl stop car-start.service
```

Disable autostart:

```
systemctl disable car-start.service
```

View status:

```
systemctl status car-start.service
```