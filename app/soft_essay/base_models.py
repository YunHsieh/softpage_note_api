from pydantic import BaseModel, validator, Field
from app.soft_essay.models import Softessay_Essay, Softessay_Topic
from app.auth.models import Auth

_Essay = Softessay_Essay.get_pydantic(exclude={
    # HACK: the tags and order_seq are not work.
    # 'tags',
    # 'order_seq',
    'softessay_bodys', 
    'softessay_comments',
})


def validator_read_auth(data):
    allow_fiedls = {'id', 'username', 'email'}
    if data:
        return {k: v for k, v in data.dict().items() if k in allow_fiedls}


class UserInfo(Auth):
    author: str = None
    password: str = None


class Create_Essay(_Essay):
    title: str = Field(..., min_length=1)
    content: str = ''
    tags: list = []
    order_seq: list = []

    author: UserInfo | None

    _validator_read_auth = validator('author', allow_reuse=True)(validator_read_auth)


class Read_Essays(_Essay):
    class Config:
        orm_mode = True

    title: Softessay_Topic
    order_seq: list
    author: Auth | None

    _validator_read_auth = validator('author', allow_reuse=True)(validator_read_auth)

    @validator('title')
    def name_to_str(cls, v, values, **kwargs):
        return v.name


class Query_Essays(BaseModel):
    author: int | None
    forker: int | None
    is_published: bool | None
    is_deleted: bool | None
