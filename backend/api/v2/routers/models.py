import pydantic
import typing


class Page(pydantic.BaseModel):
    page_num: int
    page_size: int
    total_items: int
    next_page: typing.Optional[pydantic.HttpUrl] = None
    previous_page: typing.Optional[pydantic.HttpUrl] = None
