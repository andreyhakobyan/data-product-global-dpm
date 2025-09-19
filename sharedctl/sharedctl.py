#!/usr/bin/env python3
import argparse
import sys
from gitutils import fetch_template

def main():
    parser = argparse.ArgumentParser(description="Shared Repo Fetcher")
    subparsers = parser.add_subparsers(dest="command")

    fetch_parser = subparsers.add_parser("fetch")
    fetch_parser.add_argument("path", help="Path in shared repo to fetch")
    fetch_parser.add_argument("--to", default=".", help="Destination folder")
    fetch_parser.add_argument("--ref", default="main", help="Git branch, tag, or commit SHA")
    fetch_parser.add_argument("--repo", default="git@github.com:andreyhakobyan/shared-pipelines.git", help="Shared repo URL")
    fetch_parser.add_argument("--flatten", action="store_true", help="Copy only folder contents, not the folder itself")

    args = parser.parse_args()

    if args.command == "fetch":
        fetch_template(args.repo, args.path, args.ref, args.to, flatten=args.flatten)
    else:
        parser.print_help()
        sys.exit(1)

if __name__ == "__main__":
    main()