import uuid
import ormar

from app.auth.models import Auth
from app.stores import BaseMeta
from app.models import DateTimeFieldsMixins
from sqlalchemy import func
from typing import ForwardRef
from fastapi import HTTPException
from ormar.queryset.queryset import QuerySet
from ormar import property_field

Softessay_BodyRef = ForwardRef('Softessay_Body')
Softessay_CommentRef = ForwardRef('Softessay_Comment')

class NoGetTarget(QuerySet):

    async def first_or_404(self, *args, **kwargs):
        entity = await self.get_or_none(*args, **kwargs)
        if entity is None:
            # in fastapi or starlette
            raise HTTPException(404)


class Softessay_Topic(ormar.Model, DateTimeFieldsMixins):

    class Meta(BaseMeta):
        tablename: str = 'softessay_topic'
        queryset_class = NoGetTarget

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    name: str = ormar.String(max_length=256)

    # @property_field
    # def prefixed_name(self):
    #     return self.name


class Softessay_Tag(ormar.Model, DateTimeFieldsMixins):

    class Meta(BaseMeta):
        tablename: str = 'softessay_tag'
        queryset_class = NoGetTarget

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    name: str = ormar.String(max_length=256)


class EssayTag(ormar.Model):
    class Meta(BaseMeta):
        tablename = 'essay_x_tag'

    id: int = ormar.Integer(primary_key=True)


class Softessay_Essay(ormar.Model, DateTimeFieldsMixins):

    class Meta(BaseMeta):
        tablename: str = 'softessay_essay'
        queryset_class = NoGetTarget

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    title: Softessay_Topic = ormar.ForeignKey(Softessay_Topic, name='title_id')
    version: str = ormar.String(max_length=32, nullable=True)
    content: str = ormar.Text()
    is_published: bool = ormar.Boolean(default=True)
    is_deleted: bool = ormar.Boolean(default=False)
    order_seq: dict = ormar.JSON(default=[])
    tags: Softessay_Tag = ormar.ManyToMany(Softessay_Tag, 
        through=EssayTag, 
        through_relation_name='essay_id', 
        through_reverse_relation_name='tag_id'
    )
    forker: Auth = ormar.ForeignKey(Auth, related_name='forker', name='forker_id', nullable=True)
    author: Auth = ormar.ForeignKey(Auth, related_name='author', name='author_id')


class Softessay_Body(ormar.Model, DateTimeFieldsMixins):

    class Meta(BaseMeta):
        tablename: str = 'softessay_body'
        queryset_class = NoGetTarget

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    last_version: Softessay_BodyRef = ormar.ForeignKey(Softessay_BodyRef, nullable=True, name='last_version_id')
    content: str = ormar.Text()
    essay: Softessay_Essay = ormar.ForeignKey(Softessay_Essay, name='essay_id')


class Softessay_Comment(ormar.Model, DateTimeFieldsMixins):

    class Meta(BaseMeta):
        tablename: str = 'softessay_comment'
        queryset_class = NoGetTarget

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    last_comment: Softessay_CommentRef = ormar.ForeignKey(Softessay_CommentRef, nullable=True, name='last_comment_id')
    comment: str = ormar.Text()
    essay: Softessay_Essay = ormar.ForeignKey(Softessay_Essay, nullable=True, name='essay_id')


Softessay_Comment.update_forward_refs()
Softessay_Body.update_forward_refs()
