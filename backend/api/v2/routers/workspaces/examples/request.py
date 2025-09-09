project_id: dict[str, dict[str, str]] = {
    "example name 1": {"value": "1337"},
    "example name 2": {"value": "2137"},
}


users: dict[str, dict[str, str | dict[str, str]]] = {
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
