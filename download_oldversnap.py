import os
import json
import urllib.request

# Папка, куда будут скачиваться jar-файлы
DOWNLOAD_FOLDER = "minecraft_versions_nonrelease"

# Типы версий, которые будут скачиваться (без релизов)
ALLOWED_TYPES = ["snapshot", "old_beta", "old_alpha", "indev", "infdev", "classic"]

# Скачиваем общий список всех версий с Mojang API
manifest_url = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
with urllib.request.urlopen(manifest_url) as response:
    manifest = json.loads(response.read().decode())

# Создаём папку, если её нет
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Перебираем все версии
for version in manifest["versions"]:
    version_id = version["id"]
    version_type = version["type"]

    if version_type not in ALLOWED_TYPES:
        continue  # Пропускаем релизы и другие

    print(f" Downloading {version_id} ({version_type})...")

    try:
        # Получаем ссылку на metadata JSON
        meta_url = version["url"]
        with urllib.request.urlopen(meta_url) as meta_response:
            meta_data = json.loads(meta_response.read().decode())

        # Получаем ссылку на client.jar
        client_url = meta_data["downloads"].get("client", {}).get("url")
        if not client_url:
            print(f" Missed: {version_id} (нет client.jar)")
            continue

        # Путь для сохранения
        output_path = os.path.join(DOWNLOAD_FOLDER, f"{version_id}.jar")

        # Скачиваем jar
        urllib.request.urlretrieve(client_url, output_path)
        print(f" Downloaded: {version_id}")

    except Exception as e:
        print(f"Error during downloading {version_id}: {e}")

print("\n All was downloaded!")
