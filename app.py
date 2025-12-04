import streamlit as st
import pandas as pd
from utils import login_user, register_user, normalize_text, save_to_history, fetch_history

# ============================================
# PAGE CONFIG
# ============================================
st.set_page_config(
    page_title="AI Claim Normalizer",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================
# CUSTOM CSS
# ============================================
st.markdown("""
<style>
/* Global styling */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

/* Glass container */
.glass {
    background: rgba(255, 255, 255, 0.55);
    padding: 25px;
    border-radius: 18px;
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.25);
    box-shadow: 0 8px 20px rgba(0,0,0,0.08);
}

/* Dark mode compensation */
.darkmode .glass {
    background: rgba(40,40,40,0.45);
    border: 1px solid rgba(255,255,255,0.1);
}

/* Metrics */
.metric-card {
    background: white;
    padding: 22px;
    border-radius: 16px;
    border: 1px solid #eee;
    text-align: center;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}
.metric-value {
    font-size: 34px;
    font-weight: 700;
}
.darkmode .metric-card {
    background: #1f1f1f;
    border: 1px solid #444;
}
</style>
""", unsafe_allow_html=True)

# ============================================
# DARK MODE TOGGLE
# ============================================
dark = st.sidebar.toggle("🌙 Dark Mode")

if dark:
    st.markdown("<script>document.body.classList.add('darkmode');</script>", unsafe_allow_html=True)
else:
    st.markdown("<script>document.body.classList.remove('darkmode');</script>", unsafe_allow_html=True)

# ============================================
# SIDEBAR
# ============================================
st.sidebar.title("Navigation")
menu = st.sidebar.radio(
    "Go to:",
    ["Login", "Process Claims", "History", "About"],
    index=0 if "user" not in st.session_state or st.session_state.user is None else 1
)

# ============================================
# SESSION INIT
# ============================================
if "user" not in st.session_state:
    st.session_state.user = None

# ============================================
# LOGIN PAGE
# ============================================
if menu == "Login" and st.session_state.user is None:

    st.markdown("<h2 style='text-align:center;'>🔐 Login / Create Account</h2>", unsafe_allow_html=True)

    with st.container():
        mode = st.radio("Choose:", ["Login", "Create Account"], horizontal=True)

        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        email = col1.text_input("📧 Email")
        pwd = col2.text_input("🔑 Password", type="password")
        submit = st.button("➡ Continue", width='stretch')
        st.markdown("</div>", unsafe_allow_html=True)

        if submit:
            if mode == "Create Account":
                _, err = register_user(email, pwd)
                if err:
                    st.error(err)
                else:
                    st.success("🎉 Account created! Please log in.")
            else:
                user, err = login_user(email, pwd)
                if err:
                    st.error("❌ " + err)
                else:
                    st.session_state.user = user
                    st.success("✅ Login successful!")
                    st.rerun()
    st.stop()

# ============================================
# BLOCK ACCESS IF NOT LOGGED IN
# ============================================
if st.session_state.user is None:
    st.warning("⚠ Please login to continue.")
    st.stop()

# ============================================
# AFTER LOGIN HEADER
# ============================================
st.success(f"Welcome, **{st.session_state.user['email']}** 🎉")

# =================================================
# PROCESS CLAIMS
# =================================================
if menu == "Process Claims":

    st.markdown("## ⚙️ Upload & Normalize Claims")

    uploaded = st.file_uploader("Upload CSV", type=["csv"])

    if uploaded:
        df = pd.read_csv(uploaded)

        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("### 📄 File Preview")
        st.dataframe(df, width='stretch', height=250)
        st.markdown("</div>", unsafe_allow_html=True)

        column = st.selectbox("Select column to normalize:", df.columns)

        if st.button("🚀 Normalize Now", width='stretch'):
            with st.spinner("⏳ Processing..."):

                results = []
                progress = st.progress(0)

                for idx, text in df[column].items():
                    cleaned = normalize_text(text)
                    results.append(cleaned)
                    # Debug print to verify history
                    print("Saving to history:", st.session_state.user["id"], text, cleaned)
                    save_to_history(st.session_state.user["id"], text, cleaned)
                    progress.progress((idx + 1) / len(df))

            df["Normalized_Claim"] = results

            # ======== Advanced Metrics =========
            df["Original_Length"] = df[column].astype(str).apply(len)
            df["Cleaned_Length"] = df["Normalized_Claim"].astype(str).apply(len)
            df["Reduction"] = df["Original_Length"] - df["Cleaned_Length"]
            df["Reduction_%"] = (df["Reduction"] / df["Original_Length"] * 100).round(1)

            st.success("🎉 All claims processed!")

            # Metric cards
            colA, colB, colC = st.columns(3)
            colA.metric("Total Claims", len(df))
            colB.metric("Avg Reduction", f"{df['Reduction'].mean():.1f} chars")
            colC.metric("Avg % Change", f"{df['Reduction_%'].mean():.1f}%")

            # Side-by-side comparison
            st.markdown("### 🔍 Comparison Table")
            st.dataframe(
                df[[column, "Normalized_Claim", "Reduction_%"]],
                width='stretch',
                height=350
            )

            st.download_button(
                "⬇ Download Result CSV",
                df.to_csv(index=False),
                "normalized_claims.csv",
                width='stretch'
            )

# =================================================
# HISTORY
# =================================================
elif menu == "History":

    st.markdown("## 📊 Your History")

    history = fetch_history(st.session_state.user["id"])

    if not history:
        st.info("📭 No history yet.")
    else:
        df_hist = pd.DataFrame(history)

        colA, colB = st.columns(2)
        colA.metric("Total Processed", len(df_hist))
        colB.metric("Latest Entry", df_hist['timestamp'].max())

        st.markdown("### 📜 Full Log")
        st.dataframe(df_hist, width='stretch', height=380)

        st.download_button(
            "⬇ Export History",
            df_hist.to_csv(index=False),
            "history.csv",
            width='stretch'
        )

# =================================================
# ABOUT PAGE
# =================================================
elif menu == "About":
    st.markdown("""
    ## ℹ️ About This App
    **AI-Powered Claims Text Normalizer**
    ✔ Cleans and standardizes claim descriptions
    ✔ Supports file uploads
    ✔ Keeps full processing history
    ✔ Sleek modern UI with metrics
    """)
