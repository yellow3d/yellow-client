from enum import Enum


class SculptCharactersFetchRetrieveRigType(str, Enum):
    BLENDER_BASIC_HUMAN_METARIG = "blender-basic-human-metarig"
    NO_RIG = "no-rig"

    def __str__(self) -> str:
        return str(self.value)
