from enum import Enum


class FileFormatEnum(str, Enum):
    OBJ = "obj"
    FBX = "fbx"

    def __str__(self) -> str:
        return str(self.value)
