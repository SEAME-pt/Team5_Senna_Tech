# Meta-Hailo Layer build for AGL

#### What Is meta-hailo in Yocto?

**meta-hailo** is a Yocto Project layer that provides the metadata, recipes, and configuration required to integrate Hailo AI accelerators into a Yocto-based Linux distribution.

## Step 1 — Create the Yocto Layer

The first step in creating the `meta-hailo` layer is to generate a new layer using the Yocto build system tools.

### Command

**1.1** From your Yocto build directory, run:

```bash
bitbake-layers create-layer meta-hailo
```

**1.2** Then run the following command, which will add your layer to the conf/bblayers.conf file in the build directory.

```bash
bitbake-layers add-layer meta-hailo
```

**1.3** After execution, the structure should look like this:

```bash
meta-hailo/
├── conf/
│   └── layer.conf
└── recipes-example/
    └── example/
        
```

## Step 2 — Integrate the Official Hailo Layer and Enable Required Packages

**2.1** Clone the Official Hailo Layer

Inside your Yocto project workspace, clone the official `meta-hailo` layer provided by Hailo:

```bash
git clone https://github.com/hailo-ai/meta-hailo.git
```

**2.2** Switch to a branch with a version compatible with your AGL version. 

**Important**: For the SennaTech team5, we use AGL trout. Therefore, we will use the hailo8-scarthgap branch from meta-hailo."

```bash
git checkout hailo8-scarthgap
```

**2.3** Enable Hailo Packages in the Image (Raspberry Pi 5)

For a Raspberry Pi 5 build, add this to your conf/local.conf:


```
IMAGE_INSTALL:append = " libhailort hailortcli hailo-pci pyhailort libgsthailo hailo-firmware"
Package Description
```

#### Packages Descriptions

- libhailort — Hailo Runtime shared library

- hailortcli — Command-line interface for device management

- hailo-pci — PCIe kernel driver

- pyhailort — Python bindings for HailoRT

- libgsthailo — GStreamer plugins for AI pipelines

- hailo-firmware — Required firmware binaries

## Step 3 — Fix Kernel Module Version Conflict

### Problem Description

When building for **Raspberry Pi (linux-raspberrypi)**, a common issue occurs during the integration of the `hailo-pci` driver.

The Raspberry Pi kernel attempts to automatically split and package kernel modules, which may cause it to fetch or generate a **different module version** than the one defined in the `hailo-pci` recipe.

#### Typical Scenario

- `hailo-pci` recipe version: **4.23.0**
- Raspberry Pi kernel attempts to install: **4.20.x**
- Result: **Version mismatch**
- Outcome: **HailoRT and hailo-pci failure due to module conflict**

#### Solution

Disable kernel module splitting specifically for `linux-raspberrypi` by creating a `.bbappend` file inside the `meta-hailo` layer.

This forces the build system to keep the module packaged as defined by the `hailo-pci` recipe.

---

#### Implementation

**3.1** Navigate to: meta-hailo/meta-hailo-accelerator/recipes-kernel/hailo-pci/


**3.2** Create the following file and add the content:

```
linux-raspberrypi_%.bbappend
```


File content

```bash
KERNEL_SPLIT_MODULES = "0"
```

#### What This Does?


- The kernel does not split the hailo-pci module

- The module version remains aligned with the recipe (4.23.0)

- The packaging stage does not generate conflicting module versions



## Step 4 — Build AGL image

```bash
bitbake agl-image-minimal-crosssdk
```

## Step 5 — Verify Hailo packages

**5.1 libhailort**

Ensure the file exists:

```
ls /usr/lib/libhailort.so
```

**5.2 hailortcli**

After connecting the hailo chip – scan and run commands should communicate with the board.

```
hailortcli scan
hailortcli run "example.hef"
```

**5.2 libgsthailo**

Running ```gst-inspect-1.0 | grep hailo``` returns hailo elements:

```
hailo:  hailodevicestats: hailodevicestats element
hailo:  hailonet: hailonet element
hailo:  synchailonet: sync hailonet element
```

**5.3 hailo-firmware**

Hailo’s firmware exists at: ```/lib/firmware/hailo/```


**5.3 hailo-pci**

Run:

```modinfo hailo-pci```

You must see a successful result and info about the driver. For example:

```filename:       /lib/modules/6.12.25-v8-16k/kernel/drivers/misc/hailo_pci.ko.xz
version:        4.23.0
license:        GPL v2
description:    Hailo PCIe driver
author:         Hailo Technologies Ltd.
import_ns:      DMA_BUF
srcversion:     6AA96411C62B9CA56BF4262
alias:          pci:v00001E60d00002864sv*sd*bc*sc*i*
depends:        
name:           hailo_pci
vermagic:       6.12.25-v8-16k SMP preempt mod_unload modversions aarch64
parm:           o_dbg:int
parm:           no_power_mode:Disables automatic D0->D3 PCIe transactions (invbool)
parm:           force_allocation_from_driver:Determines whether to force buffer allocation from driver or userspace (int)
parm:           force_desc_page_size:Determines the maximum DMA descriptor page size (must be a power of 2) (int)
parm:           force_hailo10h_legacy_mode:Forces work with Hailo10h in legacy mode(relevant for emulators) (bool)
parm:           force_boot_linux_from_eemc:Boot the linux image from eemc (Requires special Image) (bool)
parm:           support_soft_reset:enables driver reload to reload a new firmware as well (bool)
```



# References

- https://hailo.ai/developer-zone/documentation/hailort-v5-2-0/?sp_referrer=yocto/yocto.html#integrating-to-an-existing-yocto-environment

- https://github.com/hailo-ai/meta-hailo







