import os
import subprocess
from pathlib import Path
from fileutils import copy_dir

CACHE_DIR = Path.home() / ".sharedctl_cache"

def run(cmd, cwd=None):
    """Run a shell command and raise error if it fails"""
    result = subprocess.run(cmd, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if result.returncode != 0:
        raise RuntimeError(f"Command failed: {' '.join(cmd)}\n{result.stderr.decode()}")
    return result.stdout.decode()

def fetch_template(repo, path, ref, dst, flatten=False):
    """
    Fetch a file or folder from a shared repo using sparse checkout.

    Args:
        repo (str): Git repository URL
        path (str): Path inside repo to fetch (file or folder)
        ref (str): Branch, tag, or commit SHA
        dst (str or Path): Destination folder
        flatten (bool): If True, copy only folder contents (no top-level folder)
    """
    cache_repo = CACHE_DIR / "repo"
    os.makedirs(CACHE_DIR, exist_ok=True)

    # Clone repo into cache if it doesn't exist
    if not cache_repo.exists():
        run(["git", "clone", "--filter=blob:none", "--no-checkout", repo, str(cache_repo)])

    # Enable sparse checkout
    run(["git", "-C", str(cache_repo), "config", "core.sparseCheckout", "true"])
    run(["git", "-C", str(cache_repo), "sparse-checkout", "init", "--cone"])
    run(["git", "-C", str(cache_repo), "sparse-checkout", "set", path])

    # Fetch and checkout
    run(["git", "-C", str(cache_repo), "fetch", "origin", ref, "--depth=1"])
    run(["git", "-C", str(cache_repo), "checkout", "FETCH_HEAD"])

    # Source path in cache
    src_path = cache_repo / path
    dst_path = Path(dst)

    if not src_path.exists():
        raise FileNotFoundError(f"{path} does not exist in shared repo")

    # Flexible copying
    if src_path.is_file():
        # Single file → copy to destination
        copy_dir(src_path, dst_path)
    elif flatten:
        # Folder contents only → copy all children directly to dst
        for item in src_path.iterdir():
            copy_dir(item, dst_path / item.name)
    else:
        # Folder with folder itself → dst/folder_name
        dst_path = dst_path / src_path.name
        copy_dir(src_path, dst_path)

    print(f"Fetched {path} to {dst_path}")