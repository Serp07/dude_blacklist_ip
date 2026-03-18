import routeros_api
import subprocess
import os
import hashlib

ROUTER_IP = "192.168.3.1"
USERNAME = "baboon"
PASSWORD = "Kompass777@"
PORT = 8728

ADDRESS_LISTS = [
    "Dude_blacklist",
    "Black List (Port Scanner WAN)"
]

OUTPUT_FILE = "/root/scripts/dude_blacklist_ip/dude_blacklist.rsc"
REPO_PATH = "/root/scripts/dude_blacklist_ip"


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

    ips = set()

    for lst in ADDRESS_LISTS:
        data = addr_list.get(list=lst)

        for entry in data:
            if "address" in entry:
                ips.add(entry["address"])

    connection.disconnect()

    return sorted(ips)


def hash_file(path):

    if not os.path.exists(path):
        return None

    h = hashlib.sha256()

    with open(path, "rb") as f:
        h.update(f.read())

    return h.hexdigest()


def generate_rsc(ips):

    lines = []

    lines.append('/ip firewall address-list remove [find list=Dude_blacklist]')
    lines.append('/ip firewall address-list')

    for ip in ips:
        lines.append(f'add list=Dude_blacklist address={ip}')

    return "\n".join(lines) + "\n"


def write_file(ips):

    new_content = generate_rsc(ips)

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

    # перевірка чи є зміни
    result = subprocess.run(
        ["git", "-C", REPO_PATH, "diff", "--cached", "--quiet"]
    )

    if result.returncode == 0:
        print("No git changes")
        return

    subprocess.run(
        ["git", "-C", REPO_PATH, "commit", "-m", "update blacklist"]
    )
    subprocess.run(["git", "-C", REPO_PATH, "push"])


def main():

    print("Fetching blacklist...")

    ips = get_blacklist()

    print(f"Total IPs: {len(ips)}")

    changed = write_file(ips)

    if changed:
        git_push()
        print("Blacklist updated and pushed to git")
    else:
        print("No changes")


if __name__ == "__main__":
    main()
