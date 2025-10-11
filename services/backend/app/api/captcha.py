from app.core.config import settings
import httpx

async def is_valid_captcha(token: str, action: str) -> bool:
    async with httpx.AsyncClient() as client:
        r = await client.post(
            "https://www.google.com/recaptcha/api/siteverify",
            data={"secret": settings.RECAPTCHA_SECRET_KEY, "response": token}
        )
    result = r.json()
    if not result.get("success"):
        return False
    if result.get("action") != action:
        return False
    if result.get("score", 0) < 0.5:
        return False
    return True
