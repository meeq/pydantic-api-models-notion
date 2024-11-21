"""
Reference: https://developers.notion.com/reference/page-property-values
"""

from typing import Literal, Union, List, Optional, Annotated
from datetime import datetime

from uuid import UUID
from pydantic import Field, EmailStr, HttpUrl

from pydantic_api.base import BaseModel
from ..user import UserObject
from ..file import FileObject
from ..block import RichTextObject, RichTextObjectFactory
from .common import (
    SelectOption,
    StatusOption,
    ColorLiteral,
    PagePropertyTypeLiteral,
    FormulaValueTypeLiteral,
    RollupTypeLiteral,
    RollupFunctionLiteral,
    VerificationStateLiteral,
)


class BasePageProperty(BaseModel):
    id: Optional[str] = Field(
        None,
        description="An underlying identifier for the property. id may be used in place of name when creating or updating pages. id remains constant when the property name changes.",
    )
    type: PagePropertyTypeLiteral


# checkbox, Refer to https://developers.notion.com/reference/page-property-values#checkbox
class CheckboxProperty(BasePageProperty):
    type: Literal["checkbox"] = "checkbox"
    checkbox: bool = Field(
        ..., description="Whether the checkbox is checked (true) or unchecked (false)."
    )


# created_by, Refer to https://developers.notion.com/reference/page-property-values#created_by
class CreatedByProperty(BasePageProperty):
    type: Literal["created_by"] = "created_by"
    created_by: UserObject


# created_time, Refer to https://developers.notion.com/reference/page-property-values#created_time
class CreatedTimeProperty(BasePageProperty):
    type: Literal["created_time"] = "created_time"
    created_time: datetime


# date, Refer to https://developers.notion.com/reference/page-property-values#date
class DateValue(BaseModel):
    """Represents the value of a date property."""

    start: datetime = Field(..., description="The start of the date or date range.")
    end: Optional[datetime] = Field(
        None, description="The end of the date range. If None, the date is not a range."
    )
    time_zone: Optional[str] = Field(None, description="")


class DateProperty(BasePageProperty):
    """A page property of type 'date'."""

    type: Literal["date"] = "date"
    date: DateValue = Field(
        ...,
        description="The value of the date property, including start and optional end.",
    )

    @classmethod
    def new(
        cls,
        start: datetime,
        end: Optional[datetime] = None,
        time_zone: Optional[str] = None,
    ):
        return cls(date=DateValue(start=start, end=end, time_zone=time_zone))


# email: Refer to https://developers.notion.com/reference/page-property-values#email
class EmailProperty(BasePageProperty):
    type: Literal["email"] = "email"
    email: EmailStr


# files: Refer to https://developers.notion.com/reference/page-property-values#files
class FilesProperty(BasePageProperty):
    """Please note that when post or patch, FileObject must provide: `name` and `external` at the same time."""

    type: Literal["files"] = "files"
    files: List[FileObject]


# formula: Refer to https://developers.notion.com/reference/page-property-values#formula
class _BaseFormulaData(BaseModel):
    type: FormulaValueTypeLiteral


class BooleanFormulaData(_BaseFormulaData):
    type: Literal["boolean"] = "boolean"
    boolean: bool


class DateFormulaData(_BaseFormulaData):
    type: Literal["date"] = "date"
    date: DateValue


class NumberFormulaData(_BaseFormulaData):
    type: Literal["number"] = "number"
    number: float


class StringFormulaData(_BaseFormulaData):
    type: Literal["string"] = "string"
    string: str


FormulaData = Annotated[
    Union[BooleanFormulaData, DateFormulaData, NumberFormulaData, StringFormulaData],
    Field(discriminator="type"),
]


class FormulaProperty(BasePageProperty):
    type: Literal["formula"] = "formula"
    formula: FormulaData


# last_edited_by: Refer to https://developers.notion.com/reference/page-property-values#last_edited_by
class LastEditedByProperty(BasePageProperty):
    type: Literal["last_edited_by"] = "last_edited_by"
    last_edited_by: UserObject


# last_edited_time: Refer to https://developers.notion.com/reference/page-property-values#last_edited_time
class LastEditedTimeProperty(BasePageProperty):
    type: Literal["last_edited_time"] = "last_edited_time"
    last_edited_time: datetime


# multi_select: Refer to https://developers.notion.com/reference/page-property-values#multi_select
class MultiSelectProperty(BasePageProperty):
    type: Literal["multi_select"] = "multi_select"
    multi_select: List[SelectOption]


# number: Refer to https://developers.notion.com/reference/page-property-values#number
class NumberProperty(BasePageProperty):
    type: Literal["number"] = "number"
    number: float


# people: Refer to https://developers.notion.com/reference/page-property-values#people
class PeopleProperty(BasePageProperty):
    type: Literal["people"] = "people"
    people: List[UserObject]


# phone_number: Refer to https://developers.notion.com/reference/page-property-values#phone_number
class PhoneNumberProperty(BasePageProperty):
    type: Literal["phone_number"] = "phone_number"
    phone_number: Optional[str] = Field(
        None,
        description="A string representing a phone number. No phone number format is enforced.",
        examples=["415-867-5309"],
    )


# relation: Refer to https://developers.notion.com/reference/page-property-values#relation
class PageReference(BaseModel):
    id: UUID = Field(..., description="id of the referenced page")


class RelationProperty(BasePageProperty):
    type: Literal["relation"] = "relation"
    relation: List[PageReference]
    has_more: Optional[bool] = Field(
        None,
        description="If a relation has more than 25 references, then the has_more value for the relation in the response object is true. If a relation doesn’t exceed the limit, then has_more is false.",
    )

    @classmethod
    def create(cls, relation: List[UUID]):
        return cls(relation=[PageReference(id=uuid) for uuid in relation])


# rollup: Refer to https://developers.notion.com/reference/page-property-values#rollup
class BaseRollupData(BaseModel):
    type: RollupTypeLiteral
    function: RollupFunctionLiteral


class DateRollupData(BaseRollupData):
    type: Literal["date"] = "date"
    date: DateValue


class NumberRollupData(BaseRollupData):
    type: Literal["number"] = "number"
    number: float


class ArrayRollupData(BaseRollupData):
    # TODO: I don't know how array is represented
    type: Literal["array"] = "array"


class IncompleteRollupData(BaseRollupData):
    # TODO: I don't know how incomplete is represented
    type: Literal["incomplete"] = "incomplete"


class UnsupportedRollupData(BaseRollupData):
    # TODO: I don't know how unsupported is represented
    type: Literal["unsupported"] = "unsupported"


RollupData = Annotated[
    Union[
        DateRollupData,
        NumberRollupData,
        ArrayRollupData,
        IncompleteRollupData,
        UnsupportedRollupData,
    ],
    Field(discriminator="type"),
]


class RollupProperty(BasePageProperty):
    """
    Note:

    - The API does not support updating rollup page property values.
    - For rollup properties with more than 25 references, use the Retrieve a page property endpoint
    """

    type: Literal["rollup"] = "rollup"
    rollup: RollupData


# rich_text: Refer to https://developers.notion.com/reference/page-property-values#rich_text
class RichTextProperty(BasePageProperty):
    type: Literal["rich_text"] = "rich_text"
    rich_text: List[RichTextObject]


#  select: Refer to https://developers.notion.com/reference/page-property-values#select
class SelectProperty(BasePageProperty):
    type: Literal["select"] = "select"
    select: SelectOption

    @classmethod
    def create(
        cls,
        name: str,
        color: Optional[str] = None,
    ):
        return cls(select=SelectOption.create(name=name, color=color))


# status
class StatusProperty(BasePageProperty):
    type: Literal["status"] = "status"
    status: StatusOption

    @classmethod
    def create(
        cls,
        name: str,
        color: Optional[ColorLiteral] = "default",
    ):
        return cls(status=StatusOption.create(name=name, color=color))

    @classmethod
    def refer(
        cls,
        name: str,
    ):
        return cls(status=StatusOption.refer(name=name))


# title
class TitleProperty(BasePageProperty):
    type: Literal["title"] = "title"
    title: List[RichTextObject]

    @classmethod
    def new(
        cls,
        text: str,
    ):
        """
        Author Note: This method is a simple version now, does not support annotations and links, but it works for most cases.

        Args:
            text (str): The text content of the title.
        """
        return cls(title=[RichTextObjectFactory.new_text(content=text)])


# url
class URLProperty(BasePageProperty):
    type: Literal["url"] = "url"
    url: HttpUrl


# unique_id
class UniqueIDData(BaseModel):
    number: int = Field(..., description="The ID count (auto-incrementing).")
    prefix: Optional[str] = Field(
        None, description="An optional prefix to be applied to the unique ID."
    )


class UniqueIDProperty(BasePageProperty):
    """
    Note: Unique IDs can be read using the API with a GET page request, but they cannot be updated with the API, since they are auto-incrementing.
    """

    type: Literal["unique_id"] = "unique_id"
    unique_id: UniqueIDData


# verification
class VerificationData(BaseModel):
    state: VerificationStateLiteral
    verified_by: Optional[UserObject] = Field(
        None,
        description="If the page if verified, a User object will be included to indicate the user who verified the page.",
    )
    date: Optional[DateValue] = Field(
        None,
        description="If the page is verified, the date object will include the date the verification started (start). If an expiration date is set for the verification, an end date (end) will be included. (ISO 8601 date and time.)",
    )


class VerificationProperty(BasePageProperty):
    type: Literal["verification"] = "verification"
    verification: VerificationData


# Union types
PageProperty = Annotated[
    Union[
        CheckboxProperty,
        CreatedByProperty,
        CreatedTimeProperty,
        DateProperty,
        EmailProperty,
        FilesProperty,
        LastEditedByProperty,
        LastEditedTimeProperty,
        MultiSelectProperty,
        NumberProperty,
        PeopleProperty,
        PhoneNumberProperty,
        RichTextProperty,
        SelectProperty,
        StatusProperty,
        TitleProperty,
        URLProperty,
        FormulaProperty,
        RelationProperty,
        RollupProperty,
        UniqueIDProperty,
        VerificationProperty,
    ],
    Field(discriminator="type"),
]


__all__ = [
    "CheckboxProperty",
    "CreatedByProperty",
    "CreatedTimeProperty",
    "DateProperty",
    "EmailProperty",
    "FilesProperty",
    "LastEditedByProperty",
    "LastEditedTimeProperty",
    "MultiSelectProperty",
    "NumberProperty",
    "PeopleProperty",
    "PhoneNumberProperty",
    "RichTextProperty",
    "SelectProperty",
    "StatusProperty",
    "TitleProperty",
    "URLProperty",
    "FormulaProperty",
    "RelationProperty",
    "RollupProperty",
    "UniqueIDProperty",
    "VerificationProperty",
    # Union types
    "PageProperty",
]
