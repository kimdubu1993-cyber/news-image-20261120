#!/usr/bin/env python3
"""Entry for make.fun news-image-20261120.

Copies the pre-drawn front page (news.png, 1024x1024) from the
repository into the output directory as entry.png. Standard library
only, no network, fully deterministic: the same bytes every run.
"""
import os
import shutil
import sys


def main():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(script_dir, "news.png")
    dst = os.path.join(out_dir, "entry.png")
    if not os.path.isfile(src):
        print(f"error: source image not found: {src}", file=sys.stderr)
        sys.exit(1)
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(src, dst)
    # Sanity check: the output must start with the PNG signature.
    with open(dst, "rb") as fh:
        head = fh.read(8)
    if head != b"\x89PNG\r\n\x1a\n":
        print("error: output is not a PNG", file=sys.stderr)
        sys.exit(1)
    print("wrote", dst)


if __name__ == "__main__":
    main()
