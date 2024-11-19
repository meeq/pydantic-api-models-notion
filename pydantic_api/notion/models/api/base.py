from typing import Generic, TypeVar, Literal, Optional, Annotated

from uuid import UUID
from pydantic import Field

from pydantic_api.base import BaseModel

TResult = TypeVar("TResult")


NotionPaginatedDataTypeLiteral = Literal[
    "block",
    "comment",
    "database",
    "page",
    "page_or_database",
    "property_item",
    "user",
]
"""Reference: https://developers.notion.com/reference/intro#pagination"""


class NotionPaginatedData(BaseModel, Generic[TResult]):
    """
    Reference:

    - https://developers.notion.com/reference/intro#pagination
    - https://developers.notion.com/reference/page-property-values#paginated-page-properties
    """

    object: Literal["list"] = "list"
    results: list[TResult]
    next_cursor: Optional[str] = None
    has_more: bool
    type: NotionPaginatedDataTypeLiteral
    request_id: UUID
    next_url: Optional[str] = Field(
        None,
        description="The URL the user can request to get the next page of results.",
        examples=[
            "http://api.notion.com/v1/pages/0e5235bf86aa4efb93aa772cce7eab71/properties/vYdV?start_cursor=LYxaUO&page_size=25"
        ],
    )


StartCursor = Annotated[
    Optional[str],
    Field(
        description="If supplied, this endpoint will return a page of results starting after the cursor provided. If not supplied, this endpoint will return the first page of results.",
    ),
]

PageSize = Annotated[
    Optional[int],
    Field(
        gt=0,
        le=100,
        description="The number of results to return. The default page size is 100, and the maximum is 100.",
    ),
]

__all__ = [
    "NotionPaginatedData",
    "NotionPaginatedDataTypeLiteral",
    "StartCursor",
    "PageSize",
]
