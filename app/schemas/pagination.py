"""
 PaginatedResponse
"""
from typing import Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar('T')

class PaginatedResponse(BaseModel, Generic[T]):
    """
    PaginatedResponse
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    """
    items: List[T]
    total: int
    page: int
    page_size: int
    total_pages: int
    has_next: bool
    has_prev: bool
