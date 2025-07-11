# OCI Backup & Restore Automation

**Automated boot & block volume backups and restores in Oracle Cloud Infrastructure using the Python SDK with instance principal authentication.**  
Improves platform resilience and eliminates manual backup errors by implementing a lightweight, reusable backup and restore pattern.

---

## 📄 Overview

Manually backing up and restoring OCI boot and block volumes is time-consuming and error-prone.  
This automation orchestrates backups and restores using Python and the OCI SDK, running under the executing compute instance’s instance principal (no config file required).

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
- Run on an OCI compute instance or Cloud Shell with appropriate IAM policies assigned.
- Python 3.x (pre-installed in Cloud Shell and Oracle Linux instances).
- OCI Python SDK (pre-installed in Cloud Shell and most Oracle Linux images).

### 🔷 Configure
Before running, replace the `COMPARTMENT_ID` variable in `01_instance_select.py` with your target compartment OCID:

```python
COMPARTMENT_ID = "<your_compartment_ocid>"
