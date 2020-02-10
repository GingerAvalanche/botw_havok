import io
from typing import Union

from .binary import BinaryReader, BinaryWriter
from .container import HKClassnamesSection, HKDataSection, HKHeader, HKTypesSection


class HK:
    header: HKHeader

    classnames: HKClassnamesSection
    types: HKTypesSection
    data: HKDataSection

    def __init__(self, d: dict = None):
        if d:
            self.header = HKHeader.fromdict(d["header"])

            self.classnames = HKClassnamesSection.fromdict(d["classnames"])
            self.types = HKTypesSection.fromdict(d["types"])
            self.data = HKDataSection.fromdict(d["data"])

    def read(self, br: BinaryReader, deserialize: bool):
        # Read the endian byte ahead
        br.step_in(0x11)
        br.big_endian = br.read_int8() == 0
        br.step_out()

        # Create all needed instances
        self.header = HKHeader()
        self.classnames = HKClassnamesSection()
        self.types = HKTypesSection()
        self.data = HKDataSection()

        # Read Havok header
        self.header.read(br)

        # Read Havok sections' headers
        self.classnames.read_header(br)
        self.types.read_header(br)
        self.data.read_header(br)

        # Read Havok sections' data
        self.classnames.read(br)
        self.types.read(br)
        self.data.read(self, br, deserialize)

    def write(self, bw: BinaryWriter):
        # Write Havok header
        self.header.write(bw)

        # Write Havok sections' header
        self.classnames.write_header(bw)
        self.types.write_header(bw)
        self.data.write_header(bw)

        # Write Havok sections' data
        self.classnames.write(bw)
        self.types.write(bw)
        self.data.write(self, bw)

    def _assert_pointer(self, br: BinaryReader):
        if self.header.pointer_size == 4:
            br.assert_int32(0)
        elif self.header.pointer_size == 8:
            br.assert_int64(0)
        else:
            raise NotImplementedError("Wrong pointer size!")

    def _write_empty_pointer(self, bw: BinaryWriter):
        if self.header.pointer_size == 4:
            bw.write_int32(0)
        elif self.header.pointer_size == 8:
            bw.write_int64(0)
        else:
            raise Exception("Wrong pointer size!")

    @classmethod
    def fromdict(cls, d: dict):
        return cls(d)

    def to_switch(self):
        self.data.deserialize(self)
        self.header.to_switch()
        self.data.serialize(self)

    def to_wiiu(self):
        self.data.deserialize(self)
        self.header.to_wiiu()
        self.data.serialize(self)

    def __repr__(self):
        return f"<{self.__class__.__name__} ({self.header})>"
