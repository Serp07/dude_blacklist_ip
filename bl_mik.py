import routeros_api
import subprocess
import os
import hashlib

ROUTER_IP = "192.168.3.1"
USERNAME = "baboon"
PASSWORD = "Kompass777@"
PORT = 8728

ADDRESS_LIST = "Dude_blacklist"

OUTPUT_FILE = "/root/scripts/bl_mik/Dude_blacklist.rsc"
REPO_PATH = "/root/scripts/bl_mik/"


def get_blacklist():

    connection = routeros_api.RouterOsApiPool(
        ROUTER_IP,
        username=USERNAME,
        password=PASSWORD,
        port=PORT,
        plaintext_login=True
    )

    api = connection.get_api()

    addr_list = api.get_resource('/ip/firewall/address-list')

    data = addr_list.get(list=ADDRESS_LIST)

    connection.disconnect()

    ips = []

    for entry in data:
        ips.append(entry["address"])

    ips = sorted(list(set(ips)))

    return ips


def hash_file(path):

    if not os.path.exists(path):
        return None

    h = hashlib.sha256()

    with open(path, "rb") as f:
        h.update(f.read())

    return h.hexdigest()


def write_file(ips):

    new_content = "\n".join(ips) + "\n"

    new_hash = hashlib.sha256(new_content.encode()).hexdigest()
    old_hash = hash_file(OUTPUT_FILE)

    if new_hash == old_hash:
        print("Blacklist unchanged")
        return False

    with open(OUTPUT_FILE, "w") as f:
        f.write(new_content)

    return True


def git_push():

    subprocess.run(["git", "-C", REPO_PATH, "add", "."])
    subprocess.run(["git", "-C", REPO_PATH, "commit", "-m", "update Dude blacklist"])
    subprocess.run(["git", "-C", REPO_PATH, "push"])


def main():

    ips = get_blacklist()

    changed = write_file(ips)

    if changed:
        git_push()
        print("Blacklist updated and pushed to git")
    else:
        print("No changes")


if __name__ == "__main__":
    main()
