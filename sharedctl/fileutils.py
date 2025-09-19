from pathlib import Path
import shutil

def copy_dir(src: Path, dst: Path):
    dst.mkdir(parents=True, exist_ok=True)
    if src.is_file():
        shutil.copy2(src, dst / src.name)
        return
    for item in src.iterdir():
        s = item
        d = dst / item.name
        if item.is_dir():
            copy_dir(s, d)
        else:
            shutil.copy2(s, d)