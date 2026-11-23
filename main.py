#!/usr/bin/env python3
"""Copy the pre-rendered newspaper front page into the output folder.

The image (entry.png) is generated ahead of time and committed in this
repository. At grade time this script only validates the committed file
and copies it byte-for-byte to the directory named by
MAKEFUN_OUTPUT_DIR (default /output). It never draws anything, never
imports any drawing module, and never writes into this repository.

Only the Python standard library is used.
"""

import os
import struct
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
MAX_BYTES = 1_048_576
MAX_SIDE = 1024
SOURCE_NAME = "entry.png"


def fail(message):
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def inspect_png(data):
    """Check the magic bytes and IHDR, return (width, height)."""
    if len(data) < 33:
        fail("file too short to be a PNG")
    if data[:8] != PNG_MAGIC:
        fail("missing PNG signature")
    ihdr_length = struct.unpack(">I", data[8:12])[0]
    ihdr_type = data[12:16]
    if ihdr_type != b"IHDR" or ihdr_length != 13:
        fail("first chunk is not a 13-byte IHDR")
    width, height = struct.unpack(">II", data[16:24])
    return width, height


def main():
    here = Path(__file__).resolve().parent
    source = here / SOURCE_NAME
    if not source.is_file():
        fail(f"{SOURCE_NAME} not found next to this script")

    data = source.read_bytes()
    if len(data) > MAX_BYTES:
        fail(f"{SOURCE_NAME} is {len(data)} bytes, over the {MAX_BYTES} limit")

    width, height = inspect_png(data)
    if width > MAX_SIDE or height > MAX_SIDE:
        fail(f"image is {width}x{height}, over the {MAX_SIDE}px limit")

    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    destination = out_dir / SOURCE_NAME
    with open(destination, "wb") as handle:
        handle.write(data)

    print(f"copied {SOURCE_NAME}: {width}x{height}, {len(data)} bytes -> {destination}")


if __name__ == "__main__":
    main()
