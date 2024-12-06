"""
    Cache Repository
"""
from typing import Generic, List, Optional, TypeVar

from pydantic import BaseModel

T = TypeVar('T')


class PaginatedResponse(BaseModel, Generic[T]):
    """
    PaginatedResponse serves as a generic model for paginated API responses.

    It encapsulates the necessary attributes to handle paginated content efficiently,
    including the list of items, total counts, pagination details, and optional
    query information. This class is designed to work generically with any type of items,
    facilitating versatile usage across different domain contexts.

    Attributes:
        items (List[T]): The list of items on the current page.
        total (int): The total number of items in the entire dataset.
        page (int): The current page number.
        page_size (int): The number of items per page.
        total_pages (int): The total number of pages based on the current page size.
        has_next (bool): Indicates if there is a subsequent page available.
        has_prev (bool): Indicates if there is a preceding page available.
        search_query (Optional[str]): An optional query string that was used to
                                      filter the dataset, if applicable.
    """
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
    search_query: Optional[str] = None
