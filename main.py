#!/usr/bin/env python3
"""Delivery script for the news-image-20261123 entry.

The artwork itself is finished ahead of time: ``entry.png``, sitting next
to this file, holds the rendered front page. Nothing here draws, resizes
or otherwise touches the picture. The one job of this script is to act as
a careful courier — confirm the committed file really is a PNG that fits
the competition limits, then drop an exact copy of it into the folder the
grader names through the MAKEFUN_OUTPUT_DIR environment variable (or
``/output`` when that variable is not set).

Standard library only.
"""

import os
import sys
from pathlib import Path

ARTWORK_NAME = "entry.png"

# Competition limits for the delivered image.
BYTE_LIMIT = 1024 * 1024   # the file may not grow past one mebibyte
SIDE_LIMIT = 1024          # neither edge may exceed 1024 pixels

# How a PNG file begins: an eight-byte signature, then the first chunk,
# which is always IHDR. A chunk opens with its length (4 bytes) and its
# four-letter name; the IHDR body is 13 bytes and starts with the image
# width and height, each a big-endian 32-bit unsigned integer.
SIGNATURE = bytes([0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A])
FIRST_CHUNK_NAME = b"IHDR"
IHDR_BODY_LEN = 13
# signature + chunk length + chunk name + IHDR body
HEADER_LEN = 8 + 4 + 4 + IHDR_BODY_LEN


class ArtworkProblem(Exception):
    """The committed image failed one of the pre-delivery checks."""


def probe_dimensions(blob):
    """Validate the PNG header in ``blob`` and return (width, height)."""
    if len(blob) < HEADER_LEN:
        raise ArtworkProblem(
            f"only {len(blob)} bytes — too short to hold a PNG header"
        )
    if not blob.startswith(SIGNATURE):
        raise ArtworkProblem("the file does not start with a PNG signature")
    declared_len = int.from_bytes(blob[8:12], "big")
    chunk_name = blob[12:16]
    if chunk_name != FIRST_CHUNK_NAME or declared_len != IHDR_BODY_LEN:
        raise ArtworkProblem(
            f"first chunk is {chunk_name!r} of {declared_len} bytes, "
            f"not the expected 13-byte IHDR"
        )
    width = int.from_bytes(blob[16:20], "big")
    height = int.from_bytes(blob[20:24], "big")
    return width, height


def load_and_check(artwork_path):
    """Read the artwork and run every check; return (blob, width, height)."""
    if not artwork_path.is_file():
        raise ArtworkProblem(f"no {ARTWORK_NAME} found beside this script")
    blob = artwork_path.read_bytes()
    if len(blob) > BYTE_LIMIT:
        raise ArtworkProblem(
            f"{ARTWORK_NAME} weighs {len(blob)} bytes; "
            f"the limit is {BYTE_LIMIT}"
        )
    width, height = probe_dimensions(blob)
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        raise ArtworkProblem(
            f"canvas is {width}x{height}; "
            f"the limit is {SIDE_LIMIT}x{SIDE_LIMIT}"
        )
    return blob, width, height


def deliver(blob, target_dir):
    """Write ``blob`` to ``target_dir/entry.png`` in slices; return the path."""
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / ARTWORK_NAME
    with target.open("wb") as sink:
        for offset in range(0, len(blob), 65536):
            sink.write(blob[offset:offset + 65536])
    return target


def run():
    script_dir = Path(__file__).resolve().parent
    try:
        blob, width, height = load_and_check(script_dir / ARTWORK_NAME)
    except ArtworkProblem as problem:
        print(f"refusing to deliver: {problem}", file=sys.stderr)
        return 1

    destination_root = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    written = deliver(blob, destination_root)
    print(
        f"delivered {ARTWORK_NAME} ({width}x{height}, {len(blob)} bytes) "
        f"to {written}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(run())
