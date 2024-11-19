from typing import List

from uuid import UUID
from pydantic import BaseModel, Field

from ..objects import CommentObject, RichTextObject
from .base import NotionPaginatedData, StartCursor, PageSize


class CreateCommentRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/create-a-comment"""

    start_cursor: StartCursor = None
    page_size: PageSize = None
    rich_text: List[RichTextObject]


CreateCommentResponse = CommentObject
"""Reference: https://developers.notion.com/reference/create-a-comment"""


class RetrieveCommentsRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/retrieve-a-comment"""

    block_id: UUID = Field(
        ...,
        description="Identifier for a Notion block or page, a uuidv4 string. Reference: https://developers.notion.com/reference/block#keys",
    )
    start_cursor: StartCursor = None
    page_size: PageSize = None


RetrieveCommentsResponse = NotionPaginatedData[CommentObject]
"""Reference: https://developers.notion.com/reference/retrieve-a-comment"""


__all__ = [
    "CreateCommentRequest",
    "CreateCommentResponse",
    "RetrieveCommentsRequest",
    "RetrieveCommentsResponse",
]
