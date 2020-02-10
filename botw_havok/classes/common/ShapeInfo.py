from ...binary import BinaryReader, BinaryWriter


class ShapeInfo:
    ActorInfoIndex: int
    InstanceId: int
    BodyGroup: int
    BodyLayerType: int

    def __init__(self, d: dict = None):
        if d:
            (
                self.ActorInfoIndex,
                self.InstanceId,
                self.BodyGroup,
                self.BodyLayerType,
            ) = d.values()

    def read(self, br: BinaryReader):
        self.ActorInfoIndex = br.read_int32()
        self.InstanceId = br.read_int32()
        self.BodyGroup = br.read_int16()
        self.BodyLayerType = br.read_uint16()

    def write(self, bw: BinaryWriter):
        bw.write_int32(self.ActorInfoIndex)
        bw.write_int32(self.InstanceId)
        bw.write_int16(self.BodyGroup)
        bw.write_uint16(self.BodyLayerType)

    def asdict(self):
        return {
            "ActorInfoIndex": self.ActorInfoIndex,
            "InstanceId": self.InstanceId,
            "BodyGroup": self.BodyGroup,
            "BodyLayerType": self.BodyLayerType,
        }

    @classmethod
    def fromdict(cls, d: dict):
        return cls(d)

    def __repr__(self):
        return (
            f"{self.__class__.__name__}({self.ActorInfoIndex}, "
            f"{self.InstanceId}, {self.BodyGroup}, {self.BodyLayerType})"
        )
