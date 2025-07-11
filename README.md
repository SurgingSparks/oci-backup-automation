# OCI Backup & Restore Automation

**Automated boot & block volume backups and restores in Oracle Cloud Infrastructure using OCI CLI via Python orchestration.**  
Improves platform resilience and eliminates manual backup errors by implementing a lightweight, reusable backup and restore pattern.

---

## 📄 Overview

Manually backing up and restoring OCI boot and block volumes is time-consuming and error-prone.  
This automation orchestrates backups and restores using Python and the OCI CLI, running under the executing user’s authentication context (e.g., OCI config file or instance principal).

Designed for Oracle Cloud environments where RPO compliance and operational efficiency are critical.

---

## 🏗️ Architecture

![Architecture](diagrams/architecture.png)

**Workflow:**
1. Select compute instances in a compartment.
2. Identify attached boot and block volumes.
3. Backup volumes.
4. Restore volumes back into the same compartment (optional).

---

## 🚀 How to Run

### 🔷 Prerequisites
- OCI CLI installed & configured:
  - Install: https://docs.oracle.com/en-us/iaas/Content/API/SDKDocs/cliinstall.htm
  - Authenticated via `~/.oci/config` or instance principal

### 🔷 Run steps
```bash
python 01_instance_select.py
python 02_volume_identify.py
python 03_volume_backup.py
python 04_volume_restore.py
