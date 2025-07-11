import oci
import json
import sys

STATE_FILE = "state.json"


def save_instance_to_state(instance):
    with open(STATE_FILE, "w") as f:
        json.dump({
            "instance_id": instance.id,
            "display_name": instance.display_name,
            "availability_domain": instance.availability_domain,
            "compartment_id": instance.compartment_id
        }, f, indent=2)


def list_instances(compartment_id):
    config = oci.config.from_file()
    compute = oci.core.ComputeClient(config)

    print("🔍 Fetching instances in compartment...")
    instances = compute.list_instances(compartment_id).data

    instances = [i for i in instances if i.lifecycle_state != "TERMINATED"]

    if not instances:
        print("❌ No running or stopped instances found.")
        sys.exit(1)

    for idx, instance in enumerate(instances, start=1):
        print(f"[{idx}] {instance.display_name} (State: {instance.lifecycle_state})")

    choice = input("👉 Select an instance number: ")

    try:
        selected = instances[int(choice) - 1]
        print(f"✅ Selected: {selected.display_name}")
        save_instance_to_state(selected)
    except (IndexError, ValueError):
        print("❌ Invalid selection.")
        sys.exit(1)


if __name__ == "__main__":
    COMPARTMENT_ID = "YourCompartmentID"
    list_instances(COMPARTMENT_ID)
