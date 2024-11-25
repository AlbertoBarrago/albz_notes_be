"""
 Error schema
"""
from typing import List, Any
from pydantic import BaseModel

class ErrorDetail(BaseModel):
    """
    Error Detail
    """
    loc: List[Any]
    msg: str
    type: str

class ErrorResponse(BaseModel):
    """
    Error Response
    """
    detail: List[ErrorDetail]
