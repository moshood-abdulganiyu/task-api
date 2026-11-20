import os

from dotenv import load_dotenv
from fastapi import FastAPI
from supabase import Client, create_client

load_dotenv()

SUPABASE_URL = os.environ["SUPABASE_URL"]
SUPABASE_KEY = os.environ["SUPABASE_KEY"]

app = FastAPI(title="Auth API", version="1.0")


def get_supabase() -> Client:
    return create_client(SUPABASE_URL, SUPABASE_KEY)


get_supabase()
print("Server running and connected to Supabase")
