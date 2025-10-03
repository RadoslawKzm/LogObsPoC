import pydantic


class Record(pydantic.BaseModel):
    filename: str
    content: bytes | bool = None
