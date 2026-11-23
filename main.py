#!/usr/bin/env python3
"""Delivery script for the news-image-20261123 entry.

The one job of this script is to act as a careful courier — confirm the
picture really is a PNG that fits the competition limits, then drop an
exact copy of it into the folder the grader names through the
MAKEFUN_OUTPUT_DIR environment variable (or ``/output`` when that
variable is not set). Nothing here draws, resizes or otherwise touches
the picture itself.

Where the picture comes from, in order of preference:

1. ``entry.png`` beside this script — the finished artwork, when it is
   present (local runs, a full checkout).
2. ``entry.png.b64`` beside this script — the same artwork carried as
   base64 text. This is the path the platform takes: its checkout holds
   text files only, the repository folder is read-only, and no imaging
   library is installed there. The decode happens in memory and the
   script writes nothing next to itself.
3. A fresh drawing from the companion module ``make_image`` — local
   development only. It needs Pillow and writes into this folder, so it
   is never used on the platform; the embedded copy above always serves
   there first.

Standard library only.
"""

import base64
import os
import sys
from pathlib import Path

ARTWORK_NAME = "entry.png"
EMBEDDED_NAME = "entry.png.b64"

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


def check_blob(blob, label):
    """Run every delivery check over raw PNG bytes; return (blob, w, h)."""
    if len(blob) > BYTE_LIMIT:
        raise ArtworkProblem(
            f"{label} weighs {len(blob)} bytes; "
            f"the limit is {BYTE_LIMIT}"
        )
    width, height = probe_dimensions(blob)
    if width > SIDE_LIMIT or height > SIDE_LIMIT:
        raise ArtworkProblem(
            f"canvas is {width}x{height}; "
            f"the limit is {SIDE_LIMIT}x{SIDE_LIMIT}"
        )
    return blob, width, height


def load_and_check(artwork_path):
    """Read the artwork file and run every check over its bytes."""
    if not artwork_path.is_file():
        raise ArtworkProblem(f"no {ARTWORK_NAME} found beside this script")
    return check_blob(artwork_path.read_bytes(), ARTWORK_NAME)


def load_embedded(script_dir):
    """Decode the base64-embedded artwork; return checked (blob, w, h).

    Returns None when no embedded copy sits beside the script. Raises
    ArtworkProblem when one is present but damaged. The bytes live only
    in memory — nothing is written to ``script_dir``, which on the
    platform is a read-only checkout.
    """
    embedded_path = script_dir / EMBEDDED_NAME
    if not embedded_path.is_file():
        return None
    encoded = embedded_path.read_bytes().strip()
    try:
        blob = base64.b64decode(encoded, validate=True)
    except ValueError as failure:
        raise ArtworkProblem(
            f"{EMBEDDED_NAME} is not valid base64: {failure}"
        )
    return check_blob(blob, EMBEDDED_NAME)


def ensure_artwork(artwork_path):
    """Draw the page with ``make_image`` so ``artwork_path`` exists.

    Last resort for local development only: it needs Pillow and writes
    the PNG next to this script, neither of which the platform allows —
    and the platform never reaches this, because the embedded base64
    copy is served first. The import stays inside this function on
    purpose: when the artwork comes from disk or from the embedded
    copy, the drawing module is never loaded at all.
    """
    if artwork_path.is_file():
        return
    folder = str(artwork_path.parent)
    if folder not in sys.path:
        sys.path.insert(0, folder)
    import make_image

    make_image.build()


def deliver(blob, target_dir):
    """Write ``blob`` to ``target_dir/entry.png`` in slices; return the path."""
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / ARTWORK_NAME
    with target.open("wb") as sink:
        for offset in range(0, len(blob), 65536):
            sink.write(blob[offset:offset + 65536])
    return target


def obtain_artwork(script_dir):
    """Return checked (blob, width, height) from the best source at hand.

    Preference order: the rendered ``entry.png`` beside the script; the
    base64-embedded copy (the platform path — decoded in memory, with
    nothing written to the script's folder); and, for local development
    only, a fresh drawing from ``make_image``.
    """
    artwork_path = script_dir / ARTWORK_NAME
    if artwork_path.is_file():
        return load_and_check(artwork_path)
    embedded = load_embedded(script_dir)
    if embedded is not None:
        return embedded
    try:
        ensure_artwork(artwork_path)
    except Exception as failure:
        # Drawing did not work out; load_and_check below will refuse
        # with the plain "no entry.png" message, which is clearer.
        print(f"could not produce {ARTWORK_NAME}: {failure}",
              file=sys.stderr)
    return load_and_check(artwork_path)


def run():
    script_dir = Path(__file__).resolve().parent
    try:
        blob, width, height = obtain_artwork(script_dir)
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
