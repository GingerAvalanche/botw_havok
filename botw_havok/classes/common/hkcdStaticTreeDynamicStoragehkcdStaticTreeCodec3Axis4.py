from typing import List

from ...binary import BinaryReader, BinaryWriter
from .hkcdStaticTreeCodec3Axis4 import hkcdStaticTreeCodec3Axis4

if False:
    from ...hk import HK
    from ...container.sections.hkobject import HKObject


class hkcdStaticTreeDynamicStoragehkcdStaticTreeCodec3Axis4:
    nodes: List[hkcdStaticTreeCodec3Axis4]

    def __init__(self):
        self.nodes = []

    def deserialize(self, hk: "HK", br: BinaryReader, obj: "HKObject"):
        nodesCount_offset = br.tell()
        nodesCount = hk._read_counter(br)

        br.align_to(16)

        for lfu in obj.local_fixups:
            br.step_in(lfu.dst)

            if lfu.src == nodesCount_offset:
                for _ in range(nodesCount):
                    node = hkcdStaticTreeCodec3Axis4()
                    self.nodes.append(node)
                    node.deserialize(hk, br, obj)

            br.step_out()

    def serialize(self, hk: "HK", bw: BinaryWriter):
        self._nodesCount_offset = bw.tell()
        hk._write_counter(bw, len(self.nodes))

        bw.align_to(16)

        # Nodes get written later

    def asdict(self):
        return {"nodes": [node.asdict() for node in self.nodes]}

    @classmethod
    def fromdict(cls, d: dict):
        inst = cls()

        inst.nodes = [hkcdStaticTreeCodec3Axis4.fromdict(node) for node in d["nodes"]]

        return inst