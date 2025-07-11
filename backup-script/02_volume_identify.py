import oci
import json
import sys

STATE_FILE = "state.json"
OUTPUT_FILE = "volumes.json"


def load_state():
    try:
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print("❌ state.json not found. Run instance_select.py first.")
        sys.exit(1)


def get_attached_volumes(instance_id, availability_domain, compartment_id):
    config = oci.config.from_file()
    compute = oci.core.ComputeClient(config)
    block = oci.core.BlockstorageClient(config)

    print("🔍 Looking up boot volume attachments...")

    boot_attachments = compute.list_boot_volume_attachments(
        compartment_id=compartment_id,
        availability_domain=availability_domain
    ).data

    boot_vol = next(
        (
            b for b in boot_attachments
            if b.instance_id == instance_id and b.lifecycle_state == "ATTACHED"
        ),
        None
    )

    if not boot_vol:
        print("❌ No boot volume currently attached to the instance.")
        sys.exit(1)

    print(f"✅ Boot Volume OCID: {boot_vol.boot_volume_id}")

    print("🔍 Looking up block volume attachments...")
    volume_attachments = compute.list_volume_attachments(
        compartment_id=compartment_id
    ).data

    seen = set()
    block_volumes = []

    for v in volume_attachments:
        if (
            v.instance_id == instance_id
            and v.lifecycle_state == "ATTACHED"
            and v.volume_id not in seen
        ):
            vol_data = {
                "volume_id": v.volume_id,
                "display_name": block.get_volume(v.volume_id).data.display_name
            }
            block_volumes.append(vol_data)
            seen.add(v.volume_id)

    if block_volumes:
        for vol in block_volumes:
            print(f"✅ Block Volume: {vol['display_name']} ({vol['volume_id']})")
    else:
        print("ℹ️ No block volumes attached to the instance.")

    return {
        "boot_volume_id": boot_vol.boot_volume_id,
        "boot_attachment_id": boot_vol.id,
        "block_volumes": block_volumes
    }


def save_output(volumes):
    with open(OUTPUT_FILE, "w") as f:
        json.dump(volumes, f, indent=2)
    print(f"💾 Volume info saved to {OUTPUT_FILE}")


if __name__ == "__main__":
    state = load_state()
    volumes = get_attached_volumes(
        instance_id=state["instance_id"],
        availability_domain=state["availability_domain"],
        compartment_id=state["compartment_id"]
    )
    save_output(volumes)
