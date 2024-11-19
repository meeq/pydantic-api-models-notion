from pydantic import BaseModel, Field

from ..entities import CommentObject
from .base import NotionPaginatedData, StartCursor, PageSize


class CreateCommentRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/create-a-comment"""

    start_cursor: StartCursor = None
    page_size: PageSize = None


CreateCommentResponse = CommentObject
"""Reference: https://developers.notion.com/reference/create-a-comment"""


class RetrieveCommentsRequest(BaseModel):
    """Reference: https://developers.notion.com/reference/retrieve-a-comment"""

    block_id: str = Field(..., description="Identifier for a Notion block or page")
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
