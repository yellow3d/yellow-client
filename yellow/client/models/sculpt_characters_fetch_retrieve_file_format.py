from enum import Enum


class SculptCharactersFetchRetrieveFileFormat(str, Enum):
    FBX = "fbx"
    OBJ = "obj"

    def __str__(self) -> str:
        return str(self.value)
