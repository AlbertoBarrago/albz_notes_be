"""
Handle note related errors
"""
from fastapi import HTTPException
from starlette import status

class NoteErrorHandler:
    """
    Handle note related errors
    """
    @classmethod
    def raise_note_not_found(cls):
        """
        Raise note not found error
        """
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Note not found"
        )

    @classmethod
    def raise_unauthorized_note_access(cls):
        """
        Raise unauthorized note access error
        """
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to access this note"
        )

    @classmethod
    def raise_note_creation_error(cls, error):
        """
        Raise note creation error
        """
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the note: {str(error)}"
        )
