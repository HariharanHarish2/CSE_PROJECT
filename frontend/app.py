import streamlit as st
import requests
import pandas as pd
import json

# ==========================================
# CONSTANTS & CONFIG
# ==========================================
API_URL = "https://sql-ai-chatbox.vercel.app"

st.set_page_config(
    page_title="HNV AI - Intelligent NL2SQL", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================
# CUSTOM CSS FOR CHATGPT ULTRA PREMIUM (DESKTOP)
# ==========================================
def inject_custom_css():
    st.markdown("""
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&family=Inter:wght@400;600&display=swap');
        
        :root {
            --sidebar-bg: #000000;
            --chat-bg: #030712;
            --accent: #10b981; 
            --glass: rgba(255, 255, 255, 0.03);
            --border: rgba(255, 255, 255, 0.1);
        }

        .stApp {
            background: radial-gradient(circle at center, #111827, #030712);
            color: #f8fafc;
            font-family: 'Outfit', sans-serif;
        }

        /* Pulse Cards Styling */
        .pulse-card {
            background: rgba(16, 185, 129, 0.05);
            border: 1px solid rgba(16, 185, 129, 0.2);
            border-radius: 12px;
            padding: 10px;
            text-align: center;
        }
        .pulse-val {
            font-size: 1.5rem;
            font-weight: 700;
            color: #10b981;
        }
        .pulse-lbl {
            font-size: 0.7rem;
            color: #94a3b8;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        /* ChatGPT Sidebar Styling */
        [data-testid="stSidebar"] {
            background: var(--sidebar-bg);
            border-right: 1px solid var(--border);
        }

        /* History Item Styling */
        .history-item {
            padding: 10px;
            border-radius: 8px;
            margin-bottom: 5px;
            cursor: pointer;
            font-size: 0.9rem;
            color: #94a3b8;
            transition: all 0.2s;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .history-item:hover {
            background: rgba(255,255,255,0.05);
            color: white;
        }

        /* 3D Glass Cards */
        .premium-card {
            background: var(--glass);
            backdrop-filter: blur(10px);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 20px;
            box-shadow: 0 8px 32px 0 rgba(0,0,0,0.8);
            margin-bottom: 20px;
        }

        /* Floating Input */
        .stChatInputContainer {
            background: rgba(15, 23, 42, 0.9) !important;
            border: 1px solid #334155 !important;
            border-radius: 40px !important;
            max-width: 800px;
            margin: 0 auto !important;
        }

        /* Connection Flow Stepper */
        .step-container {
            display: flex;
            justify-content: space-between;
            margin: 20px 0;
            padding: 15px;
            background: rgba(16, 185, 129, 0.05);
            border-radius: 12px;
            border: 1px dashed var(--accent);
        }
        .step {
            text-align: center;
            font-size: 0.8rem;
            color: #64748b;
        }
        .step.active {
            color: var(--accent);
            font-weight: 600;
        }
        /* Hide Streamlit Default UI (Deploy button, Menu, etc.) */
        header {visibility: hidden;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display:none;}

        /* Floating User Profile Corner */
        .user-corner {
            position: fixed;
            top: 15px;
            right: 25px;
            z-index: 9999;
            background: rgba(16, 185, 129, 0.1);
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            padding: 8px 15px;
            border-radius: 30px;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        .user-avatar {
            width: 30px;
            height: 30px;
            background: var(--accent);
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 700;
            color: black;
            font-size: 0.8rem;
        }
        
        /* Buttons */
        .stButton > button {
            border-radius: 12px;
            border: 1px solid #334155;
            background: #111827;
            color: white;
            transition: 0.3s;
        }
        .stButton > button:hover {
            border-color: var(--accent);
            box-shadow: 0 0 15px rgba(16, 185, 129, 0.3);
        }
        </style>
    """, unsafe_allow_html=True)

inject_custom_css()

# Initialize Session State
if "messages" not in st.session_state: st.session_state.messages = []
if "history" not in st.session_state: st.session_state.history = ["Check employee salaries", "Analyze project budgets", "Student grade report"]
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = "Demo User"

# ==========================================
# ChatGPT-STYLE LOGIN (OPEN ACCESS)
# ==========================================
if not st.session_state.logged_in:
    st.markdown("""
        <div style='text-align: center; margin-top: 12vh;'>
            <img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' width='60' style='margin-bottom: 20px; filter: drop-shadow(0 0 10px rgba(16,185,129,0.5));'>
            <h2 style='color: white; font-weight: 600; margin-bottom: 5px;'>Welcome to HNV AI</h2>
            <p style='color: #94a3b8; margin-bottom: 30px;'>Sign in to your intelligent data account to continue</p>
        </div>
    """, unsafe_allow_html=True)
    
    with st.container():
        # Centered Login Box
        _, login_col, _ = st.columns([1, 2, 1])
        with login_col:
            st.markdown("<div class='premium-card' style='padding: 30px; border-radius: 12px;'>", unsafe_allow_html=True)
            login_user = st.text_input("Email address or Username", placeholder="e.g. John Doe")
            login_pass = st.text_input("Password", type="password", placeholder="••••••••")
            
            # OpenAI-style colored button
            if st.button("Continue", use_container_width=True):
                if login_user and login_pass: 
                    st.session_state.logged_in = True
                    st.session_state.username = login_user
                    st.rerun()
                else:
                    st.warning("Please enter credentials to start your session.")
            
            st.markdown("<p style='text-align:center; color:#64748b; font-size:0.8rem; margin-top:20px;'>Don't have an account? <span style='color:#10b981; cursor:pointer;'>Sign up</span></p>", unsafe_allow_html=True)
            st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# Floating Logout / User Info Corner
st.markdown(f"""
    <div class='user-corner'>
        <div class='user-avatar'>{st.session_state.username[0].upper()}</div>
        <div style='font-size: 0.8rem; font-weight: 600;'>{st.session_state.username}</div>
    </div>
""", unsafe_allow_html=True)

# Add logout button in sidebar for clear UX
with st.sidebar:
    st.markdown("---")
    if st.button("🚪 System Logout", use_container_width=True):
        st.session_state.logged_in = False
        st.rerun()

# ==========================================
# SIDEBAR REFACTOR (ChatGPT-STYLE)
# ==========================================
with st.sidebar:
    st.markdown("### 💠 HNV AI Core")
    
    if st.button("➕ New Chat", use_container_width=True):
        try:
            requests.delete(f"{API_URL}/memory")
        except:
            pass
        st.session_state.messages = []
        st.session_state.current_prompt = None
        st.rerun()

    st.markdown("---")
    st.markdown("#### 🕒 Recent History")
    for idx, h in enumerate(st.session_state.history):
        if st.button(f"🗨️ {h[:25]}...", key=f"hist_{idx}", use_container_width=True, help=h):
            st.session_state.messages = []
            st.session_state.current_prompt = h
            st.rerun()

    st.markdown("---")
    st.markdown("#### 📝 System Insights")
    st.info("🔓 **Free Local Core**: This is an open-source engine running entirely on your machine. No premium subscription or API key required for core data tasks.")

    st.markdown("---")
    st.markdown("#### 🔒 Privacy Mode")
    st.success("Data remains local in `company.db`")

# ==========================================
# PAGE: HOME (DESKTOP DASHBOARD MODE)
# ==========================================
# AI Guide Avatar (3D Effect)
col_a, col_b = st.columns([0.2, 0.8])
with col_a:
    st.markdown("""
        <div style='perspective: 1000px;'>
            <img src='https://cdn-icons-png.flaticon.com/512/4712/4712035.png' width='120' 
                 style='filter: drop-shadow(0 20px 30px rgba(16,185,129,0.4)); transform: rotateY(-10deg);'>
        </div>
    """, unsafe_allow_html=True)
with col_b:
    st.markdown("<h1 style='margin-bottom: 0; color: #10b981 !important;'>HNV AI: Cognitive Layer</h1>", unsafe_allow_html=True)
    st.info("👋 **I'm HNV AI.** Click a dashboard initiative below or type a custom complex query. I'll transform it into SQL and filter your results instantly.")

st.markdown("---")

# 1. Live System Pulse (New Feature)
try:
    stats_res = requests.get(f"{API_URL}/stats").json()
    p_cols = st.columns(4)
    with p_cols[0]:
        st.markdown(f"<div class='pulse-card'><div class='pulse-val'>{stats_res.get('employees', 0)}</div><div class='pulse-lbl'>Active Nodes</div></div>", unsafe_allow_html=True)
    with p_cols[1]:
        st.markdown(f"<div class='pulse-card'><div class='pulse-val'>{stats_res.get('students', 0)}</div><div class='pulse-lbl'>Enrolled Pupils</div></div>", unsafe_allow_html=True)
    with p_cols[2]:
        st.markdown(f"<div class='pulse-card'><div class='pulse-val'>{stats_res.get('projects', 0)}</div><div class='pulse-lbl'>Active Initiatives</div></div>", unsafe_allow_html=True)
    with p_cols[3]:
        st.markdown(f"<div class='pulse-card'><div class='pulse-val'>{stats_res.get('departments', 0)}</div><div class='pulse-lbl'>Dept Clusters</div></div>", unsafe_allow_html=True)
except:
    pass

st.markdown("---")

# 2. Persistent Dashboard (Descriptive Queries)
st.markdown("### 💠 Interactive Data Initiatives")
q_cols1 = st.columns(3)
q_cols2 = st.columns(3)

queries = [
    ("🚀 Show All Projects", "show all projects including budget and status"),
    ("👥 Staff Directory", "list all employees with their roles and departments"),
    ("🎓 Student Table", "show all students and their academic grades"),
    ("🏢 Dept Overview", "list all departments and office locations"),
    ("💰 Total Budget", "calculate the total salary budget for the company"),
    ("⭐ Peak Earner", "who is the highest paid worker and what is their role?")
]

# Row 1
for idx, (label, q_text) in enumerate(queries[:3]):
    if q_cols1[idx].button(label, key=f"dash_{idx}", use_container_width=True):
        st.session_state.messages = [] 
        st.session_state.current_prompt = q_text
        st.rerun()

# Row 2
for idx, (label, q_text) in enumerate(queries[3:]):
    if q_cols2[idx].button(label, key=f"dash_{idx+3}", use_container_width=True):
        st.session_state.messages = []
        st.session_state.current_prompt = q_text
        st.rerun()

st.markdown("---")

# 2. Results / Chat Area
if not st.session_state.get("messages") and not st.session_state.get("current_prompt"):
    st.markdown("""
        <div style='text-align: center; padding: 40px; border: 1px solid rgba(16,185,129,0.2); border-radius: 24px; background: rgba(16,185,129,0.02); box-shadow: inset 0 0 20px rgba(0,0,0,0.5);'>
            <h4 style='color: #94a3b8;'>Select an Initiative to Begin</h4>
            <p style='color: #64748b; font-size: 0.9rem;'>The AI is connected to <b>company.db</b> and ready to synthesize queries.</p>
        </div>
    """, unsafe_allow_html=True)

# Connection Flow Stepper
if st.session_state.get("messages"):
    st.markdown("""
        <div class='step-container'>
            <div class='step active'>🏢 Data Connected</div>
            <div class='step active'>⚡ Neural Filtered</div>
            <div class='step active'>📊 Result Logic Array</div>
        </div>
    """, unsafe_allow_html=True)

# Display Messages as Premium Cards
for i, msg in enumerate(st.session_state.messages):
    is_user = msg["role"] == "user"
    
    if is_user:
        st.markdown(f"<div style='margin: 15px 0 5px 0; color: #10b981; font-family: Inter;'><b>[PROMPT]</b> {msg['content']}</div>", unsafe_allow_html=True)
    else:
        with st.container():
            st.markdown(f"<div class='premium-card' style='border-left: 4px solid #10b981; transform: translateZ(10px);'>", unsafe_allow_html=True)
            st.markdown(f"**🤖 AI ANALYSIS:** {msg['content']}")
            
            if "data" in msg:
                data = msg["data"]
                if data.get("results") and not data.get("results").get("error"):
                    df = pd.DataFrame(data["results"]["rows"], columns=data["results"]["columns"])
                    
                    if "status" in df.columns:
                        df['status'] = df['status'].apply(lambda x: f"🚀 {x}" if "Active" in x or "Running" in x else f"⚪ {x}")
                    if "role" in df.columns:
                        df['role'] = df['role'].apply(lambda x: f"👥 {x}")
                    
                    st.dataframe(df, use_container_width=True, hide_index=True)
                    
                    # New Feature: Export & Visualize
                    ctrl_col1, ctrl_col2 = st.columns([0.5, 0.5])
                    with ctrl_col1:
                        csv = df.to_csv(index=False).encode('utf-8')
                        st.download_button(label="📥 Export Result (CSV)", data=csv, file_name='ai_extraction.csv', mime='text/csv')
                    
                    with ctrl_col2:
                        if st.checkbox("📊 Neural Visualizer", key=f"viz_{i}"):
                            # Try to find a numeric column for visualization
                            num_cols = df.select_dtypes(include=['number']).columns.tolist()
                            if num_cols and len(df) > 1:
                                label_col = next((c for c in df.columns if c not in num_cols), df.columns[0])
                                plot_df = df.set_index(label_col)[num_cols[0]]
                                st.bar_chart(plot_df)
                            else:
                                st.warning("Requires numeric values for chart.")

                with st.expander("🛠️ View Neural SQL Synthesis"):
                    st.code(data.get('generated_sql'), language='sql')
                    st.caption(f"Cognitive Path: {data.get('reasoning')}")
            st.markdown("</div>", unsafe_allow_html=True)

# Main Interaction Logic
input_prompt = st.chat_input("Synthesize new data query...")
trigger_prompt = st.session_state.get('current_prompt')
final_prompt = input_prompt or trigger_prompt

if final_prompt:
    if trigger_prompt: st.session_state.current_prompt = None
    
    if final_prompt not in st.session_state.history:
        st.session_state.history.insert(0, final_prompt)
        st.session_state.history = st.session_state.history[:5]

    st.session_state.messages.append({"role": "user", "content": final_prompt})
    
    with st.spinner("🧠 Synthesizing Neural Query..."):
        try:
            response = requests.post(f"{API_URL}/chat", json={"query": final_prompt})
            if response.status_code == 200:
                payload = response.json()
                st.session_state.messages.append({"role": "assistant", "content": payload.get("explanation"), "data": payload})
            else:
                st.error("Synthesizer Error: Backend Connection Lost")
        except Exception as e:
            st.error(f"Error: {e}")
    st.rerun()
