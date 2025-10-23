# 🧭 VPN and Remote Server Access Guide via NetBird + TigerVNC

## 1. Introduction
This guide helps new team members set up remote access to the team server using **NetBird (VPN)** and **TigerVNC (remote graphical client)**.
NetBird provides a secure connection to the internal network, while TigerVNC allows access to the server's graphical interface.

---

## 2. Prerequisites
Before starting, make sure you have:
- Access to the **team email** (required for NetBird authentication).
- A compatible operating system (**Windows**, **macOS**, or **Linux**).
- Permissions to install software on your machine.

---

## 3. NetBird Installation and Setup

### 3.1 Login
1. Go to the official website:
   [https://netbird.io/download](https://netbird.io/download)
2. Download and install the **NetBird Client** for your OS.
3. Open a terminal (or command prompt) and log in using the team email:
   ```bash
   netbird login
   ```
4. Authenticate in the browser with the team email (e.g., team@company.com).

### 3.2 Post-login Setup
After logging in, follow the official NetBird installation instructions for your OS:

- Linux: https://docs.netbird.io/how-to/install/linux
- macOS: https://docs.netbird.io/how-to/install/macos
- Windows: https://docs.netbird.io/how-to/install/windows

Once installed, start the VPN:

```bash
netbird up
```
Check the VPN status:

```bash
netbird status
```
You should see:
Status: Connected


## 4. Connectivity Test
Verify that you are on the internal network:

```bash
ping <internal-server-IP>
```
If you receive replies, the VPN is working correctly.

## 5. TigerVNC Installation and Use

### 5.1 Installation
Download **TigerVNC Viewer**:
[https://tigervnc.org](https://tigervnc.org)

Install it according to your operating system.

### 5.2 Connect to the Server
1. Open VNC Viewer.

2. Enter the server address and port provided by the team:
```ruby
<server-IP>:<port>
```
Example: 10.8.0.5:5901

3. Click Connect.

4. Enter the server password provided by the team when prompted.

## 6. Best Practices
- Always run netbird up before opening TigerVNC.
- Disconnect the VPN with netbird down when done.
- Do not share credentials or passwords.
- If you cannot connect:
    - Check that NetBird shows Connected.
    - Verify the server IP and port.
    - Ensure no firewall is blocking the connection.

