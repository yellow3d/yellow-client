import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

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
        created_at (Union[None, datetime.datetime]):
    """

    uuid: str
    spec: "CharacterSpec"
    state: str
    created_at: Union[None, datetime.datetime]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid

        spec = self.spec.to_dict()

        state = self.state

        created_at: Union[None, str]
        if isinstance(self.created_at, datetime.datetime):
            created_at = self.created_at.isoformat()
        else:
            created_at = self.created_at

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "spec": spec,
                "state": state,
                "created_at": created_at,
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

        def _parse_created_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                created_at_type_0 = isoparse(data)

                return created_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        created_at = _parse_created_at(d.pop("created_at"))

        character_generation = cls(
            uuid=uuid,
            spec=spec,
            state=state,
            created_at=created_at,
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
