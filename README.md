<<<<<<< HEAD
# 🎓 AI Student Dropout Prediction & Intervention System

## Project Structure

```
dropout_system/
├── data/
│   ├── student-mat.csv        ← your UCI dataset (place here)
│   └── processed.csv          ← auto-generated after preprocessing
├── models/
│   ├── best_model.pkl         ← auto-generated after training
│   └── model_meta.pkl         ← auto-generated after training
├── preprocess.py              ← Step 1: Data preprocessing
├── train.py                   ← Step 2: Model training
├── rag.py                     ← Step 5: RAG + Groq LLaMA
├── api.py                     ← Step 3+4: SHAP + FastAPI backend
├── app.py                     ← Step 6+7: Streamlit frontend + What-If
├── requirements.txt
└── README.md
```

---

## Setup

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Groq API key
Get your free key at https://console.groq.com
```bash
# Linux/Mac
export GROQ_API_KEY=your_key_here

# Windows
set GROQ_API_KEY=your_key_here
```

---

## Run Order (ALL 4 steps must be done in sequence)

### Step 1 — Preprocess the dataset
Place your `student-mat.csv` in the `data/` folder, then:
```bash
python preprocess.py --input data/student-mat.csv --output data/processed.csv
```

### Step 2 — Train the ML model
```bash
python train.py
```
This prints accuracy/F1/recall for all 3 models and saves the best one.

### Step 3 — Start the FastAPI backend
Open Terminal 1:
```bash
uvicorn api:app --reload --port 8000
```
Verify it's running: http://localhost:8000

### Step 4 — Launch the Streamlit frontend
Open Terminal 2:
```bash
streamlit run app.py
```
Opens at: http://localhost:8501

---

## Sample Test Input (POST /predict)

```json
{
  "school": 0,
  "sex": 1,
  "age": 17,
  "address": 0,
  "famsize": 0,
  "Pstatus": 0,
  "Medu": 2,
  "Fedu": 2,
  "Mjob": 0,
  "Fjob": 0,
  "reason": 0,
  "guardian": 0,
  "traveltime": 1,
  "studytime": 1,
  "failures": 2,
  "schoolsup": 0,
  "famsup": 0,
  "paid": 0,
  "activities": 0,
  "nursery": 0,
  "higher": 0,
  "internet": 1,
  "romantic": 0,
  "famrel": 2,
  "freetime": 4,
  "goout": 4,
  "Dalc": 3,
  "Walc": 4,
  "health": 2,
  "absences": 15,
  "G1": 6.0,
  "G2": 5.0,
  "G3": 4.0,
  "engagement_score": -13.0,
  "academic_risk": 18.0
}
```

## Sample Test Output

```json
{
  "risk_score": 0.8732,
  "risk_level": "High",
  "top_factors": ["absences", "G3", "failures"],
  "recommendation": "• Assign a dedicated mentor to monitor attendance weekly and flag consecutive absences immediately.\n• Enroll the student in remedial classes for core subjects to address the low G3 grade.\n• Schedule an academic counseling session to assess the root causes of repeated failures and set a recovery plan.\n• Consider a motivational intervention to reconnect the student with their long-term educational goals.\n• Notify parents/guardians and establish a weekly check-in routine."
}
```

---

## Full Pipeline Flow

```
Streamlit (app.py)
    ↓  POST /predict  (student features)
FastAPI (api.py)
    ↓  loads
ML Model (best_model.pkl)
    ↓  returns risk_score + calls
SHAP (api.py → get_top_factors)
    ↓  top_factors → calls
RAG + Groq LLaMA (rag.py → get_recommendation)
    ↓  returns recommendation
FastAPI response JSON
    ↓  displayed in
Streamlit (risk card + factors + recommendation + what-if)
```
=======
# dropout_prediction
>>>>>>> 0971cdb39902f6a31b60856391725e7d356dca58
