# 🧾 Claims Description Normalizer System Documentation

This project is a **Claims Description Normalizer** that uses **Generative AI** (OpenAI GPT) to clean and standardize insurance claim descriptions.  
It allows users to upload CSV files, normalize text, track history, and download results — all through an interactive **Streamlit** web app.  

Live Demo: [Click here to open the app](https://usa-excited-brief-dispatched.trycloudflare.com/)

---

## **🚀 Features**
- **User Authentication** (Login / Sign Up)
- **CSV Upload & AI Normalization**
- **Download Normalized Results**
- **User History Tracking** via Supabase
- **Cloud Deployment** with Cloudflare Tunnel
- **Secure Handling of API Keys** (OpenAI & Supabase)
- ---

## **💻 Technologies Used**
- **Frontend:** Streamlit  
- **Backend / Logic:** Python (`utils.py`)  
- **Generative AI:** OpenAI GPT-3.5-turbo  
- **Database:** Supabase (PostgreSQL)  
- **Data Processing:** pandas  
- **Security:** bcrypt for password hashing  
- **Deployment / Tunneling:** Cloudflare Tunnel  
- **Environment Management:** python-dotenv  

---

## **📂 Project Structure**
├── app.py # Streamlit app

├── utils.py # Backend functions: auth, AI, DB

├── sample_claims.csv # Sample CSV for testing

├── requirements.txt # Python dependencies

└── README.md # Project documentation
---

## **⚙️ Setup Instructions**

### 1. Clone the repository
git clone https://github.com/yourusername/claims-normalizer.git
cd claims-normalizer

### 2. Create a .env file (locally)
Do not commit .env to GitHub. Add your real keys:.env

OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXX

SUPABASE_URL=https://your-project.supabase.co

SUPABASE_KEY=sb_publishable_XXXXXXXXXXXXXXXX

### 3. Install dependencies
pip install -r requirements.txt
or
pip install streamlit pandas openai supabase pyngrok python-dotenv bcrypt cloudflare

### 4. Run the app
streamlit run app.py
If using Cloudflare Tunnel in Colab:
!cloudflared tunnel --url http://localhost:8501 --no-autoupdate

📝 Usage
Login or sign up as a new user.

Upload a CSV file containing claim descriptions.

Select the column containing claims.

Click “Normalize Text” to generate cleaned claims using AI.

Download the results as a CSV.

View your processing history within the app.

🔒 Security Best Practices
Replace real API keys in code with placeholders before pushing to GitHub:

python
Copy code
os.environ["OPENAI_API_KEY"] = "YOUR_OPENAI_KEY"
os.environ["SUPABASE_URL"] = "YOUR_SUPABASE_URL"
os.environ["SUPABASE_KEY"] = "YOUR_SUPABASE_KEY"
Keep real keys in a .env file or Colab session.

Add .env to .gitignore to avoid exposing secrets.

📈 Example CSV
sample_claims.csv is included for testing.

Format:

Claim_ID	Claim_Description
1	patient admitted w/ flu and fever
2	minor accident, car damage only

🎯 Outcome
Converts messy insurance claims into clean, standardized, professional text.

Fully functional project for portfolio, resume, or placement projects.

📄 References
Streamlit Documentation

Supabase Docs

OpenAI API

👨‍💻 Author

Jignyasa Lunkad

Email: jignyasa0703@gmail.com
