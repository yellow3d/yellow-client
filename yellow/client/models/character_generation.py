from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.character_spec import CharacterSpec


T = TypeVar("T", bound="CharacterGeneration")


@_attrs_define
class CharacterGeneration:
    """
    Attributes:
        uuid (str):
        spec (CharacterSpec):
        state (str):
    """

    uuid: str
    spec: "CharacterSpec"
    state: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid

        spec = self.spec.to_dict()

        state = self.state

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "spec": spec,
                "state": state,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.character_spec import CharacterSpec

        d = src_dict.copy()
        uuid = d.pop("uuid")

        spec = CharacterSpec.from_dict(d.pop("spec"))

        state = d.pop("state")

        character_generation = cls(
            uuid=uuid,
            spec=spec,
            state=state,
        )

        character_generation.additional_properties = d
        return character_generation

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
