"""
Common responses for the API.
"""


class CommonResponses:
    """
    Provides a collection of common HTTP response representations.

    This class defines a set of standard HTTP responses that can be reused across
    various parts of an application to ensure consistency and clarity in API
    communications. Each response is structured with a status code, a description,
    and an accompanying JSON example for clarity. This class is particularly useful
    for managing error responses and other common status notifications.

    Attributes:
        MAIL_NOT_SENT: Represents a 500 error indicating a failure to send mail.
        MAIL_RESET_NOT_SENT: Represents a 500 error indicating a failure to send a mail reset.
        INTERNAL_SERVER_ERROR: Represents a 500 error for internal server issues.
        SERVICE_UNAVAILABLE: Represents a 503 error indicating service unavailability.
        GATEWAY_TIMEOUT: Represents a 504 error indicating a gateway timeout.
        UNAUTHORIZED: Represents a 401 error indicating a lack of authentication.
        BAD_REQUEST: Represents a 400 error indicating a malformed request.
        FORBIDDEN: Represents a 403 error indicating insufficient permissions.
        NOT_FOUND: Represents a 404 error indicating a missing resource.
        CONFLICT: Represents a 409 error indicating a resource conflict.
        UNPROCESSABLE_ENTITY: Represents a 422 error indicating validation failure.
        SUCCESS: Represents a 200 status indicating a successful operation.
        CREATED: Represents a 201 status indicating successful creation of a resource.
        NO_CONTENT: Represents a 204 status indicating success with no additional content.
    """
    MAIL_NOT_SENT = {
        500: {
            "description": "Mail not sent",
            "content": {
                "application/json": {
                    "example": {"detail": "Mail not sent"}
                }
            }
        }
    }
    MAIL_RESET_NOT_SENT = {
        500: {
            "description": "Mail reset not sent",
            "content": {
                "application/json": {
                    "example": {"detail": "Mail reset not sent"}
                }
            }
        }
    }
    INTERNAL_SERVER_ERROR = {
        500: {
            "description": "Internal server error",
            "content": {
                "application/json": {
                    "example": {"detail": "Internal server error"}
                }
            }
        }
    }

    SERVICE_UNAVAILABLE = {
        503: {
            "description": "Service unavailable",
            "content": {
                "application/json": {
                    "example": {"detail": "Service temporarily unavailable"}
                }
            }
        }
    }

    GATEWAY_TIMEOUT = {
        504: {
            "description": "Gateway timeout",
            "content": {
                "application/json": {
                    "example": {"detail": "Gateway timeout error"}
                }
            }
        }
    }
    UNAUTHORIZED = {
        401: {
            "description": "Not authenticated",
            "content": {
                "application/json": {
                    "example": {"detail": "Not authenticated"}
                }
            }
        }
    }

    BAD_REQUEST = {
        400: {
            "description": "Bad request",
            "content": {
                "application/json": {
                    "example": {"detail": "Bad request"}
                }
            }
        }
    }

    FORBIDDEN = {
        403: {
            "description": "Forbidden",
            "content": {
                "application/json": {
                    "example": {"detail": "Permission denied"}
                }
            }
        }
    }

    NOT_FOUND = {
        404: {
            "description": "Not found",
            "content": {
                "application/json": {
                    "example": {"detail": "Resource not found"}
                }
            }
        }
    }

    CONFLICT = {
        409: {
            "description": "Conflict",
            "content": {
                "application/json": {
                    "example": {"detail": "Resource already exists"}
                }
            }
        }
    }

    UNPROCESSABLE_ENTITY = {
        422: {
            "description": "Validation Error",
            "content": {
                "application/json": {
                    "example": {"detail": "Validation error"}
                }
            }
        }
    }

    SUCCESS = {
        200: {
            "description": "Success",
            "content": {
                "application/json": {
                    "example": {"detail": "Operation successful"}
                }
            }
        }
    }

    CREATED = {
        201: {
            "description": "Created",
            "content": {
                "application/json": {
                    "example": {"detail": "Resource created successfully"}
                }
            }
        }
    }

    NO_CONTENT = {
        204: {
            "description": "No content",
            "content": {
                "application/json": {
                    "example": {"detail": "Operation successful, no content"}
                }
            }
        }
    }
