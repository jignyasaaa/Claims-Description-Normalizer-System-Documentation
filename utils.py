import os
import bcrypt
import pandas as pd
import openai
from supabase import create_client, Client

# Load environment keys
openai.api_key = os.getenv("OPENAI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Connect to Supabase (Optional Mode)
db_enabled = SUPABASE_URL not in [None, "", "YOUR_SUPABASE_URL"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if db_enabled else None


# ---------------- AUTH ----------------
def register_user(email, password):
    if not db_enabled:
        return None, "⚠ Database disabled — running in demo mode."

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    exists = supabase.table("users").select("*").eq("email", email).execute()

    if exists.data:
        return None, "User already exists."

    res = supabase.table("users").insert({"email": email, "password_hash": hashed_pw}).execute()
    return res.data, None


def login_user(email, password):
    if not db_enabled:
        return {"email": email, "id": "demo_user"}, None

    res = supabase.table("users").select("*").eq("email", email).execute()

    if not res.data or len(res.data) == 0:
        return None, "User not found."

    user_data = res.data[0]  # safely get the first row

    if bcrypt.checkpw(password.encode(), user_data["password_hash"].encode()):
        return user_data, None
    return None, "Incorrect password."


# ---------------- AI NORMALIZATION ----------------
def normalize_text(text):
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Rewrite insurance claim text professionally, standardized and clean."},
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"[AI ERROR] {e}"


# ---------------- SAVE HISTORY ----------------
def save_to_history(user_id, original, normalized):
    if db_enabled:
        supabase.table("claims").insert({
            "user_id": user_id,
            "original_text": original,
            "normalized_text": normalized
        }).execute()


def fetch_history(user_id):
    if not db_enabled:
        return []
    return supabase.table("claims").select("*").eq("user_id", user_id).execute().data
