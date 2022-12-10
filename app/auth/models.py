import datetime
import ormar

from ormar.queryset.queryset import QuerySet
from fastapi import HTTPException
from app.stores import BaseMeta
from app.models import DateTimeFieldsMixins


class NoGetTarget(QuerySet):

    async def first_or_404(self, *args, **kwargs):
        entity = await self.get_or_none(*args, **kwargs)
        if entity is None:
            # in fastapi or starlette
            raise HTTPException(404)


class Auth(ormar.Model):

    class Meta(BaseMeta):
        tablename: str = 'auth'
        queryset_class = NoGetTarget

    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    email: str = ormar.String(max_length=254)
    username: str = ormar.String(max_length=150)
    password: str = ormar.String(max_length=128)
    first_name: str = ormar.String(max_length=150, nullable=True)
    last_name: str = ormar.String(max_length=150, nullable=True)
    is_staff: bool = ormar.Boolean(default=False)
    is_active: bool = ormar.Boolean(default=False)
    date_joined: datetime = ormar.DateTime(default=datetime.datetime.utcnow())
    last_login: datetime = ormar.DateTime(default=datetime.datetime.utcnow(), onupdate=datetime.datetime.utcnow())


class OutstandingToken(ormar.Model):
    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    user: Auth = ormar.ForeignKey(Auth, name='user_id')
    jti: str = ormar.String(max_length=255)
    token = ormar.Text()
    created_at: datetime = ormar.DateTime(default=datetime.datetime.utcnow())
    expires_at = ormar.DateTime()

    class Meta(BaseMeta):
        tablename: str = 'account_jwt_token'
        orders_by = ['user',]

    def __str__(self):
        return 'Token for {} ({})'.format(
            self.user,
        )


class BlacklistedToken(ormar.Model):
    id: int = ormar.Integer(primary_key=True, autoincrement=True)
    token: OutstandingToken = ormar.ForeignKey(OutstandingToken, name='token_id')
    blacklisted_at = ormar.DateTime(default=datetime.datetime.utcnow())

    class Meta(BaseMeta):
        db_table = 'account_black_list_token'

    def __str__(self):
        return f'Blacklisted token for {self.token.user}'
