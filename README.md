# Hybrid Schema-Aware and LLM-Guided NL2SQL System

A robust, production-ready Natural Language to SQL interface that merges deterministic rule-based engines with LLM semantic reasoning. For details on local deployment and optimization (Ollama), see [viva_and_comparisons.md](file:///e:/cseproject/viva_and_comparisons.md#4-local-llm-selection--optimization-ollama-deployment).
Conversational AI System

This project is the implementation of a Final Year CSE Project extending the "G-SQL" paper capabilities. It integrates deterministic Rule-Based SQL Generation with LLM Reasoning (ChatGPT-style AI) while enforcing schema validation to prevent hallucinations.

This complete application includes:
1.  **A sample script to generate a simulated SQLite Database.**
2.  **A FastAPI Backend Application.**
3.  **A Streamlit interactive Frontend Chat UI.**

## Setup Instructions

### 1. Install Dependencies
Make sure you have Python installed. You can create a virtual environment, then install the required packages:

```bash
pip install -r requirements.txt
```

### 2. Set your Gemini API Key
The system uses the Google Gemini API for handling "Hard" and "Extra-Hard" complexities.
You can:
-   **Option A:** Paste the key directly into the **sidebar** in the Streamlit UI.
-   **Option B:** Add it to the `backend/.env` file:
    ```bash
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

*Note: If you run without a key, the system uses a local "Free Mode" fallback to demonstrate execution flow.*

### 3. Initialize the Sample Database
Run the initialization script to create `company.db` with dummy employees and departments:

```bash
python scripts/init_db.py
```

### 4. Run the Backend API (Terminal 1)
Start the FastAPI application. Ensure you are in the root directory (`e:\cseproject`):

```bash
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8080 --reload
```
You can view the interactive API documentation at `http://localhost:8080/docs`.

### 5. Run the Frontend UI (Terminal 2)
In a separate terminal, launch the Streamlit web interface:

```bash
streamlit run frontend/app.py
```
This will automatically open your browser to `http://localhost:8501`.

## Core Features Demonstrated
*   **Routing Logic**: Queries like "Show all employees" are evaluated as EASY and handled by the Python rules engine. Queries like "Who is the highest paid engineer?" are evaluated as HARD and parsed via the LLM API.
*   **Schema Validation**: The system uses `schema_manager.py` to ensure hallucinated columns from the LLM are corrected.
*   **Conversation Memory**: Supports conversational flow (e.g. Follow up query: "What about the ones in London?").
*   **Error Correction**: Built-in 2-retry loop where if the DB throws a syntax error, the stack trace is fed back into the LLM to self-correct.

## Documentation References
For theoretical details, grading features, and complete processing flow read the exhaustive documentation in `nl2sql_architecture_and_docs.md`.
