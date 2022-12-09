from fastapi import Depends
from app.dependencies import has_token_required
from app.soft_essay import essays as soft_essay_views
from app.beta import views as beta_views
from app.auth import login as login_views


def init_routers(app):
    app.include_router(
        login_views.router,
        prefix='/api',
        tags=['api', 'login'],
        responses={418: {'description': 'Bad Request'}},
    )
