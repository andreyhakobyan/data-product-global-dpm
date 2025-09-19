# SharedCTL

`sharedctl` is a lightweight CLI tool to fetch files, folders, or templates from a shared Git repository into your local project. It uses **Git sparse checkout** and a **local cache** to minimize downloads and speed up repeated fetches.  

It supports flexible copying:  

- Single file  
- Folder with contents  
- Folder contents only  

## Features

- Fetch **any file or folder** from a shared Git repo  
- Optionally copy **only the folder contents** (`--flatten`)  
- **Cache repository locally** to avoid repeated downloads  
- Works with **branches, tags, or commit SHA**  
- Cross-platform (Python 3.9+)  

## Usage

Basic command
```bash
python3 sharedctl/sharedctl.py fetch <path-in-repo> --to <destination> [--ref <branch|tag|SHA>] [--repo <git-url>] [--flatten]
```

- <path-in-repo> – path to file or folder in the shared repo
- --to – destination directory (default: .)
- --ref – branch, tag, or commit SHA (default: main)
- --repo – URL of the shared Git repository (default: your repo URL)
- --flatten – copy only folder contents, not the folder itself

### Examples

- Fetch a single file
```bash
python3 sharedctl/sharedctl.py fetch configs/app.yaml --to ./configs --repo https://github.com/andreyhakobyan/shared-repo.git
```
**Result:** `./configs/app.yaml`

- Fetch a folder with folder itself (default)
```bash
python3 sharedctl/sharedctl.py fetch templates/ --to ./project --repo https://github.com/andreyhakobyan/shared-repo.git
```
**Result:** `./project/templates/template.yml`

- Fetch folder contents only
```bash
python3 sharedctl/sharedctl.py fetch templates/ --to ./project --repo https://github.com/andreyhakobyan/shared-repo.git --flatten
```
**Result:** `./project/templates/template.yml`

- Fetch from a specific branch or tag
```bash
python3 sharedctl/sharedctl.py fetch templates/ --to . --ref dev-branch --repo https://github.com/andreyhakobyan/shared-repo.git
```
**Result:** `./project/template.yml`

### Notes
- The CLI stores a cached copy of the shared repo in: ~/.sharedctl_cache/repo
Repeated fetches are fast and do not re-clone the entire repository.
- To start fresh, delete the cache:

```bash
rm -rf ~/.sharedctl_cache
```