from fastapi import status
from backend.exceptions import api_exceptions

users_dict: dict[str, dict[str, str | dict[str, str]]] = {
    "user_2137": {
        "summary": "A totally normal example",
        "description": "A **normal** user works correctly.",
        "value": {
            "user_id": "user_2137",
            "name": "John",
            "email": "john.paul@second.pl",
        },
    },
    "user_69": {
        "summary": "For some people normal example",
        "description": "A **'normal'** user works correctly.",
        "value": {
            "user_id": "user_69",
            "name": "Jeffrey",
            "email": "jeffrey.epstein@loveisland.vi",
        },
    },
    "austrian painter": {
        "summary": "For most people not a normal example",
        "description": "A **not normal** user but still works correctly.",
        "value": {
            "user_id": "user_1939",
            "name": "Adolf",
            "email": "adolf.h@academy.fine.arts.at",
        },
    },
}

tst = {
    200: {
        "description": "User found and returned",
        "content": {
            "application/json": {
                "examples": {
                    "user_2137": {
                        "summary": "A totally normal example",
                        "description": "A **normal** user works correctly.",
                        "value": {
                            "user_id": "user_2137",
                            "name": "John",
                            "email": "john.paul@second.pl",
                        },
                    },
                    "user_69": {
                        "summary": "For some people normal example",
                        "description": "A **'normal'** user works correctly.",
                        "value": {
                            "user_id": "user_69",
                            "name": "Jeffrey",
                            "email": "jeffrey.epstein@loveisland.vi",
                        },
                    },
                    "austrian painter": {
                        "summary": "For most people not a normal example",
                        "description": "A **not normal** user but still works correctly.",
                        "value": {
                            "user_id": "user_1939",
                            "name": "Adolf",
                            "email": "adolf.h@finearts.at",
                        },
                    },
                }
            }
        },
    },
    # 404: {"description": "User not found"},
    "4xx": {
        "description": "4xx Status code returned",
        "content": {
            "application/json": {
                "examples": {
                    api_exceptions.InvalidInputError.__name__: api_exceptions.InvalidInputError.openapi(),
                    api_exceptions.MissingFieldError.__name__: api_exceptions.MissingFieldError.openapi(),
                    api_exceptions.FieldFormatError.__name__: api_exceptions.FieldFormatError.openapi(),
                    api_exceptions.NotFoundError.__name__: api_exceptions.NotFoundError.openapi(),
                    api_exceptions.RequestConflictError.__name__: api_exceptions.RequestConflictError.openapi(),
                },
            }
        },
    },
    500: {"description": "Internal server error"},
}


dct = {
    200: {
        "description": "User found and returned",
        "content": {
            "application/json": {
                "examples": {
                    "normal user": {
                        "summary": "Getting user successful 1",
                        "description": "User found and returned 1",
                        "value": {
                            "content": users_dict["user_2137"],
                        },
                    },
                    "'normal' user": {
                        "summary": "Getting user successful 2",
                        "description": "User found and returned 2",
                        "value": {
                            "content": users_dict["user_69"],
                        },
                    },
                    "not normal user": {
                        "summary": "Getting user successful 3",
                        "description": "User found and returned 3",
                        "value": {
                            "content": users_dict["austrian painter"],
                        },
                    },
                }
            }
        },
    },
    404: {"description": "User not found"},
    500: {"description": "Internal server error"},
}


users: dict = {
    200: {
        "description": "Success",
        "content": {
            "application/json": {
                "examples": {
                    "normal user": {
                        "summary": "Getting user successful 1",
                        "value": {
                            "status_code": status.HTTP_200_OK,
                            # "content": users_dict["user_2137"],
                        },
                    },
                    "'normal' user": {
                        "summary": "Getting user successful 2",
                        "value": {
                            "status_code": status.HTTP_200_OK,
                            # "content": users_dict["user_69"],
                        },
                    },
                    "not normal user": {
                        "summary": "Getting user successful 3",
                        "value": {
                            "status_code": status.HTTP_200_OK,
                            # "content": users_dict["austrian painter"],
                        },
                    },
                }
            }
        },
    },
    404: {
        "content": {
            "application/json": {"example": "User_ID: {user_id} Not Found"}
        },
    },
}
