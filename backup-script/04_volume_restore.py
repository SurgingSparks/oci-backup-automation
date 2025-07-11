#!/usr/bin/env python3

import oci
import json
import sys
from datetime import datetime
import pytz

BACKUP_FILE = "volume_backups.json"
RESTORE_FILE = "restored_volumes.json"
STATE_FILE = "state.json"

def load_json_or_exit(file_path, error_message):
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ {error_message}")
        sys.exit(1)

def restore_volumes(backups, state):
    config = oci.config.from_file()
    block = oci.core.BlockstorageClient(config)

    sydney = pytz.timezone("Australia/Sydney")
    timestamp = datetime.now(sydney).strftime('%Y%m%d-%H%M%S')

    restored = {}

    print("🔁 Restoring boot volume from backup...")
    boot_restore = block.create_boot_volume(
        create_boot_volume_details=oci.core.models.CreateBootVolumeDetails(
            availability_domain=state["availability_domain"],
            compartment_id=state["compartment_id"],            
            source_details=oci.core.models.BootVolumeSourceFromBootVolumeBackupDetails(
                id=backups["boot_volume_backup_id"],
                type="bootVolumeBackup"
            ),
            display_name=f"restored-{backups['boot_volume_backup_name']}-{timestamp}"
        )
    ).data

    print(f"✅ Boot volume restored: {boot_restore.display_name}")
    restored["boot_volume_id"] = boot_restore.id
    restored["boot_display_name"] = boot_restore.display_name

    restored["block_volumes"] = []

    for vol in backups.get("block_volume_backups", []):
        print(f"🔁 Restoring block volume: {vol['display_name']}")
        block_restore = block.create_volume(
            create_volume_details=oci.core.models.CreateVolumeDetails(
                availability_domain=state["availability_domain"],
                compartment_id=state["compartment_id"],  
                source_details=oci.core.models.VolumeSourceFromVolumeBackupDetails(
                    id=vol["backup_id"],
                    type="volumeBackup"
                ),
                display_name=f"restored-{vol['display_name']}-{timestamp}"
            )
        ).data
        print(f"✅ Block volume restored: {block_restore.display_name}")
        restored["block_volumes"].append({
            "volume_id": block_restore.id,
            "display_name": block_restore.display_name
        })

    return restored

def save_output(restored):
    with open(RESTORE_FILE, "w") as f:
        json.dump(restored, f, indent=2)
    print(f"💾 Restore info saved to {RESTORE_FILE}")

if __name__ == "__main__":
    state = load_json_or_exit(STATE_FILE, "state.json not found.")
    backups = load_json_or_exit(BACKUP_FILE, "volume_backups.json not found.")
    restored = restore_volumes(backups, state)
    save_output(restored)