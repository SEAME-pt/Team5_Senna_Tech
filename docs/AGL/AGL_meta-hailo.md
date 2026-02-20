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







