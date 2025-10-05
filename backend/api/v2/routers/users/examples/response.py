from backend import exceptions

user_2137 = {
    "user_2137": {
        "summary": "A totally normal example",
        "description": "A **normal** user works correctly.",
        "value": {
            "user_id": "user_2137",
            "name": "John",
            "email": "john.paul@second.pl",
        },
    }
}
user_69 = {
    "user_69": {
        "summary": "For some people normal example",
        "description": "A **'normal'** user works correctly.",
        "value": {
            "user_id": "user_69",
            "name": "Jeffrey",
            "email": "jeffrey.epstein@loveisland.vi",
        },
    }
}
austrian_painter = {
    "austrian painter": {
        "summary": "For most people not a normal example",
        "description": "A **not normal** user but still works correctly.",
        "value": {
            "user_id": "user_1939",
            "name": "Adolf",
            "email": "adolf.h@academy.fine.arts.at",
        },
    }
}

# users_dict: dict[str, dict[str, str | dict[str, str]]] = {
#     "user_2137": {
#         "summary": "A totally normal example",
#         "description": "A **normal** user works correctly.",
#         "value": {
#             "user_id": "user_2137",
#             "name": "John",
#             "email": "john.paul@second.pl",
#         },
#     },
#     "user_69": {
#         "summary": "For some people normal example",
#         "description": "A **'normal'** user works correctly.",
#         "value": {
#             "user_id": "user_69",
#             "name": "Jeffrey",
#             "email": "jeffrey.epstein@loveisland.vi",
#         },
#     },
#     "austrian painter": {
#         "summary": "For most people not a normal example",
#         "description": "A **not normal** user but still works correctly.",
#         "value": {
#             "user_id": "user_1939",
#             "name": "Adolf",
#             "email": "adolf.h@academy.fine.arts.at",
#         },
#     },
# }

users_get_user = {
    200: {
        "description": "User found and returned",
        "content": {
            "application/json": {
                "examples": {**user_2137, **user_69, **austrian_painter}
            }
        },
    },
    "4xx": {
        "description": "4xx Status code returned",
        "content": {
            "application/json": {
                "examples": exceptions.api.ApiError._api_errors
            }
        },
    },
    500: {"description": "Internal server error"},
}

users_create_user = {
    201: {
        "description": "User found and returned",
        "content": {
            "application/json": {
                "examples": {**user_2137, **user_69, **austrian_painter}
            }
        },
    },
    "4xx": {
        "description": "4xx Status code returned",
        "content": {
            "application/json": {
                "examples": exceptions.api.ApiError._api_errors
            }
        },
    },
    500: {"description": "Internal server error"},
}

users_get_many_users = {
    200: {
        "description": "User found for query or no matches for query",
        "content": {
            "application/json": {
                "examples": {
                    "all_users": {
                        "summary": "All users exampke",
                        "description": "Returning all users.",
                        "value": [
                            {
                                "user_id": "user_2137",
                                "name": "John",
                                "email": "john.paul@second.pl",
                            },
                            {
                                "user_id": "user_69",
                                "name": "Jeffrey",
                                "email": "jeffrey.epstein@loveisland.vi",
                            },
                            {
                                "user_id": "user_1939",
                                "name": "Adolf",
                                "email": "adolf.h@academy.fine.arts.at",
                            },
                        ],
                    },
                    "no_users_matching_query": {
                        "summary": "No users matching query",
                        "description": "No users found for requested query",
                        "value": [],
                    },
                }
            }
        },
    },
    "4xx": {
        "description": "4xx Status code returned",
        "content": {
            "application/json": {
                "examples": exceptions.api.ApiError._api_errors
            }
        },
    },
    500: {"description": "Internal server error"},
}

users_delete_user = {
    "4xx": {
        "description": "4xx Status code returned",
        "content": {
            "application/json": {
                "examples": exceptions.api.ApiError._api_errors
            }
        },
    },
    500: {"description": "Internal server error"},
}
