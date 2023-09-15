from fastapi_login import LoginManager
from fastapi_sqlalchemy import db
from apps.api.admin.models import User
from apps.core.config import SECRET_KEY, TOKEN_URL
from fastapi import Request
from starlette.responses import RedirectResponse

# Fastapi-login 令牌失效重定向

class NotAuthenticatedException(Exception):
    pass

def auth_exception_handler(request: Request, exc: NotAuthenticatedException):
    """
    Redirect the user to the login page if not logged in
    """
    return RedirectResponse(url=TOKEN_URL)
    

manager = LoginManager(SECRET_KEY, token_url=TOKEN_URL, use_cookie=True)
manager.not_authenticated_exception = NotAuthenticatedException


@manager.user_loader
def load_user(username: str):  # could also be an asynchronous function
    user = db.session.query(User).filter_by(username=username).first()
    return user