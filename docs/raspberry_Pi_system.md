# 🚀 Booting Raspberry Pi OS from SSD NVMe (Instead of microSD)

This guide explains how to **move your Raspberry Pi OS (Raspberry Pi OS with Desktop)** from the microSD card to an **SSD NVMe**, providing better performance and reliability.


## Index
1. [Requirements](#-requirements)
2. [Steps for Copy the Operating System to the NVMe (Cloning)](#️-step-1--copy-the-operating-system-to-the-nvme-cloning)
3. [Result](#-result)
4. [Credits](#-credits)

## 🧰 Requirements

- Raspberry Pi 5 with an **M.2 HAT+** or compatible PCIe adapter
- A **connected NVMe SSD**
- A **microSD card** with Raspberry Pi OS installed
- **Rufus** (or similar tool) to flash the `.iso` image

🔗 [Download Raspberry Pi OS](https://www.raspberrypi.com/software/operating-systems/)

----

## ⚙️ Step 1 — Copy the Operating System to the NVMe (Cloning)

The easiest way to transfer your OS is by using the built-in **SD Card Copier** utility.

1. **Open SD Card Copier:**
   - On Raspberry Pi OS desktop:
     ```
     Menu → Accessories → SD Card Copier
     ```
   - (You can also launch it from the terminal, but the graphical interface is simpler.)

2. **Set up the copy:**
   - **Copy From:** your current **microSD card** (where the OS is running)
   - **Copy To:** your **NVMe SSD** (usually `/dev/nvme0n1` or similar)

3. **Start the cloning process:**
   - Click **Start**
   - The utility will clone all partitions and data, including the boot partition
   - Wait until the process completes — it may take several minutes

---

## ⚙️ Step 2 — Configure the Boot Order

Once cloning is complete, configure your Raspberry Pi to boot from the NVMe drive first.

1. **Open the terminal and run:**
   ```bash
    sudo raspi-config
    ```
2. **Navigate to boot options:**

    ``` mathematica
    6 Advanced Options → A7 Boot Order
    ```
3. **Select NVMe/USB Boot:**

    ``` mathematica
    Choose NVMe/USB Boot as the first boot option.
    ```

4. **Finish and reboot:**
    ``` mathematica
    Select Finish
    ```
When prompted, choose Yes to reboot the system.

## ⚙️ Step 3 — Boot from the SSD NVMe
1. After shutting down, you can remove the microSD card (optional but recommended).
2. Power on your Raspberry Pi again.
3. The system should now boot directly from the NVMe SSD.

## 🎯 Result
Your Raspberry Pi is now running Raspberry Pi OS directly from the SSD NVMe, providing:

- ⚡ Significantly faster performance

- 💾 Better durability

- 🚀 Quicker startup times

## 🧩 Credits
Based on the official documentation from the Raspberry Pi Foundation.
This guide was adapted for practical use with Raspberry Pi 5 and NVMe SSDs.

