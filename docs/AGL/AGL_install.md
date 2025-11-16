## AGL (Automotive Grade Linux) installation


This documentation describes the complete process for installing and running **Automotive Grade Linux (AGL)** on a RaspBerry Pi5.

---

## 🧭 Summary
- [Requisites](#-requisites)
- [1️⃣ Preparing environment](#1️⃣-preparing-environment)
- [2️⃣ Download AGL](#2️⃣-download-agl)
- [3️⃣ Build for RaspBerryPi 5](#2️⃣-download-agl)
- [4️⃣ Flash to microSD](#4️⃣-flash-to-microsd)
- [📚 References](#-referências)

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


---