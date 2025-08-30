import pydantic

class Record(pydantic.BaseModel):
    filename: str
    content: str | bool = None
