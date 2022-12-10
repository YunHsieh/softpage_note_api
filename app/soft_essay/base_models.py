from pydantic import BaseModel, validator
from app.soft_essay.models import Softessay_Essay, Softessay_Topic
from app.auth.models import Auth


def validator_read_auth(data):
    if data:
        return {k:v for k, v in data.dict().items() if k in {'id', 'username', 'email'}}


class _Essay(BaseModel):
    __fields__ = Softessay_Essay.__fields__


class Essay(_Essay):
    title: str
    tags: list


class Read_Essays(_Essay):
    class Config:
        orm_mode = True

    title: Softessay_Topic
    version: str
    order_seq: list
    forker: Auth | None
    author: Auth | None

    _validator_read_auth = validator('forker', allow_reuse=True)(validator_read_auth)
    _validator_read_auth = validator('author', allow_reuse=True)(validator_read_auth)
    @validator('title')
    def name_to_str(cls, v, values, **kwargs):
        return v.name


class Query_Essays(BaseModel):
    author: int | None
    forker: int | None
    is_published: bool | None
    is_deleted: bool | None
