# news-image-20261119 entry (Python 3.13, standard library only).
#
# The entry image is entry.png in this directory: a newspaper-style
# infographic summing up the world's news of Thursday 19 November 2026
# (the first Trump-Xi-Putin trilateral in Shenzhen and its joint peace
# declaration, the ICJ ruling that Myanmar committed genocide, the third
# Kerch Bridge strike, tankers ablaze in the Strait of Hormuz, Anthropic's
# record IPO debut, plus four more stories in the bottom strip).
# This program copies those exact bytes to /output/entry.png, so two runs
# always write the same file. No network, no third-party code.
#
# Run it outside the grader's container with:
#   mkdir -p out && MAKEFUN_OUTPUT_DIR=out python3 main.py

import hashlib
import os
import shutil
import sys
from pathlib import Path


def file_digest(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            block = stream.read(1 << 16)
            if not block:
                break
            digest.update(block)
    return digest.hexdigest()


def run():
    target_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    source = Path(__file__).resolve().parent / "entry.png"
    if not source.is_file():
        print(f"error: entry image missing: {source}", file=sys.stderr)
        return 1
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / "entry.png"
    shutil.copyfile(source, target)
    if target.stat().st_size != source.stat().st_size:
        print("error: copied size differs from source", file=sys.stderr)
        return 1
    if file_digest(target) != file_digest(source):
        print("error: copied bytes differ from source", file=sys.stderr)
        return 1
    with target.open("rb") as handle:
        magic = handle.read(8)
    if magic != b"\x89PNG\r\n\x1a\n":
        print("error: output is not a PNG file", file=sys.stderr)
        return 1
    print(f"wrote {target} ({target.stat().st_size} bytes, sha256 verified)")
    return 0


if __name__ == "__main__":
    sys.exit(run())
