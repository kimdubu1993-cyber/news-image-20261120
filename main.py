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
    in_dir = os.environ.get("MAKEFUN_INPUT_DIR", "/input")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    src = os.path.join(in_dir, "news.png")
    dst = os.path.join(out_dir, "entry.png")
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
