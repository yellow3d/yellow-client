from enum import Enum


class GenderEnum(str, Enum):
    FEMALE = "female"
    MALE = "male"
    NEUTRAL = "neutral"

    def __str__(self) -> str:
        return str(self.value)
