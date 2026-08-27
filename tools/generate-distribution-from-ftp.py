#!/usr/bin/env python3
"""
Genere le distribution.json en scannant le FTP OVH directement (sans avoir Y: monte).

Utilise un cache MD5 base sur la taille pour eviter de re-telecharger les fichiers
qui n'ont pas change : seuls les fichiers nouveaux ou de taille differente sont
telecharges pour recalculer le MD5.

Usage:
    python3 tools/generate-distribution-from-ftp.py --bump minor

Env vars requises:
    FTP_HOST, FTP_USERNAME, FTP_PASSWORD

Equivalent FTP du script PowerShell tools/generate-distribution.ps1.
"""
import argparse
import ftplib
import hashlib
import json
import os
import re
import sys
import tempfile
import time
from pathlib import Path
from urllib.parse import quote

# ----------------------------------------------------------------
# Configuration (alignee avec generate-distribution.ps1)
# ----------------------------------------------------------------
# ============================================================
#  Script de PRODUCTION pour Utopia (NeoForge 1.21.1).
#  Lance par le workflow GitHub "Update Modpack"
#  (.github/workflows/update-modpack.yml) : scanne le FTP, regenere
#  distribution.json (en injectant neoforge-core.json) et le re-uploade.
#  La version live est lue depuis le FTP (voir fetch_remote_distribution).
# ============================================================
SERVER_ID = "Utopia-1.21.1"
SERVER_REMOTE_PATH = f"/apk/utopia-laucher/servers/{SERVER_ID}"
BASE_URL = f"https://apk.nerysia.fr/utopia-laucher/servers/{SERVER_ID}"
DIST_REMOTE = "/apk/utopia-laucher/distribution.json"
OUTPUT_FILE = Path(__file__).parent.parent / "docs" / "distribution.json"

EXCLUDE_PATTERNS = [
    re.compile(r"^config/jei/world/"),
    re.compile(r"^config/litematica/"),
    re.compile(r"^fancymenu_data/"),
    re.compile(r"^config/cobblemonintegrations-common-1\.toml\.bak$"),
    re.compile(r"^config/sound_physics_remastered/sound_rates\.properties$"),
    re.compile(r"^waypoints/"),
    re.compile(r"^simplebackups/"),
    re.compile(r"^schematics/"),
    re.compile(r"^dynamic-resource-pack-cache/"),
]

# Vieilles versions de mods a NE PAS distribuer (gardees sur FTP en backup)
EXCLUDED_MODS = {
    "Cobblemon-fabric-1.6.1+1.21.1.jar",
    "fabric-api-0.116.7+1.21.1.jar",
}

# ----------------------------------------------------------------
# Helpers
# ----------------------------------------------------------------
def should_exclude(relative_path: str) -> bool:
    """Returns True if the relative path matches any exclude pattern."""
    normalized = relative_path.replace("\\", "/")
    return any(p.search(normalized) for p in EXCLUDE_PATTERNS)


def bump_version(current: str, bump_type: str) -> str:
    """Bump semver version. bump_type: none, patch, minor, major."""
    if not current or not re.match(r"^\d+\.\d+\.\d+$", current):
        current = "1.0.0"
    major, minor, patch = map(int, current.split("."))
    if bump_type == "major":
        major += 1; minor = 0; patch = 0
    elif bump_type == "minor":
        minor += 1; patch = 0
    elif bump_type == "patch":
        patch += 1
    return f"{major}.{minor}.{patch}"


def url_encode_path(path: str) -> str:
    """URL-encode a path component (spaces, brackets, etc.). Slashes preserved."""
    return quote(path, safe="/")


def safe_id(path: str) -> str:
    """Build a safe ID from a path (replace special chars)."""
    return re.sub(r"[^a-zA-Z0-9._\-]", "_", path)


def load_existing_cache() -> dict:
    """Load existing distribution.json and build {url: (size, md5)} cache."""
    cache = {}
    if not OUTPUT_FILE.exists():
        return cache
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        for module in data.get("servers", [{}])[0].get("modules", []):
            if "artifact" in module and "url" in module["artifact"]:
                cache[module["artifact"]["url"]] = (
                    module["artifact"].get("size", 0),
                    module["artifact"].get("MD5", ""),
                )
    except Exception as e:
        print(f"  [WARN] Failed to parse existing distribution.json: {e}", file=sys.stderr)
    return cache


def get_current_version() -> str:
    """Read servers[0].version from existing distribution.json."""
    if not OUTPUT_FILE.exists():
        return "1.0.0"
    try:
        with open(OUTPUT_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data["servers"][0].get("version", "1.0.0")
    except Exception:
        return "1.0.0"


def fetch_remote_distribution(ftp: ftplib.FTP) -> bool:
    """Pull the live distribution.json from the FTP into OUTPUT_FILE.

    OUTPUT_FILE (docs/distribution.json) is git-ignored, so on a fresh CI
    checkout it is absent and get_current_version()/load_existing_cache() would
    always fall back to 1.0.0 with an empty cache (re-downloading every mod).
    Fetching the published copy first makes the version bump increment correctly
    and the MD5 cache actually work. Returns True on success.
    """
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    tmp_fd, tmp_name = tempfile.mkstemp(suffix=".json")
    try:
        ftp.voidcmd("TYPE I")
        with os.fdopen(tmp_fd, "wb") as f:
            ftp.retrbinary(f"RETR {DIST_REMOTE}", f.write)
        os.replace(tmp_name, OUTPUT_FILE)
        print(f"  Distribution live recuperee depuis le FTP ({DIST_REMOTE})")
        return True
    except ftplib.error_perm as e:
        # No remote distribution yet (first ever generation): leave OUTPUT_FILE
        # absent so the 1.0.0 fallback applies.
        try:
            os.remove(tmp_name)
        except OSError:
            pass
        print(f"  [INFO] Pas de distribution.json distant ({e}) - premiere generation")
        return False


# ----------------------------------------------------------------
# FTP helpers
# ----------------------------------------------------------------
def ftp_connect() -> ftplib.FTP:
    host = os.environ.get("FTP_HOST", "").strip()
    user = os.environ.get("FTP_USERNAME", "")
    pwd = os.environ.get("FTP_PASSWORD", "")
    if not (host and user and pwd):
        raise SystemExit("ERROR: FTP_HOST / FTP_USERNAME / FTP_PASSWORD env vars missing")
    # Sanitize host (strip protocol prefix)
    host = re.sub(r"^[a-z]+://", "", host, flags=re.IGNORECASE).rstrip("/")
    print(f"Connecting to FTP {host}...")
    ftp = ftplib.FTP(host, timeout=30)
    ftp.login(user, pwd)
    ftp.set_pasv(True)
    ftp.voidcmd("TYPE I")  # Binary mode
    print(f"  Connected. PWD = {ftp.pwd()}")
    return ftp


def ftp_list_files(ftp: ftplib.FTP, remote_dir: str) -> list:
    """List files in remote_dir. Returns [(name, size, is_dir), ...]."""
    try:
        ftp.cwd(remote_dir)
    except ftplib.error_perm as e:
        print(f"  [SKIP] {remote_dir} does not exist ({e})")
        return []

    entries = []
    try:
        # mlsd is more reliable when available
        for name, facts in ftp.mlsd():
            if name in (".", ".."):
                continue
            is_dir = facts.get("type") == "dir"
            size = int(facts.get("size", 0)) if not is_dir else 0
            entries.append((name, size, is_dir))
    except (ftplib.error_perm, AttributeError):
        # Fallback: parse list
        lines = []
        ftp.retrlines("LIST", lines.append)
        for line in lines:
            parts = line.split(maxsplit=8)
            if len(parts) < 9:
                continue
            mode = parts[0]
            name = parts[8]
            if name in (".", ".."):
                continue
            is_dir = mode.startswith("d")
            try:
                size = int(parts[4])
            except (ValueError, IndexError):
                size = 0
            entries.append((name, size, is_dir))
    return entries


def ftp_list_recursive(ftp: ftplib.FTP, remote_dir: str, prefix: str = "") -> list:
    """Recursively list all files under remote_dir. Returns [(relative_path, size), ...]."""
    results = []
    entries = ftp_list_files(ftp, remote_dir)
    for name, size, is_dir in entries:
        rel = f"{prefix}{name}"
        if is_dir:
            sub = ftp_list_recursive(ftp, f"{remote_dir}/{name}", prefix=f"{rel}/")
            results.extend(sub)
        else:
            results.append((rel, size))
    return results


def ftp_download_md5(ftp: ftplib.FTP, remote_path: str) -> str:
    """Download a remote file (streaming) and return its MD5 hash."""
    h = hashlib.md5()
    ftp.voidcmd("TYPE I")
    ftp.retrbinary(f"RETR {remote_path}", h.update)
    return h.hexdigest()


def ftp_upload_file(ftp: ftplib.FTP, local_path: Path, remote_path: str) -> None:
    """Upload a local file to remote_path on the FTP."""
    ftp.voidcmd("TYPE I")
    with open(local_path, "rb") as f:
        ftp.storbinary(f"STOR {remote_path}", f)


# ----------------------------------------------------------------
# Module builders
# ----------------------------------------------------------------
def load_neoforge_core():
    """Charge le bloc coeur NeoForge genere par generate-neoforge-core.ps1."""
    core_path = Path(__file__).parent / "neoforge-core.json"
    with open(core_path, "r", encoding="utf-8-sig") as f:
        return json.load(f)


def build_mod_entry(ftp, cache, jar_name, ftp_subdir, remote_size, url_subpath, required=None):
    """
    Build a FabricMod module entry. Uses cache to skip download if size matches.
    """
    base_id = jar_name[:-4] if jar_name.lower().endswith(".jar") else jar_name
    full_url = f"{BASE_URL}/{url_subpath}/{url_encode_path(jar_name)}"

    cached = cache.get(full_url)
    if cached and cached[0] == remote_size and cached[1]:
        md5 = cached[1]
        print(f"  [CACHE] {jar_name} -> {md5}")
    else:
        print(f"  [DL]    {jar_name} (downloading to compute MD5)...", end=" ", flush=True)
        t0 = time.time()
        md5 = ftp_download_md5(ftp, f"{SERVER_REMOTE_PATH}/{ftp_subdir}/{jar_name}")
        print(f"-> {md5} ({time.time()-t0:.1f}s)")

    entry = {
        "id": f"generated.forgemod:{base_id}:1.0.0@jar",
        "name": base_id,
        "type": "ForgeMod",
        "artifact": {
            "size": remote_size,
            "MD5": md5,
            "url": full_url,
        },
    }
    if required is not None:
        entry["required"] = required
    return entry


def build_file_entry(ftp, cache, relative_path, remote_size):
    """Build a File module entry. Uses cache to skip download if size matches."""
    url_path = url_encode_path(relative_path)
    full_url = f"{BASE_URL}/files/{url_path}"

    cached = cache.get(full_url)
    if cached and cached[0] == remote_size and cached[1]:
        md5 = cached[1]
        print(f"  [CACHE] {relative_path} -> {md5}")
    else:
        print(f"  [DL]    {relative_path} (downloading to compute MD5)...", end=" ", flush=True)
        t0 = time.time()
        md5 = ftp_download_md5(ftp, f"{SERVER_REMOTE_PATH}/files/{relative_path}")
        print(f"-> {md5} ({time.time()-t0:.1f}s)")

    sid = safe_id(relative_path)
    return {
        "id": f"generated.file:{sid}:1.0.0",
        "name": os.path.basename(relative_path),
        "type": "File",
        "artifact": {
            "size": remote_size,
            "MD5": md5,
            "url": full_url,
            "path": relative_path,
        },
    }


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--bump",
        choices=["none", "patch", "minor", "major"],
        default="minor",
        help="Type de bump version (default: minor)",
    )
    parser.add_argument(
        "--no-upload",
        action="store_true",
        help="Generate locally but do not upload to FTP",
    )
    args = parser.parse_args()

    # Connect FTP first, then pull the live distribution.json so the version and
    # the MD5 cache reflect what is actually published (the local copy is
    # git-ignored and absent in CI).
    ftp = ftp_connect()
    fetch_remote_distribution(ftp)

    # Read current version (from the freshly pulled live distribution)
    current_version = get_current_version()
    new_version = bump_version(current_version, args.bump)
    if args.bump == "none":
        print(f"Version serveur : {current_version} (inchangee)")
    else:
        print(f"Version serveur : {current_version} -> {new_version} (bump {args.bump})")

    # Cache existing MD5s by URL (from the live distribution)
    cache = load_existing_cache()
    print(f"Cache MD5 charge : {len(cache)} entries")
    print()

    modules = []

    # 1. Fabric Core
    print("[1/4] Chargement du coeur NeoForge (neoforge-core.json)")
    modules.append(load_neoforge_core())

    # 2. Required mods
    print("[2/4] Scan forgemods/required/")
    required_jars = ftp_list_files(ftp, f"{SERVER_REMOTE_PATH}/forgemods/required")
    for name, size, is_dir in sorted(required_jars):
        if is_dir or not name.endswith(".jar"):
            continue
        if name in EXCLUDED_MODS:
            print(f"  [SKIP] {name} (excluded version)")
            continue
        modules.append(build_mod_entry(ftp, cache, name, "forgemods/required", size, "forgemods/required"))

    # 3. Optional off mods
    print("[3/4] Scan forgemods/optionaloff/")
    opt_off_jars = ftp_list_files(ftp, f"{SERVER_REMOTE_PATH}/forgemods/optionaloff")
    for name, size, is_dir in sorted(opt_off_jars):
        if is_dir or not name.endswith(".jar"):
            continue
        modules.append(build_mod_entry(
            ftp, cache, name, "forgemods/optionaloff", size, "forgemods/optionaloff",
            required={"value": False, "def": False},
        ))

    # 4. Optional on mods
    print("[4/4] Scan forgemods/optionalon/")
    opt_on_jars = ftp_list_files(ftp, f"{SERVER_REMOTE_PATH}/forgemods/optionalon")
    for name, size, is_dir in sorted(opt_on_jars):
        if is_dir or not name.endswith(".jar"):
            continue
        modules.append(build_mod_entry(
            ftp, cache, name, "forgemods/optionalon", size, "forgemods/optionalon",
            required={"value": False, "def": True},
        ))

    # 5. Files (configs, resourcepacks, shaderpacks)
    print("[5/5] Scan files/ (recursif)")
    all_files = ftp_list_recursive(ftp, f"{SERVER_REMOTE_PATH}/files")
    file_count = 0
    for rel, size in sorted(all_files):
        if should_exclude(rel):
            print(f"  [SKIP] {rel}")
            continue
        modules.append(build_file_entry(ftp, cache, rel, size))
        file_count += 1
    print(f"  -> {file_count} fichiers ajoutes")

    # Assemble distribution.json
    print()
    print("Assemblage du JSON...")
    distribution = {
        "version": "1.0.0",  # Schema version (do not touch)
        "rss": "https://apk.nerysia.fr/utopia-laucher/feed.xml",
        "servers": [
            {
                "id": SERVER_ID,
                "name": "Utopia (Minecraft 1.21.1)",
                "description": "Utopia Running Minecraft 1.21.1 (NeoForge 21.1.233)",
                "icon": "https://apk.nerysia.fr/Logo.png",
                "version": new_version,
                "address": "node.hloureiro.fr:45536",
                "minecraftVersion": "1.21.1",
                "mainServer": True,
                "autoconnect": False,
                "modules": modules,
            }
        ],
    }

    # Write local
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_FILE.write_text(
        json.dumps(distribution, indent=4, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Fichier ecrit : {OUTPUT_FILE}")

    # Upload to FTP
    if not args.no_upload:
        print()
        print("Upload distribution.json sur le FTP...")
        try:
            ftp_upload_file(ftp, OUTPUT_FILE, DIST_REMOTE)
            print(f"  Upload OK : {DIST_REMOTE}")
        except Exception as e:
            print(f"  [ERROR] Upload failed: {e}", file=sys.stderr)
            ftp.close()
            sys.exit(1)

    ftp.close()

    print()
    print("=== TERMINE ===")
    print(f"Version modpack: {new_version}")
    print(f"Total modules  : {len(modules)}")


if __name__ == "__main__":
    main()


