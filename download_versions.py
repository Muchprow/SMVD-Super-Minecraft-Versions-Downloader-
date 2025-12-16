import os
import json
import urllib.request

VERSIONS_DIR = "minecraft_versions"
os.makedirs(VERSIONS_DIR, exist_ok=True)

with urllib.request.urlopen("https://piston-meta.mojang.com/mc/game/version_manifest.json") as url:
    data = json.loads(url.read().decode())

for version in data["versions"]:
    if version["type"] == "release":
        version_id = version["id"]
        if version_id > "1.21.11":
            continue
        print(f" Downloading {version_id}...")
        version_url = version["url"]
        with urllib.request.urlopen(version_url) as v_url:
            version_data = json.loads(v_url.read().decode())
            client_url = version_data["downloads"]["client"]["url"]
            client_path = os.path.join(VERSIONS_DIR, f"{version_id}.jar")
            urllib.request.urlretrieve(client_url, client_path)

print("\n All was downloaded!")
