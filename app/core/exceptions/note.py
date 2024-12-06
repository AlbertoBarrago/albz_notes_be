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
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error retrieving note"
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

    @classmethod
    def raise_pagination_error(cls, error):
        """
        Raise pagination error
        """
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while paginating the notes list: {str(error)}"
        )

    @classmethod
    def raise_general_error(cls, param):
        """
        Raises a general error with the given parameter as the error message.

        This method is a class method that triggers a controlled error for
        demonstration or testing purposes. It uses the provided parameter as
        the message for the error being raised, allowing the user to specify
        custom error messages.

        Parameters:
        param (str): The message to be used as the error text. This should be a
        string that clearly describes the error situation or condition.

        Raises:
        Exception: An exception is raised using the provided parameter as the
        error message.
        """
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"General error: {param}"
        )

    @classmethod
    def raise_note_update_error(cls, e):
        """
        Raise note update error
        """
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the note: {str(e)}"
        )

    @classmethod
    def raise_delete_note_error(cls, e):
        """
        Raise delete note error
        """
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the note: {str(e)}"
        )
