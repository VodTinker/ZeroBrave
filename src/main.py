import json
import platform
from pathlib import Path
import urllib.request

SOURCE_URL = "https://raw.githubusercontent.com/rompelhd/ZeroBrave/refs/heads/main/policies.json"

def get_policy_path() -> Path:
    system = platform.system().lower()
    if system == "windows":
        return Path(r"C:\Program Files\BraveSoftware\Brave-Browser\Application\policy\managed\policies.json")
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

def main():
    policies = download_json(SOURCE_URL)
    target_path = get_policy_path()
    write_json(target_path, policies)

if __name__ == "__main__":
    main()
