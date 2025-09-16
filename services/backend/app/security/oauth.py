from authlib.integrations.starlette_client import OAuth
from starlette.requests import Request

from app.core.config import settings

oauth = OAuth()

oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)

async def login(request: Request, redirect_name = None):
    redirect_uri = request.url_for("google_auth")
    if redirect_name is not None:
        redirect_uri = request.url_for(redirect_name)
    print("CLIENT ID:", settings.GOOGLE_CLIENT_ID)
    print("REDIRECT URI:", redirect_uri)
    return await oauth.google.authorize_redirect(request, redirect_uri)

async def auth(request: Request):
    token = await oauth.google.authorize_access_token(request)

    # Проверяем, есть ли id_token
    id_token = token.get("id_token")
    #print("ID_TOKEN:", id_token)
    user = token['userinfo']
    print("TOKEN:", token)
    print("USER:", user)
    #return {}
    # Теперь разбираем id_token
    #user = await oauth.google.userinfo(request, token)

    return {
        "provider": "google",
        "user": normalize_google_user(user),
        "token": token,
    }

def normalize_google_user(data: dict) -> dict:
    return {
        "id": data.get("sub"),
        "email": data.get("email"),
        "name": data.get("name"),
    }
