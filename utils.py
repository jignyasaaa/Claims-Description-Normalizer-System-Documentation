import os
import bcrypt
import pandas as pd
import google.generativeai as genai
from supabase import create_client, Client

# =====================================================
# LOAD ENVIRONMENT KEYS
# =====================================================
GEMINI_KEY = os.getenv("GEMINI_API_KEY")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

# Gemini Config
genai.configure(api_key=GEMINI_KEY)

# Connect Supabase
db_enabled = SUPABASE_URL not in [None, "", "YOUR_SUPABASE_URL"]
supabase = create_client(SUPABASE_URL, SUPABASE_KEY) if db_enabled else None


# =====================================================
# AUTH FUNCTIONS
# =====================================================
def register_user(email, password):
    if not db_enabled:
        return None, "⚠ Database Disabled — running in demo mode."

    hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    exists = supabase.table("users").select("*").eq("email", email).execute()
    if exists.data:
        return None, "User already exists."

    res = supabase.table("users").insert({
        "email": email,
        "password_hash": hashed_pw
    }).execute()

    return res.data, None


def login_user(email, password):
    if not db_enabled:
        return {"email": email, "id": "demo_user"}, None

    res = supabase.table("users").select("*").eq("email", email).execute()

    if not res.data:
        return None, "User not found."

    user_data = res.data[0]

    if bcrypt.checkpw(password.encode(), user_data["password_hash"].encode()):
        return user_data, None

    return None, "Incorrect password."


# =====================================================
# GEMINI NORMALIZATION
# =====================================================
def normalize_text(text):
    """
    Uses Google Gemini to professionally normalize messy claim descriptions.
    """
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(
            f"Rewrite this insurance claim professionally and clearly:\n\n{text}"
        )
        return response.text.strip()

    except Exception as e:
        return f"[AI ERROR] {e}"


# =====================================================
# SAVE TO SUPABASE
# =====================================================
def save_to_history(user_id, original, normalized):
    if db_enabled:
        try:
            supabase.table("claims").insert({
                "user_id": user_id,
                "original_text": original,
                "normalized_text": normalized,
                "status": "processed"
            }).execute()
        except Exception as e:
            print("❌ Error saving to Supabase:", e)


# =====================================================
# FETCH USER HISTORY
# =====================================================
def fetch_history(user_id):
    if not db_enabled:
        return []
    try:
        res = supabase.table("claims") \
            .select("*") \
            .eq("user_id", user_id) \
            .order("created_at", desc=True) \
            .execute()

        return res.data
    except Exception as e:
        print("❌ Error fetching history:", e)
        return []
