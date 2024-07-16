import datetime
from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar, Union, cast

from attrs import define as _attrs_define
from attrs import field as _attrs_field
from dateutil.parser import isoparse

if TYPE_CHECKING:
    from ..models.character_variant_generation_status import CharacterVariantGenerationStatus


T = TypeVar("T", bound="CharacterGenerationStatus")


@_attrs_define
class CharacterGenerationStatus:
    """
    Attributes:
        uuid (str):
        state (str):
        progress (float):
        started_at (Union[None, datetime.datetime]):
        feedback (str):
        variants (List['CharacterVariantGenerationStatus']):
    """

    uuid: str
    state: str
    progress: float
    started_at: Union[None, datetime.datetime]
    feedback: str
    variants: List["CharacterVariantGenerationStatus"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        uuid = self.uuid

        state = self.state

        progress = self.progress

        started_at: Union[None, str]
        if isinstance(self.started_at, datetime.datetime):
            started_at = self.started_at.isoformat()
        else:
            started_at = self.started_at

        feedback = self.feedback

        variants = []
        for variants_item_data in self.variants:
            variants_item = variants_item_data.to_dict()
            variants.append(variants_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "uuid": uuid,
                "state": state,
                "progress": progress,
                "started_at": started_at,
                "feedback": feedback,
                "variants": variants,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.character_variant_generation_status import CharacterVariantGenerationStatus

        d = src_dict.copy()
        uuid = d.pop("uuid")

        state = d.pop("state")

        progress = d.pop("progress")

        def _parse_started_at(data: object) -> Union[None, datetime.datetime]:
            if data is None:
                return data
            try:
                if not isinstance(data, str):
                    raise TypeError()
                started_at_type_0 = isoparse(data)

                return started_at_type_0
            except:  # noqa: E722
                pass
            return cast(Union[None, datetime.datetime], data)

        started_at = _parse_started_at(d.pop("started_at"))

        feedback = d.pop("feedback")

        variants = []
        _variants = d.pop("variants")
        for variants_item_data in _variants:
            variants_item = CharacterVariantGenerationStatus.from_dict(variants_item_data)

            variants.append(variants_item)

        character_generation_status = cls(
            uuid=uuid,
            state=state,
            progress=progress,
            started_at=started_at,
            feedback=feedback,
            variants=variants,
        )

        character_generation_status.additional_properties = d
        return character_generation_status

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
