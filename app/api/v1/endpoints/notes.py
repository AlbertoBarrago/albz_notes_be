"""
Note Endpoint
"""
from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.models.users import User
from app.db.mysql import get_db, get_current_user
from app.schemas.note import (NoteOut, NoteCreate,
                              NoteDelete, NoteUpdate)
from app.schemas.pagination import PaginatedResponse
from app.services.note.actions import NoteManager

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='api/v1/token')

router = APIRouter()


@router.get("/list/explore",
            response_model=PaginatedResponse[NoteOut],
            responses={
                404: {
                    "description": "Notes not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Notes not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            })
def get_explore_notes(
        page: int = Query(default=1, gt=0),
        page_size: int = Query(default=10, gt=0, le=100),
        sort_order: str = Query(default="asc", regex="^(asc|desc)$"),
        query: str = Query(default="", max_length=100),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Get paginated notes
    :param page:
    :param page_size:
    :param sort_order:
    :param current_user:
    :param query:
    :param db:
    :return:
    """
    return NoteManager(db).perform_note_action("get_explore_notes",
                                               current_user=current_user,
                                               page=page,
                                               sort_order=sort_order,
                                               query=query,
                                               page_size=page_size)


@router.get("/list/paginated",
            response_model=PaginatedResponse[NoteOut],
            responses={
                404: {
                    "description": "Notes not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Notes not found",
                                "status_code": 404
                            }
                        }
                    }
                }
            })
def get_paginated_and_filtered_notes(
        page: int = Query(default=1, gt=0),
        page_size: int = Query(default=10, gt=0, le=100),
        sort_order: str = Query(default="asc", regex="^(asc|desc)$"),
        query: str = Query(default="", max_length=100),
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    """
    Get paginated notes
    :param page:
    :param page_size:
    :param sort_order:
    :param current_user:
    :param query:
    :param db:
    :return:
    """
    return NoteManager(db).perform_note_action("get_note_paginated",
                                               current_user=current_user,
                                               page=page,
                                               sort_order=sort_order,
                                               query=query,
                                               page_size=page_size)


@router.get("/{note_id}",
            response_model=NoteOut,
            responses={
                404: {
                    "description": "Note not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Note not found",
                                "status_code": 404
                            }
                        }
                    }
                },
                403: {
                    "description": "Not authorized",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Not authorized to update this note",
                                "status_code": 403
                            }
                        }
                    }
                }
            })
def get_note(note_id: int,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    """
    Get Note
    :param note_id:
    :param db:
    :param current_user:
    :return: NoteOut
    """

    return NoteManager(db).perform_note_action('get_note_by_id',
                                               note_id=note_id,
                                               current_user=current_user)


@router.put("/{note_id}",
            response_model=NoteOut,
            responses={
                404: {
                    "description": "Note not found",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "Note not found",
                                "status_code": 404
                            }
                        }
                    }
                },
                403: {
                    "description": "Permission denied",
                    "content": {
                        "application/json": {
                            "example": {
                                "detail": "You do not have permission to update this note",
                                "status_code": 403
                            }
                        }
                    }
                }
            })
def update_note(note_id: int, note: NoteUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    """
    Update a note
    :param note_id:
    :param note:
    :param db:
    :param current_user:
    :return: NoteOut
    """

    return NoteManager(db).perform_note_action('update_note',
                                               note,
                                               note_id=note_id,
                                               current_user=current_user)


@router.post("/",
             response_model=NoteOut,
             responses={
                 403: {
                     "description": "Permission denied",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "You do not have permission to create a note",
                                 "status_code": 403
                             }
                         }
                     }
                 },
                 500: {
                     "description": "Note creation failed",
                     "content": {
                         "application/json": {
                             "example": {
                                 "detail": "An error occurred while creating the note",
                                 "status_code": 500
                             }
                         }
                     }
                 }
             })
def add_note(note: NoteCreate,
             db: Session = Depends(get_db),
             current_user: User = Depends(get_current_user)):
    """
    Create a new note
    :param note:
    :param db:
    :param current_user:
    :return: NoteOut
    """

    return NoteManager(db).perform_note_action('add_note',
                                               note,
                                               current_user=current_user)


@router.delete("/{note_id}",
               response_model=NoteDelete,
               responses={
                   403: {
                       "description": "Permission denied",
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "You do not have permission to delete this note",
                                   "status_code": 403
                               }
                           }
                       }
                   },
                   404: {
                       "description": "Note not found",
                       "content": {
                           "application/json": {
                               "example": {
                                   "detail": "Note not found",
                                   "status_code": 404
                               }
                           }
                       }
                   }
               })
def delete_note(note_id: int,
                db: Session = Depends(get_db),
                current_user: User = Depends(get_current_user)):
    """
    Delete a note
    :param note_id:
    :param db:
    :param current_user:
    :return: NoteDelete
    """

    return NoteManager(db).perform_note_action("delete_note",
                                               note_id=note_id,
                                               current_user=current_user)
