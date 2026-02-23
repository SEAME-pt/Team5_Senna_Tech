# AGL Documentation Overview

This document provides a high-level guide to the available AGL documentation in the Team5_Senna_Tech/docs/AGL folder. It explains the purpose of each file and how it fits into our AGL project.

## 1. AGL_install.md

#### Purpose: Provides step-by-step instructions for installing Automotive Grade Linux (AGL) on our target hardware (e.g., Raspberry Pi).

**Content includes:**

- Required tools and dependencies

- Cloning the AGL repositories

- Building the AGL image

- Flashing the image onto the device

- Basic troubleshooting tips

## 2. AGL_meta-customs.md

#### Purpose: Describes the custom layers we have implemented for our project, such as meta-services and meta-clusterqt.

**Content includes:**

- Structure of each layer

- Purpose of recipes (e.g., system services, ClusterQT application files)

- How to add new services or applications

- Installation paths and how the layers integrate with AGL

## 3. AGL_meta-hailo.md

#### Purpose: Covers integration of the Hailo AI accelerator with AGL.

**Content includes:**

- Custom meta-layer for Hailo

- Installing runtime libraries and drivers

- Interaction with the Raspberry Pi and camera input

- Testing Hailo installation and verifying versions

- Troubleshooting driver and library conflicts

## 4. AGL_wifi_connect.md

#### Purpose: Explains how Wi-Fi connectivity is configured and managed on the AGL image.

**Content includes:**

- How to connect wifi for the first time


## 5. AGL_support.md

**Purpose: A general support guide for the AGL environment.
Content includes:**

- Common issues encountered during development

- Debugging tips and tools

- How to inspect system logs, services, and kernel modules

- Guidelines for adding new hardware support or features