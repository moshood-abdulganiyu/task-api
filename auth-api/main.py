import os

from dotenv import load_dotenv
from fastapi import FastAPI, Request, Header
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

app = FastAPI(title="Auth API", version="1.0")


def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


def error(status_code: int, message: str):
    return JSONResponse(status_code=status_code, content={"error": message})


@app.exception_handler(RequestValidationError)
async def handle_validation_error(request: Request, exc: RequestValidationError):
    first = exc.errors()[0]
    where = ".".join(str(part) for part in first["loc"])
    return error(400, f"Invalid request - {where}: {first['msg']}")


def extract_token(authorization: str | None):
    """Return the token from 'Authorization: Bearer <token>', or None."""
    if not authorization:
        return None
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        return None
    return parts[1]


class Credentials(BaseModel):
    email: str | None = None
    password: str | None = None


get_supabase()
print("Server running and connected to Supabase")


@app.post("/auth/signup", status_code=201)
def signup(body: Credentials):
    """Create a new user account."""
    if not body.email or not body.password:
        return error(400, "email and password are required")
    try:
        result = get_supabase().auth.sign_up(
            {"email": body.email.strip(), "password": body.password}
        )
    except Exception as exc:
        return error(400, f"Signup failed: {exc}")
    if result.user is None:
        return error(400, "Signup failed")
    user = result.user
    return {"id": user.id, "email": user.email, "created_at": user.created_at}


@app.post("/auth/login")
def login(body: Credentials):
    """Log in and receive an access token and a refresh token."""
    if not body.email or not body.password:
        return error(400, "email and password are required")
    try:
        result = get_supabase().auth.sign_in_with_password(
            {"email": body.email.strip(), "password": body.password}
        )
    except Exception:
        return error(401, "Invalid login credentials")
    if result.session is None:
        return error(401, "Invalid login credentials")
    session = result.session
    return {
        "access_token": session.access_token,
        "refresh_token": session.refresh_token,
        "token_type": "bearer",
        "expires_in": session.expires_in,
    }


@app.get("/public/info")
def public_info():
    """Open to everyone."""
    return {"message": "Welcome stranger! This info is public."}


@app.get("/protected/profile")
def profile(authorization: str | None = Header(default=None)):
    """Needs a bearer token (not yet verified)."""
    token = extract_token(authorization)
    if token is None:
        return error(401, "Access token required")
    return {"message": "A token was presented (not verified yet)"}


