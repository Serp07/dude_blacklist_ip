import shutil
import os

SOURCE_FILE = "/root/scripts/dude_blacklist_ip/dude_blacklist.rsc"
DEST_FILE = "/root/scripts/bl_mik/dude_blacklist.rsc"


def count_ips(file_path):

    if not os.path.exists(file_path):
        print("Source file not found")
        return 0

    count = 0

    with open(file_path, "r") as f:
        for line in f:
            if line.strip().startswith("add list="):
                count += 1

    return count


def copy_if_not_empty():

    ip_count = count_ips(SOURCE_FILE)

    print(f"IPs in file: {ip_count}")

    if ip_count < 500:
        print("Too few IPs. Copy skipped.")
        return

    shutil.copy2(SOURCE_FILE, DEST_FILE)

    print("File copied successfully")


if __name__ == "__main__":
    copy_if_not_empty()
