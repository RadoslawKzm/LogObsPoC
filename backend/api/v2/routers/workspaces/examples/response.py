from backend import exceptions

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

users = {
    200: {
        "description": "User found and returned",
        "content": {"application/json": {"examples": users_dict}},
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
