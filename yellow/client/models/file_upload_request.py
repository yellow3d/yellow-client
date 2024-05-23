from io import BytesIO
from typing import Any, Dict, List, Tuple, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.gender_enum import GenderEnum
from ..models.genesis_enum import GenesisEnum
from ..types import UNSET, File, Unset

T = TypeVar("T", bound="FileUploadRequest")


@_attrs_define
class FileUploadRequest:
    """
    Attributes:
        file (File):
        gender (Union[Unset, GenderEnum]): * `male` - Male
            * `female` - Female
            * `neutral` - Neutral
        genesis (Union[Unset, GenesisEnum]): * `3` - Genesis 3
            * `8` - Genesis 8
            * `9` - Genesis 9
    """

    file: File
    gender: Union[Unset, GenderEnum] = UNSET
    genesis: Union[Unset, GenesisEnum] = UNSET
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        gender: Union[Unset, str] = UNSET
        if not isinstance(self.gender, Unset):
            gender = self.gender.value

        genesis: Union[Unset, str] = UNSET
        if not isinstance(self.genesis, Unset):
            genesis = self.genesis.value

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "file": file,
            }
        )
        if gender is not UNSET:
            field_dict["gender"] = gender
        if genesis is not UNSET:
            field_dict["genesis"] = genesis

        return field_dict

    def to_multipart(self) -> Dict[str, Any]:
        file = self.file.to_tuple()

        gender: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.gender, Unset):
            gender = (None, str(self.gender.value).encode(), "text/plain")

        genesis: Union[Unset, Tuple[None, bytes, str]] = UNSET
        if not isinstance(self.genesis, Unset):
            genesis = (None, str(self.genesis.value).encode(), "text/plain")

        field_dict: Dict[str, Any] = {}
        field_dict.update(
            {key: (None, str(value).encode(), "text/plain") for key, value in self.additional_properties.items()}
        )
        field_dict.update(
            {
                "file": file,
            }
        )
        if gender is not UNSET:
            field_dict["gender"] = gender
        if genesis is not UNSET:
            field_dict["genesis"] = genesis

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        file = File(payload=BytesIO(d.pop("file")))

        _gender = d.pop("gender", UNSET)
        gender: Union[Unset, GenderEnum]
        if isinstance(_gender, Unset):
            gender = UNSET
        else:
            gender = GenderEnum(_gender)

        _genesis = d.pop("genesis", UNSET)
        genesis: Union[Unset, GenesisEnum]
        if isinstance(_genesis, Unset):
            genesis = UNSET
        else:
            genesis = GenesisEnum(_genesis)

        file_upload_request = cls(
            file=file,
            gender=gender,
            genesis=genesis,
        )

        file_upload_request.additional_properties = d
        return file_upload_request

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
