import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set.")

HOST = os.getenv("HOST")
if not HOST:
    raise ValueError("HOST environment variable is not set.")

PORT = os.getenv("PORT")
if not PORT:
    raise ValueError("PORT environment variable is not set.")