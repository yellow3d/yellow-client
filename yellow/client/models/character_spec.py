from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.gender_enum import GenderEnum
from ..types import UNSET, Unset

T = TypeVar("T", bound="CharacterSpec")


@_attrs_define
class CharacterSpec:
    """
    Attributes:
        prompt (str):
        gender (GenderEnum): * `male` - Male
            * `female` - Female
            * `neutral` - Neutral
        n_variants (Union[Unset, int]):  Default: 2.
    """

    prompt: str
    gender: GenderEnum
    n_variants: Union[Unset, int] = 2
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        prompt = self.prompt

        gender = self.gender.value

        n_variants = self.n_variants

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "prompt": prompt,
                "gender": gender,
            }
        )
        if n_variants is not UNSET:
            field_dict["n_variants"] = n_variants

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        prompt = d.pop("prompt")

        gender = GenderEnum(d.pop("gender"))

        n_variants = d.pop("n_variants", UNSET)

        character_spec = cls(
            prompt=prompt,
            gender=gender,
            n_variants=n_variants,
        )

        character_spec.additional_properties = d
        return character_spec

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
