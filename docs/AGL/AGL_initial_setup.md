## AGL (Automotive Grade Linux) initial setup and configurations

This documentation describes the process to setup configurations in our system such as (WIFI, Camera, Environnment variables, etc...)

This documentation is being updated regularly as we progress with the necessary configurations.

---

## 🧭 Summary
- [1️⃣ Enable Wifi](#1️⃣-enable-wifi)

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