import json
import platform
import subprocess
import sys
import os
from pathlib import Path
import urllib.request

SOURCE_URL = "https://raw.githubusercontent.com/rompelhd/ZeroBrave/refs/heads/main/policies.json"


def require_root():
    if os.geteuid() != 0:
        print("This script must be run as root (use sudo).")
        sys.exit(1)


def get_policy_path() -> Path:
    system = platform.system().lower()
    if system == "windows":
        return Path(
            r"C:\Program Files\BraveSoftware\Brave-Browser\Application\policy\managed\policies.json"
        )
    elif system == "linux":
        return Path("/etc/brave/policies/managed/policies.json")
    else:
        raise RuntimeError(f"Unsupported operating system: {system}")


def ensure_dir(path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)


def download_json(url: str) -> dict:
    with urllib.request.urlopen(url) as resp:
        if resp.status != 200:
            raise RuntimeError(f"Download failed: HTTP {resp.status}")
        data = resp.read()
    return json.loads(data.decode("utf-8"))


def write_json(path: Path, data: dict):
    ensure_dir(path)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"Policies written to: {path}")


def is_brave_flatpak() -> bool:
    try:
        result = subprocess.run(
            ["flatpak", "info", "com.brave.Browser"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        return result.returncode == 0
    except FileNotFoundError:
        return False


def ask_yes_no(msg: str) -> bool:
    return input(f"{msg} [y/N]: ").strip().lower() == "y"


def grant_flatpak_permission():
    subprocess.run(
        [
            "flatpak",
            "override",
            "--system",
            "com.brave.Browser",
            "--filesystem=/etc/brave",
        ],
        check=True,
    )


def main():
    system = platform.system().lower()

    if system == "linux":
        require_root()

    policies = download_json(SOURCE_URL)
    target_path = get_policy_path()
    write_json(target_path, policies)

    if system == "linux" and is_brave_flatpak():
        print("Brave is installed as a Flatpak.")
        if ask_yes_no(
            "Grant Flatpak access to /etc/brave so policies can be applied?"
        ):
            grant_flatpak_permission()
            print("Permission granted. Please restart Brave.")
        else:
            print(
                "Without this permission, Brave Flatpak will not read system policies."
            )


if __name__ == "__main__":
    main()
