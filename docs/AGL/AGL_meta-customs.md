# 📄 Custom Layers Documentation for SEA:ME Project

## Table of Contents

1. [Overview](#overview)
2. [Layer `meta-services`](#layer-meta-services)

   * [Directory Structure](#directory-structure)
   * [Implemented Recipes](#implemented-recipes)
   * [Services and Scripts](#services-and-scripts)
3. [Layer `meta-clusterqt`](#layer-meta-clusterqt)

   * [Directory Structure](#directory-structure-1)
   * [Implemented Recipes](#implemented-recipes-1)
   * [Cluster Application Files Installation](#cluster-application-files-installation)
4. [Build and Deployment Flow](#build-and-deployment-flow)
5. [Considerations and Best Practices](#considerations-and-best-practices)

---

## Overview

These custom layers were created to manage:

* **`meta-services`**: system services (systemd), initialization scripts, and custom application directories (e.g., `Kuksa`).
* **`meta-clusterqt`**: ClusterQT application files and Weston compositor configuration.

The goal is to allow other developers to include these layers in the **Yocto/AGL build** without conflicts, keeping control over project-specific scripts and services.

---

## Layer `meta-services`

### Directory Structure

```
meta-services/
├── COPYING.MIT
├── README.md
├── conf/
│   └── layer.conf
├── recipes-core/
│   └── services/
│       ├── files/
│       │   ├── check-update.service
│       │   ├── cluster_release.sh
│       │   ├── rc.local
│       │   ├── wifi-up.service
│       │   ├── Kuksa/
│       │   ├── odometer_writer
│       │   └── odometer.service
│       └── services.bb
└── recipes-example/
    └── example/
```

### Implemented Recipes

* **`services.bb`**:
  Main recipe that installs scripts, services, and project directories.

**Summary:**

| Property          | Value / Function                                                                               |
| ----------------- | ---------------------------------------------------------------------------------------------- |
| `SUMMARY`         | "System Services"                                                                              |
| `LICENSE`         | "CLOSED"                                                                                       |
| `inherit`         | systemd                                                                                        |
| `RDEPENDS`        | bash                                                                                           |
| `SRC_URI`         | Includes all scripts and services in `files/`                                                  |
| `SYSTEMD_SERVICE` | Lists services to be auto-enabled (`check-update`, `wifi-up`, `odometer`)                      |
| `do_install()`    | Copies scripts to `${bindir}`, services to `${systemd_system_unitdir}`, and `Kuksa` to `/home` |
| `FILES:${PN}`     | Defines which files are included in the final package                                          |

### Services and Scripts

* **Scripts installed in `/usr/bin/`**:

  * `cluster_release.sh`
  * `odometer_writer`

* **Systemd services**:

  * `check-update.service`
  * `wifi-up.service`
  * `odometer.service`

* **Additional directories and files**:

  * `/home/Kuksa` (application/custom files)
  * `/etc/rc.local` (startup configuration)

* **Behavior**:

  * Services are **automatically enabled** on system boot (`SYSTEMD_AUTO_ENABLE = "enable"`).

---

## Layer `meta-clusterqt`

### Directory Structure

```
meta-clusterqt/
├── recipes-core/
│   └── clusterqt/
│       ├── clusterqt-files.bb
│       └── files/
│           ├── clusterqt/
│           └── weston.ini.default
```

### Implemented Recipes

* **`clusterqt-files.bb`**:
  Installs ClusterQT application files and Weston configuration.

**Summary:**

| Property       | Value / Function                                                                                          |
| -------------- | --------------------------------------------------------------------------------------------------------- |
| `SUMMARY`      | "ClusterQT Application Files"                                                                             |
| `LICENSE`      | "CLOSED"                                                                                                  |
| `SRC_URI`      | Includes `clusterqt` directory and `weston.ini.default` file                                              |
| `do_install()` | Copies `clusterqt/*` to `/opt/clusterqt` and `weston.ini.default` to `/etc/xdg/weston/weston.ini.default` |
| `FILES:${PN}`  | `/opt/clusterqt` and `/etc/xdg/weston/weston.ini.default`                                                 |

### Cluster Application Files Installation

* **Application directory**: `/opt/clusterqt`
* **Weston compositor configuration**: `/etc/xdg/weston/weston.ini.default`

> Note: Ensure `/etc/xdg/weston/` exists before installation.

---

## Build and Deployment Flow

1. Add the layers to your **bblayers.conf** in the AGL project.
2. Build the image with `bitbake`:

```bash
bitbake agl-image-minimal-crosssdk
```

3. The layers will install:

   * System scripts and services (`meta-services`)
   * ClusterQT application (`meta-clusterqt`)

4. On Raspberry/AGL device boot:

   * Services are automatically enabled via systemd
   * ClusterQT is available at `/opt/clusterqt`
   * Weston uses the custom configuration

---

## Considerations and Best Practices

* Always **check for conflicts** with kernel services or other layers.
* **Separate scripts and services** into distinct layers for easier maintenance.
* Use `do_install()` to copy files instead of modifying the image directly.
* Document each service and script to help new developers understand each component.
* For future versions, include **recipe versioning** and **dependency control**.
