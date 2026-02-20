## AGL (Automotive Grade Linux) initial setup and configurations

This documentation describes the process to setup configurations in our system such as (WIFI, Camera, Environnment variables, etc...)

This documentation is being updated regularly as we progress with the necessary configurations.

---

## 🧭 Summary
- [Enable Wifi and SSH](#enable-wifi-and-ssh)

## Enable Wifi and SSH

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
    agent on
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
