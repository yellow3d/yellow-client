from enum import Enum


class RigTypeEnum(str, Enum):
    NO_RIG = "no-rig"
    BLENDER_BASIC_HUMAN_METARIG = "blender-basic-human-metarig"

    def __str__(self) -> str:
        return str(self.value)
