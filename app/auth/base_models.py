from pydantic import BaseModel


class Token(BaseModel):
    redirect_url: str | None
    access_token: str | None
    token_type: str | None
