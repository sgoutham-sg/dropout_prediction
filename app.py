# """
# Step 6 + 7: Streamlit Frontend + What-If Simulator
# Run: streamlit run app.py
# """

# import streamlit as st
# import requests
# import json

# API_URL = "http://localhost:8000/predict"

# # ── Page config ───────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Student Dropout Predictor",
#     page_icon="🎓",
#     layout="wide",
# )

# st.markdown("""
# <style>
#     @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;600&display=swap');

#     html, body, [class*="css"] {
#         font-family: 'IBM Plex Sans', sans-serif;
#     }

#     .main { background-color: #0d0d0d; color: #e8e8e8; }

#     h1, h2, h3 { font-family: 'IBM Plex Mono', monospace; }

#     .stApp { background-color: #0d0d0d; }

#     .risk-card {
#         padding: 1.5rem;
#         border-radius: 4px;
#         margin-bottom: 1rem;
#         font-family: 'IBM Plex Mono', monospace;
#     }
#     .risk-low    { background: #0a2e1a; border-left: 4px solid #00e676; color: #00e676; }
#     .risk-medium { background: #2e1f00; border-left: 4px solid #ffb300; color: #ffb300; }
#     .risk-high   { background: #2e0a0a; border-left: 4px solid #ff1744; color: #ff1744; }

#     .factor-tag {
#         display: inline-block;
#         background: #1a1a2e;
#         border: 1px solid #3a3a6e;
#         padding: 4px 12px;
#         border-radius: 2px;
#         margin: 4px;
#         font-family: 'IBM Plex Mono', monospace;
#         font-size: 0.85rem;
#         color: #a0a8ff;
#     }

#     .rec-box {
#         background: #111827;
#         border: 1px solid #374151;
#         border-radius: 4px;
#         padding: 1.5rem;
#         font-size: 0.95rem;
#         line-height: 1.7;
#     }

#     .score-num {
#         font-family: 'IBM Plex Mono', monospace;
#         font-size: 3rem;
#         font-weight: 600;
#     }

#     div[data-testid="metric-container"] {
#         background: #1a1a1a;
#         border: 1px solid #333;
#         border-radius: 4px;
#         padding: 1rem;
#     }
# </style>
# """, unsafe_allow_html=True)


# # ── Sidebar: Input form ────────────────────────────────────────────────────────
# st.sidebar.markdown("# 🎓 Student Dropout Predictor")
# st.sidebar.markdown("---")

# st.sidebar.markdown("### 📋 Academic Info")
# G1 = st.sidebar.slider("Grade Period 1 (G1)", 0, 20, 10)
# G2 = st.sidebar.slider("Grade Period 2 (G2)", 0, 20, 10)
# G3 = st.sidebar.slider("Final Grade (G3)",    0, 20, 10)
# failures   = st.sidebar.number_input("Past Failures",  min_value=0, max_value=10, value=0)
# absences   = st.sidebar.number_input("Absences",       min_value=0, max_value=100, value=0)
# studytime  = st.sidebar.slider("Study Time (hrs/week)", 1, 4, 2)

# st.sidebar.markdown("### 🏠 Personal Info")
# age        = st.sidebar.slider("Age", 15, 22, 17)
# sex        = st.sidebar.selectbox("Sex", ["Female (0)", "Male (1)"])
# address    = st.sidebar.selectbox("Address", ["Urban (0)", "Rural (1)"])
# higher     = st.sidebar.selectbox("Wants Higher Education", ["No (0)", "Yes (1)"])
# internet   = st.sidebar.selectbox("Internet Access", ["No (0)", "Yes (1)"])

# st.sidebar.markdown("### 👨‍👩‍👦 Family")
# Medu  = st.sidebar.slider("Mother Education (0–4)", 0, 4, 2)
# Fedu  = st.sidebar.slider("Father Education (0–4)", 0, 4, 2)
# famrel = st.sidebar.slider("Family Relationship (1–5)", 1, 5, 3)

# st.sidebar.markdown("### 🎮 Lifestyle")
# goout    = st.sidebar.slider("Going Out (1–5)", 1, 5, 2)
# freetime = st.sidebar.slider("Free Time (1–5)", 1, 5, 3)
# health   = st.sidebar.slider("Health (1–5)",    1, 5, 3)
# Dalc     = st.sidebar.slider("Workday Alcohol (1–5)", 1, 5, 1)
# Walc     = st.sidebar.slider("Weekend Alcohol (1–5)", 1, 5, 1)


# def build_payload():
#     engagement_score = studytime * 2 - absences
#     academic_risk    = failures + (20 - G3)
#     return {
#         "school": 0, "sex": int(sex[0] == "M"), "age": age,
#         "address": int(address[0] == "R"), "famsize": 0, "Pstatus": 0,
#         "Medu": Medu, "Fedu": Fedu,
#         "Mjob": 0, "Fjob": 0, "reason": 0, "guardian": 0,
#         "traveltime": 1, "studytime": studytime, "failures": failures,
#         "schoolsup": 0, "famsup": 0, "paid": 0, "activities": 0,
#         "nursery": 0, "higher": int(higher[0] == "Y"),
#         "internet": int(internet[0] == "Y"), "romantic": 0,
#         "famrel": famrel, "freetime": freetime, "goout": goout,
#         "Dalc": Dalc, "Walc": Walc, "health": health, "absences": absences,
#         "G1": float(G1), "G2": float(G2), "G3": float(G3),
#         "engagement_score": float(engagement_score),
#         "academic_risk": float(academic_risk),
#     }


# # ── Main area ─────────────────────────────────────────────────────────────────
# st.title("🎓 Student Dropout Prediction & Intervention System")
# st.markdown("Adjust the sliders in the sidebar, then click **Predict**.")

# col_btn, _ = st.columns([1, 5])
# predict_clicked = col_btn.button("🔮 Predict", use_container_width=True)

# if predict_clicked:
#     payload = build_payload()

#     with st.spinner("Analyzing student profile..."):
#         try:
#             resp = requests.post(API_URL, json=payload, timeout=30)
#             resp.raise_for_status()
#             result = resp.json()
#         except requests.exceptions.ConnectionError:
#             st.error("❌ Cannot connect to API at localhost:8000. Is the FastAPI server running?")
#             st.stop()
#         except requests.exceptions.HTTPError as e:
#             st.error(f"❌ API error: {e.response.text}")
#             st.stop()
#         except Exception as e:
#             st.error(f"❌ Unexpected error: {e}")
#             st.stop()

#     risk_score  = result["risk_score"]
#     risk_level  = result["risk_level"]
#     top_factors = result["top_factors"]
#     recommendation = result["recommendation"]

#     # ── Results row ────────────────────────────────────────────────────────────
#     st.markdown("---")
#     r1, r2, r3 = st.columns(3)

#     with r1:
#         st.markdown("#### Risk Score")
#         pct = int(risk_score * 100)
#         color = "#00e676" if risk_level == "Low" else "#ffb300" if risk_level == "Medium" else "#ff1744"
#         st.markdown(
#             f'<div class="score-num" style="color:{color}">{pct}%</div>',
#             unsafe_allow_html=True
#         )

#     with r2:
#         st.markdown("#### Risk Level")
#         css_class = f"risk-{risk_level.lower()}"
#         st.markdown(
#             f'<div class="risk-card {css_class}"><strong>{risk_level.upper()} RISK</strong></div>',
#             unsafe_allow_html=True
#         )

#     with r3:
#         st.markdown("#### Top Contributing Factors")
#         tags = "".join(f'<span class="factor-tag">{f}</span>' for f in top_factors)
#         st.markdown(tags, unsafe_allow_html=True)

#     # ── Recommendation ─────────────────────────────────────────────────────────
#     st.markdown("---")
#     st.markdown("#### 📌 Intervention Recommendation")
#     st.markdown(f'<div class="rec-box">{recommendation.replace(chr(10), "<br>")}</div>',
#                 unsafe_allow_html=True)

#     # ── What-If Simulator ──────────────────────────────────────────────────────
#     st.markdown("---")
#     st.markdown("## 🎮 What-If Simulator")
#     st.markdown("Adjust values below and click **Re-simulate** to see how changes affect the risk.")

#     wc1, wc2, wc3 = st.columns(3)
#     with wc1:
#         wif_G3       = st.slider("What if G3 →",       0, 20, G3,       key="wif_g3")
#         wif_absences = st.slider("What if Absences →",  0, 100, absences, key="wif_abs")
#     with wc2:
#         wif_failures  = st.slider("What if Failures →",  0, 10, failures,  key="wif_fail")
#         wif_studytime = st.slider("What if Study Time →", 1, 4,  studytime, key="wif_study")
#     with wc3:
#         wif_G1 = st.slider("What if G1 →", 0, 20, G1, key="wif_g1")
#         wif_G2 = st.slider("What if G2 →", 0, 20, G2, key="wif_g2")

#     if st.button("🔄 Re-simulate"):
#         wif_payload = {**payload}
#         wif_payload.update({
#             "G1": float(wif_G1), "G2": float(wif_G2), "G3": float(wif_G3),
#             "absences":  wif_absences,
#             "failures":  wif_failures,
#             "studytime": wif_studytime,
#             "engagement_score": float(wif_studytime * 2 - wif_absences),
#             "academic_risk":    float(wif_failures + (20 - wif_G3)),
#         })

#         with st.spinner("Re-simulating..."):
#             try:
#                 r2_resp = requests.post(API_URL, json=wif_payload, timeout=30)
#                 r2_resp.raise_for_status()
#                 r2_res = r2_resp.json()
#             except Exception as e:
#                 st.error(f"❌ Simulation error: {e}")
#                 st.stop()

#         wa1, wa2 = st.columns(2)
#         with wa1:
#             orig_pct = int(risk_score * 100)
#             new_pct  = int(r2_res["risk_score"] * 100)
#             delta    = new_pct - orig_pct
#             st.metric("Original Risk", f"{orig_pct}%")
#             st.metric("Simulated Risk", f"{new_pct}%", delta=f"{delta:+d}%",
#                       delta_color="inverse")
#         with wa2:
#             st.markdown(f"**Simulated Risk Level:** `{r2_res['risk_level']}`")
#             st.markdown(f"**Simulated Top Factors:** {', '.join(r2_res['top_factors'])}")

# else:
#     st.info("👈 Fill in student details in the sidebar and click **Predict** to begin.")
import streamlit as st
import requests
import json
import pickle

API_URL = "http://localhost:8000/predict"
META_PATH = "models/model_meta.pkl"

# ── Session State ─────────────────────────────────────────────────────────────
if "prediction" not in st.session_state:
    st.session_state.prediction = None

if "payload" not in st.session_state:
    st.session_state.payload = None

if "sim_result" not in st.session_state:
    st.session_state.sim_result = None


@st.cache_data
def load_meta():
    with open(META_PATH, "rb") as f:
        return pickle.load(f)

meta = load_meta()

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Student Dropout Predictor",
    page_icon="🎓",
    layout="wide",
)

st.markdown("""
<style>
    html, body, [class*="css"] { background-color: #0d0d0d; color: #e8e8e8; }
    .stApp { background-color: #0d0d0d; }

    .risk-card {
        padding: 1.5rem;
        border-radius: 4px;
        margin-bottom: 1rem;
    }
    .risk-low    { background: #0a2e1a; border-left: 4px solid #00e676; color: #00e676; }
    .risk-medium { background: #2e1f00; border-left: 4px solid #ffb300; color: #ffb300; }
    .risk-high   { background: #2e0a0a; border-left: 4px solid #ff1744; color: #ff1744; }

    .factor-tag {
        display: inline-block;
        background: #1a1a2e;
        padding: 4px 12px;
        border-radius: 2px;
        margin: 4px;
        font-size: 0.85rem;
        color: #a0a8ff;
    }

    .rec-box {
        background: #111827;
        border-radius: 4px;
        padding: 1.5rem;
    }

    .score-num {
        font-size: 3rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# ── Sidebar ───────────────────────────────────────────────────────────────────
st.sidebar.markdown("# 🎓 Student Dropout Predictor")
st.sidebar.markdown("---")

st.sidebar.markdown("### 📋 Academic Info")
G1 = st.sidebar.slider("Grade Period 1 (G1)", 0, 20, 10)
G2 = st.sidebar.slider("Grade Period 2 (G2)", 0, 20, 10)
G3 = st.sidebar.slider("Final Grade (G3)",    0, 20, 10)
failures   = st.sidebar.number_input("Past Failures", 0, 10, 0)
absences   = st.sidebar.number_input("Absences", 0, 100, 0)
studytime  = st.sidebar.slider("Study Time (hrs/week)", 1, 4, 2)

st.sidebar.markdown("### 🏠 Personal Info")
age        = st.sidebar.slider("Age", 15, 22, 17)
sex        = st.sidebar.selectbox("Sex", ["Female (0)", "Male (1)"])
address    = st.sidebar.selectbox("Address", ["Urban (0)", "Rural (1)"])
higher     = st.sidebar.selectbox("Wants Higher Education", ["No (0)", "Yes (1)"])
internet   = st.sidebar.selectbox("Internet Access", ["No (0)", "Yes (1)"])

st.sidebar.markdown("### 👨‍👩‍👦 Family")
Medu  = st.sidebar.slider("Mother Education (0–4)", 0, 4, 2)
Fedu  = st.sidebar.slider("Father Education (0–4)", 0, 4, 2)
famrel = st.sidebar.slider("Family Relationship (1–5)", 1, 5, 3)

st.sidebar.markdown("### 🎮 Lifestyle")
goout    = st.sidebar.slider("Going Out (1–5)", 1, 5, 2)
freetime = st.sidebar.slider("Free Time (1–5)", 1, 5, 3)
health   = st.sidebar.slider("Health (1–5)",    1, 5, 3)
Dalc     = st.sidebar.slider("Workday Alcohol (1–5)", 1, 5, 1)
Walc     = st.sidebar.slider("Weekend Alcohol (1–5)", 1, 5, 1)


def build_payload():
    engagement_score = studytime * 2 - absences
    academic_risk    = failures + (20 - G3)
    return {
        "school": 0, "sex": int(sex[0] == "M"), "age": age,
        "address": int(address[0] == "R"),
        "Medu": Medu, "Fedu": Fedu,
        "studytime": studytime, "failures": failures,
        "higher": int(higher[0] == "Y"),
        "internet": int(internet[0] == "Y"),
        "famrel": famrel, "freetime": freetime, "goout": goout,
        "Dalc": Dalc, "Walc": Walc, "health": health, "absences": absences,
        "G1": float(G1), "G2": float(G2), "G3": float(G3),
        "engagement_score": float(engagement_score),
        "academic_risk": float(academic_risk),
    }


# ── Main ──────────────────────────────────────────────────────────────────────
st.title("🎓 Student Dropout Prediction System")

# ✅ MODEL INFO
st.markdown("### 🤖 Model Information")
best_model = meta["best_model_name"]
metrics = meta["metrics"]

st.success(f"🏆 Best Model: {best_model}")

cols = st.columns(3)
for i, (name, m) in enumerate(metrics.items()):
    with cols[i]:
        st.metric(name, f"Acc: {m['accuracy']:.2f}", f"Recall: {m['recall']:.2f}")


predict_clicked = st.button("🔮 Predict")

if predict_clicked:
    payload = build_payload()
    resp = requests.post(API_URL, json=payload)
    st.session_state.prediction = resp.json()
    st.session_state.payload = payload
    st.session_state.sim_result = None


# ── SHOW RESULT ───────────────────────────────────────────────────────────────
if st.session_state.prediction:

    result = st.session_state.prediction

    risk_score  = result["risk_score"]
    risk_level  = result["risk_level"]
    top_factors = result["top_factors"]
    recommendation = result["recommendation"]

    st.markdown("---")

    st.markdown(f"## Risk: {int(risk_score*100)}% ({risk_level})")
    st.write("Top Factors:", top_factors)
    st.write("Recommendation:", recommendation)

    # ── What If ───────────────────────────────────────────────────────────────
    st.markdown("## 🎮 What-If Simulator")

    wif_G3 = st.slider("G3", 0, 20, int(G3))
    wif_abs = st.slider("Absences", 0, 100, int(absences))
    wif_fail = st.slider("Failures", 0, 10, int(failures))
    wif_study = st.slider("Study Time", 1, 4, int(studytime))

    if st.button("🔄 Re-simulate"):

        wif_payload = {**st.session_state.payload}

        wif_payload.update({
            "G3": wif_G3,
            "absences": wif_abs,
            "failures": wif_fail,
            "studytime": wif_study,
            "engagement_score": wif_study * 2 - wif_abs,
            "academic_risk": wif_fail + (20 - wif_G3),
        })

        r = requests.post(API_URL, json=wif_payload)
        st.session_state.sim_result = r.json()

    if st.session_state.sim_result:
        sim = st.session_state.sim_result

        st.write("Simulated Risk:", int(sim["risk_score"]*100), "%")
        st.write("Simulated Level:", sim["risk_level"])