import pytest

from bloomberg.pensieve import Tracker
from bloomberg.pensieve._test import MemoryAllocator


def test_rejects_different_header_magic(tmp_path):
    # GIVEN
    output = tmp_path / "test.bin"
    allocator = MemoryAllocator()

    # WHEN
    # Create a valid allocation record file
    with Tracker(output) as tracker:
        allocator.valloc(1024)

    # Change the header magic (same length as "pensieve")
    with output.open("rb+") as f:
        f.write(b"badmagic")

    # THEN
    with pytest.raises(OSError, match="Invalid input file"):
        tracker.reader.get_allocation_records()


def test_rejects_different_header_version(tmp_path):
    # GIVEN
    output = tmp_path / "test.bin"
    allocator = MemoryAllocator()

    # WHEN
    # Create a valid allocation record file
    with Tracker(output) as tracker:
        allocator.valloc(1024)

    # Change the header version to zero
    with output.open("rb+") as f:
        f.seek(9)
        f.write(b"\0")

    # THEN
    with pytest.raises(OSError, match="incompatible with this version"):
        tracker.reader.get_allocation_records()
