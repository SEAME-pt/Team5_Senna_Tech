
## AGL (Automotive Grade Linux) build for raspberrypi5


This documentation describes the complete process for installing and running **Automotive Grade Linux (AGL)** on a RaspBerry Pi5.

---

## 🧭 Summary
- [Requisites](#-requisites)
- [1️⃣ Preparing environment](#1️⃣-preparing-environment)
- [2️⃣ Download AGL](#2️⃣-download-agl)
- [3️⃣ Build for RaspBerryPi 5](#3️⃣-build-for-raspberrypi-5)
- [4️⃣ Flash to microSD](#4️⃣-flash-to-microsd)
- [5️⃣ Common Errors and Recommendations](#5️⃣-common-errors-and-recommendations)
- [📚 References](#📚-references)

## Requisites

Before building an AGL image, ensure your host system includes all necessary packages. The following packages are required for building images on a headless system using a supported Ubuntu or Debian Linux distribution:

**Minimum Free Disk Space**

Make sure you have at least 90 GB of available disk space and a **stable internet connection**. The build process may take several hours to complete.

**Install Required Host Packages**

``` bash
sudo apt-get install build-essential chrpath cpio debianutils diffstat file gawk gcc git iputils-ping \
libacl1 liblz4-tool locales python3 python3-git python3-jinja2 python3-pexpect python3-pip \
python3-subunit socat texinfo unzip wget xz-utils zstd
```

## 1️⃣ Preparing Environment

- Begin by defining an environment variable that will serve as your top-level AGL workspace directory.
The example below creates and assigns the folder $HOME/AGL to the environment variable AGL_TOP:

**1.1 Define Your Top-Level Directory**
``` bash
export AGL_TOP=$HOME/AGL
echo 'export AGL_TOP=$HOME/AGL' >> $HOME/.bashrc
mkdir -p $AGL_TOP
```

**1.2 Download the repo Tool and Set Permissions**

- AGL uses the repo tool to manage multiple Git repositories.
Use the following steps to install the tool and ensure it is executable:

``` bash
mkdir -p $HOME/bin
export PATH=$HOME/bin:$PATH
echo 'export PATH=$HOME/bin:$PATH' >> $HOME/.bashrc
curl https://storage.googleapis.com/git-repo-downloads/repo > $HOME/bin/repo
chmod a+x $HOME/bin/repo
```
## 2️⃣ Download AGL

The Automotive Grade Linux source code can be downloaded in different ways, depending on your development needs:

- Stable Release (recommended) – fixed, tested, and reliable

- Main Branch – latest development changes, but less stable

Currently, the most stable AGL release is **Trout**, which is the one we will download here.

**2.1 Download the Stable Release (Recommended: trout)**

To download the latest stable release — for example, the trout branch — use:

``` bash
cd $AGL_TOP
mkdir trout
cd trout
repo init -b trout -u https://gerrit.automotivelinux.org/gerrit/AGL/AGL-repo
repo sync
```

**2.2 Download the Main Branch (Cutting-Edge)**

If you want the most up-to-date development version, you can download the master branch.

``` bash
cd $AGL_TOP
mkdir trout
cd trout
repo init -b master -u https://gerrit.automotivelinux.org/gerrit/AGL/AGL-repo
repo sync
```

## 3️⃣ Build for RaspBerryPi 5

**3.1 Create the local.conf**

The **local.conf** is the main configuration file for your Yocto build environment.
In short, it tells Yocto how to build your system.

This script will create the build directory and the local.conf file:

``` bash
source meta-agl/scripts/aglsetup.sh -f -m raspberrypi5 -b raspberrypi5 agl-all-features agl-devel
```

- The -m flag is your target; set it to raspberrypi5.

- At the end of the line, include the features that make sense for your system:

    - agl-all-features: enables all standard AGL features, giving you a complete Automotive Grade Linux environment with most optional components included.

    - agl-devel: adds development tools and utilities, useful during development (debugging tools, extra logs, dev packages)

    - Check all available features: https://docs.automotivelinux.org/en/salmon/#01_Getting_Started/02_Building_AGL_Image/04_Initializing_Your_Build_Environment/


**3.2 Confirm that your local.conf is correct.**

These definitions must be present in your local.conf:

- MACHINE = "raspberrypi5"
- DISTRO = "poky-agl"
- BB_NUMBER_THREADS:   Set the number of parallel tasks that BitBake should run. For example, to run 8 tasks, use: BB_NUMBER_THREADS = "8"
- PARALLEL_MAKE: Set the number of tasks that the make tool should run in parallel. For example, to run 8 tasks, use: PARALLEL_MAKE = "-j8".


**3.3 Create cache to optimize future rebuilds**

This step is important because Yocto can create a cache of already downloaded files, saving a lot of time if you need to add new features to your build in the future.

``` bash
$ echo "# reuse download directories" >> $AGL_TOP/site.conf
$ echo "DL_DIR = \"$HOME/downloads/\"" >> $AGL_TOP/site.conf
$ echo "SSTATE_DIR = \"$AGL_TOP/sstate-cache/\"" >> $AGL_TOP/site.conf
$ ln -sf $AGL_TOP/site.conf conf/
```

**3.4 Use bitbake to build the image**

Start the build using the **bitbake** command.

``` bash
bitbake <IMAGE NAME>
```

Replace <IMAGE NAME> with the image of your choice. check: https://docs.automotivelinux.org/en/salmon/#01_Getting_Started/02_Building_AGL_Image/07_Available_Demo_Images/

For this building we'll select the agl-image-minimal-crosssdk

``` bash
bitbake agl-image-minimal-crosssdk
```

The build process can take a long time to be done.

Once the image compilation is complete, the .wic.xz image file will be located in something like:

```<build_dir>/tmp/deploy/images/raspberrypi5/<IMAGE NAME>-raspberrypi5.rootfs.wic.xz```

## 4️⃣ Flash to microSD

**4.1 Plug your MicroSD card into your Build Host**

**4.1 Extract the image and flash to the SD card**

``` bash
$ lsblk
$ sudo umount <sdcard_device_name>
$ xzcat ${IMAGE_NAME} | sudo dd of=<sdcard_device_name> bs=4M
$ sync
```

Afther that everythins is complete and you can start your Automotive Grade Linux in the RaspBerry Pi5 machine!

## 5️⃣ Common Errors and Recommendations

**5.1 Disable UART in boot/config.txt**

When starting AGL, it may hang during boot and redirect to UART. If this happens, you won’t be able to see the system on HDMI or another video output.
To fix the issue, open the ```boot/config.txt``` file located in the boot partition of your microSD and comment out the following line:

- ```# enable_uart=1```


**5.1 Lack of resources on the host during build**

Yocto builds require significant CPU, RAM, and disk space, so it is very common for the computer to kill Yocto processes due to excessive RAM usage. Therefore, set `BB_NUMBER_THREADS` and `PARALLEL_MAKE` in  `local.conf`according to your machine's specifications.

## 📚 References

- https://docs.automotivelinux.org
- https://lists.automotivelinux.org/g/agl-dev-community/topic/support_for_agl_in_raspberry/106649597

---

