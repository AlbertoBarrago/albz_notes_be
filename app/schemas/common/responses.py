"""
Common responses for the API.
"""


class CommonResponses:
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
