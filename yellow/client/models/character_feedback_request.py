from typing import Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

T = TypeVar("T", bound="CharacterFeedbackRequest")


@_attrs_define
class CharacterFeedbackRequest:
    """
    Attributes:
        feedback (str):
        uuid (str):
    """

    feedback: str
    uuid: str
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        feedback = self.feedback

        uuid = self.uuid

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "feedback": feedback,
                "uuid": uuid,
            }
        )

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        feedback = (None, str(self.feedback).encode(), "text/plain")

        uuid = (None, str(self.uuid).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        for prop_name, prop in self.additional_properties.items():
            field_dict[prop_name] = (None, str(prop).encode(), "text/plain")

        field_dict.update(
            {
                "feedback": feedback,
                "uuid": uuid,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        feedback = d.pop("feedback")

        uuid = d.pop("uuid")

        character_feedback_request = cls(
            feedback=feedback,
            uuid=uuid,
        )

        character_feedback_request.additional_properties = d
        return character_feedback_request

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
