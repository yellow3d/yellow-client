from enum import Enum


class GenesisEnum(str, Enum):
    VALUE_0 = "3"
    VALUE_1 = "8"
    VALUE_2 = "9"

    def __str__(self) -> str:
        return str(self.value)
