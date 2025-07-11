import oci
import json
import sys
from datetime import datetime
import pytz

VOLUME_FILE = "volumes.json"
BACKUP_FILE = "volume_backups.json"

def load_volumes():
    try:
        with open(VOLUME_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ volumes.json not found. Run volume_identify.py first.")
        sys.exit(1)

def backup_volumes(volumes):
    config = oci.config.from_file()
    block = oci.core.BlockstorageClient(config)

    sydney = pytz.timezone("Australia/Sydney")
    timestamp = datetime.now(sydney).strftime('%Y%m%d-%H%M%S')

    backups = {}

    print("🔄 Creating boot volume backup...")
    boot_vol = block.get_boot_volume(volumes["boot_volume_id"]).data
    boot_display_name = boot_vol.display_name

    boot_backup = block.create_boot_volume_backup(
        create_boot_volume_backup_details=oci.core.models.CreateBootVolumeBackupDetails(
            boot_volume_id=volumes["boot_volume_id"],
            display_name=f"backup-{boot_display_name}-{timestamp}",
            type="INCREMENTAL"
        )
    ).data

    print(f"✅ Boot backup started: {boot_backup.display_name}")
    backups["boot_volume_backup_id"] = boot_backup.id
    backups["boot_volume_backup_name"] = boot_backup.display_name

    backups["block_volume_backups"] = []

    for vol in volumes.get("block_volumes", []):
        print(f"🔄 Creating block volume backup: {vol['display_name']}")
        block_backup = block.create_volume_backup(
            create_volume_backup_details=oci.core.models.CreateVolumeBackupDetails(
                volume_id=vol["volume_id"],
                display_name=f"backup-{vol['display_name']}-{timestamp}",
                type="INCREMENTAL"
            )
        ).data
        print(f"✅ Block backup started: {block_backup.display_name}")
        backups["block_volume_backups"].append({
            "volume_id": vol["volume_id"],
            "backup_id": block_backup.id,
            "display_name": block_backup.display_name
        })

    return backups

def save_output(backups):
    with open(BACKUP_FILE, "w") as f:
        json.dump(backups, f, indent=2)
    print(f"💾 Backup info saved to {BACKUP_FILE}")

if __name__ == "__main__":
    volumes = load_volumes()
    backups = backup_volumes(volumes)
    save_output(backups)
