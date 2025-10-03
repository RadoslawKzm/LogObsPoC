import pydantic


class Page(pydantic.BaseModel):
    page_num: int
    page_size: int
    total_items: int
    next_page: pydantic.HttpUrl | None = None
    previous_page: pydantic.HttpUrl | None = None
