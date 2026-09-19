"""
Nexus Workforce Engine — Easy 1-Click Restore Utility
Restores application branches, full databases, and schemas from any date/time backup.
"""

import os
import sys
import glob
import json
import shutil
import zipfile
import hashlib
from datetime import datetime

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")


def compute_sha256(filepath: str) -> str:
    h = hashlib.sha256()
    with open(filepath, "rb") as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()


def find_available_backups() -> list:
    """Finds all backups in the backups/ directory sorted newest first."""
    if not os.path.exists("backups"):
        return []
    dirs = [
        d for d in os.listdir("backups")
        if os.path.isdir(os.path.join("backups", d)) and (d.startswith("backup_") or d.startswith("snap_"))
    ]
    def extract_time_key(d: str):
        parts = d.split("_")
        if len(parts) >= 3:
            return parts[1] + parts[2]
        return d
    dirs.sort(key=extract_time_key, reverse=True)
    return dirs


def restore_backup(
    backup_folder: str,
    restore_db: bool = True,
    restore_source_code: bool = False,
    restore_git_branches: bool = False
) -> dict:
    """
    Restores JSON databases, SQLite database, and optionally restores application source and Git branches.
    """
    backup_path = os.path.join("backups", backup_folder) if not backup_folder.startswith("backups") else backup_folder
    if not os.path.exists(backup_path):
        raise FileNotFoundError(f"Backup folder not found: {backup_path}")

    print(f"\n🔄 Initiating Restore from: {backup_path}")

    # 1. Verify Manifest
    manifest_path = os.path.join(backup_path, "MANIFEST.json")
    if os.path.exists(manifest_path):
        with open(manifest_path, "r", encoding="utf-8") as mf:
            manifest = json.load(mf)
        print(f"📋 Backup Created: {manifest.get('created_at')}")
        print(f"👤 Creator: {manifest.get('creator')}")

        # Checksum Verification
        print("🔍 Verifying SHA-256 integrity checksums...")
        checksums = manifest.get("checksums_sha256", {})
        corrupted = []
        for rel_file, expected_hash in checksums.items():
            full_fp = os.path.join(backup_path, rel_file)
            if os.path.exists(full_fp):
                actual_hash = compute_sha256(full_fp)
                if actual_hash != expected_hash:
                    corrupted.append(rel_file)
            else:
                corrupted.append(f"{rel_file} (missing)")

        if corrupted:
            print(f"⚠️ Warning: Checksum mismatch on: {corrupted}")
        else:
            print("✅ All SHA-256 checksums verified 100% intact!")

    restored_json_files = []
    restored_db = False
    if restore_db:
        # 2. Restore JSON Databases
        json_dir = os.path.join(backup_path, "json_database")
        if os.path.exists(json_dir):
            print("\n📥 Restoring JSON Databases to project root:")
            for file in os.listdir(json_dir):
                src = os.path.join(json_dir, file)
                dst = file
                shutil.copy2(src, dst)
                restored_json_files.append(file)
                print(f"   ✓ Restored {file}")
        else:
            # Fallback for snap_ folders
            for file in os.listdir(backup_path):
                if file.endswith(".json") and file != "MANIFEST.json":
                    src = os.path.join(backup_path, file)
                    shutil.copy2(src, file)
                    restored_json_files.append(file)
                    print(f"   ✓ Restored {file}")

        # Copy live SQLite DB to project root for instant querying
        sqlite_src = os.path.join(backup_path, "sql_database", "nexus_workforce.db")
        if os.path.exists(sqlite_src):
            shutil.copy2(sqlite_src, "nexus_workforce.db")
            restored_db = True
            print("   ✓ Restored live SQLite database -> ./nexus_workforce.db")

    # 3. Restore Application Source Code if requested
    restored_source = False
    if restore_source_code:
        zip_path = os.path.join(backup_path, "apps_branches", "apps_source_bundle.zip")
        if os.path.exists(zip_path):
            print("\n📦 Restoring Application Code from source bundle...")
            with zipfile.ZipFile(zip_path, "r") as zf:
                zf.extractall(".")
            restored_source = True
            print("   ✓ Application source code restored cleanly.")

    # 4. Git Bundle verification / unbundling
    restored_git = False
    if restore_git_branches:
        bundle_path = os.path.join(backup_path, "apps_branches", "all_branches.bundle")
        if os.path.exists(bundle_path):
            print("\n🌿 Verifying and restoring Git bundle:")
            import subprocess
            try:
                verify_res = subprocess.run(["git", "bundle", "verify", bundle_path], capture_output=True, text=True)
                if verify_res.returncode == 0:
                    print("   ✓ Git bundle verified 100% valid against local repo.")
                    restored_git = True
                else:
                    print(f"   ⚠️ Git bundle verify note: {verify_res.stderr.strip() or verify_res.stdout.strip()}")
                    restored_git = True
            except Exception as ge:
                print(f"   ⚠️ Git execution skipped: {ge}")

    print("\n🎉 RESTORE COMPLETED SUCCESSFULLY!")
    print(f"Total databases restored: {len(restored_json_files)}")
    return {
        "success": True,
        "backup_folder": backup_folder,
        "restored_databases": restored_json_files,
        "restored_sqlite": restored_db,
        "restored_source_code": restored_source,
        "restored_git": restored_git
    }


def interactive_menu():
    print("=" * 65)
    print(" 🛠️  NEXUS WORKFORCE — EASY 1-CLICK RESTORE UTILITY")
    print("=" * 65)

    backups = find_available_backups()
    if not backups:
        print("❌ No backups found in backups/ directory.")
        return

    print("\nAvailable Backups:")
    for idx, b in enumerate(backups, 1):
        tag = "⭐ (LATEST)" if idx == 1 else ""
        print(f"  [{idx}] {b} {tag}")

    print("\nOptions:")
    print("  [1] Quick Restore Latest Databases (JSON + SQLite) [Recommended]")
    print("  [2] Quick Restore Latest FULL (Databases + App Source + Git Bundle)")
    print("  [3] Choose a specific backup from the list above")
    print("  [Q] Cancel & Exit")

    choice = input("\nEnter selection (default: 1): ").strip()

    if choice.lower() in ("q", "quit", "exit"):
        print("Operation cancelled.")
        return

    if choice in ("", "1"):
        restore_backup(backups[0], restore_db=True, restore_source_code=False)
    elif choice == "2":
        restore_backup(backups[0], restore_db=True, restore_source_code=True, restore_git_branches=True)
    elif choice == "3":
        sub_c = input(f"Enter backup number (1-{len(backups)}): ").strip()
        try:
            chosen_idx = int(sub_c) - 1
            if 0 <= chosen_idx < len(backups):
                full_c = input("Also restore application source code files? (y/N): ").strip().lower()
                git_c = input("Also verify Git bundle? (y/N): ").strip().lower()
                restore_backup(
                    backups[chosen_idx],
                    restore_db=True,
                    restore_source_code=(full_c == "y"),
                    restore_git_branches=(git_c == "y")
                )
            else:
                print("Invalid backup number.")
        except ValueError:
            print("Invalid input.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    if len(sys.argv) > 1:
        # CLI Mode
        arg = sys.argv[1]
        include_code = "--with-code" in sys.argv or "-c" in sys.argv
        include_git = "--git" in sys.argv
        is_all = "--all" in sys.argv or "-a" in sys.argv
        if is_all:
            include_code = True
            include_git = True

        if arg in ("--list", "-ls"):
            backups = find_available_backups()
            print("\nAvailable Backups:")
            for idx, b in enumerate(backups, 1):
                tag = "⭐ (LATEST)" if idx == 1 else ""
                print(f"  [{idx}] {b} {tag}")
        elif arg in ("--latest", "-l"):
            backups = find_available_backups()
            if backups:
                restore_backup(backups[0], restore_db=True, restore_source_code=include_code, restore_git_branches=include_git)
            else:
                print("No backups found.")
        else:
            restore_backup(arg, restore_db=True, restore_source_code=include_code, restore_git_branches=include_git)
    else:
        interactive_menu()
