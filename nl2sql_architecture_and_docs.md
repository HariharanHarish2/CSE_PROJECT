# Hybrid Schema-Aware and LLM-Guided NL2SQL Chatbot System

This document outlines the architecture, step-by-step processing, feature ideas, and technical analysis for the integrated NL2SQL ChatGPT-style Chatbot, built upon the theoretical foundations of the "G-SQL" paper.

---

## 1. Complete System Architecture

The system is divided into two primary environments: a modern frontend user interface and a robust AI backend API.

### Frontend (Streamlit ChatGPT-style UI)
*   **Chat Interface**: Handles natural language queries and renders database tables, generated SQL, and AI explanations.
*   **State Management**: Manages session history (Conversation Memory) for context-aware follow-up questions.
*   **Debug/Developer Mode**: Toggles visibility of complex operations (showing the generated SQL, complexity score, and error retries).

### Backend (FastAPI Python Application)
*   **API Gateway**: Exposes endpoints (`/chat`, `/schema`, `/history`).
*   **Conversation Memory Module**: Injects prior queries to resolve anaphora (e.g., "What about the ones in New York?").
*   **NLP Routing Engine**: Analyzes complexity (Easy/Medium/Hard/Extra-Hard).
*   **Rule-Based Engine**: Handles simple select/filter queries.
*   **LLM Reasoning Engine**: Receives structured prompts containing the schema graph and outputs JSON reasoning for nested/complex schemas.
*   **Schema Validator**: Cross-checks generated SQL against the actual database schema to prune hallucinations.
*   **Error Correction Loop**: Traps DB execution errors and feeds the stack trace back to the LLM to self-correct up to N times.
*   **Execution Engine**: Safely queries MySQL/PostgreSQL using SQLAlchemy or generic connectors.

---

## 2. Architecture Diagram Explanation (Textual)

1.  **[User]** -> Submits NLQ (Natural Language Query) via **[Streamlit UI]**.
2.  **[Streamlit UI]** -> Appends query to **[Session Memory]** -> Sends to **[FastAPI /chat endpoint]**.
3.  **[FastAPI Backend]** -> Injects memory for context -> Parses through **[NLP Complexity Classifier]**.
    *   *If Easy/Medium*: Routes to **[Rule-Based Clause Planner]** (Deterministic SQL generation).
    *   *If Hard/Extra-Hard*: Routes to **[LLM Reasoning Engine]** with **[JSON Schema Graph]** and **[Structured Prompts]**.
4.  Both pathways converge at the **[Template SQL Generator]**.
5.  **[SQL Validation Layer]** -> Checks syntax and schema linkage.
    *   *If Invalid*: Sent back to LLM via **[Error Correction Loop]**.
6.  *If Valid*: **[DB Execution Engine]** executes SQL against **[PostgreSQL/MySQL DB]**.
    *   *If Runtime Error*: Sent to **[Error Correction Loop]**.
7.  **[Response Formatter]** -> Packages the SQL string, the execution results (rows), and an LLM-generated natural language explanation of the query.
8.  **[FastAPI Backend]** -> Returns response to **[Streamlit UI]**.

---

## 3. Folder Structure of the Project

```text
nl2sql_project/
├── backend/
│   ├── main.py                  # FastAPI entry point
│   ├── core/
│   │   ├── nlp_processor.py     # Complexity classifier & rule routing
│   │   ├── schema_manager.py    # Schema loading & serialization
│   │   ├── sql_generator.py     # LLM prompting & Error correction
│   │   ├── db_connector.py      # SQLAlchemy execution handling
│   │   └── memory.py            # Chat session memory management
│   ├── prompts/
│   │   └── llm_prompts.py       # Prompt templates (Schema-aware)
│   └── .env                     # Secrets (DB_URL, OPENAI_API_KEY)
├── frontend/
│   └── app.py                   # Streamlit UI
├── scripts/
│   └── init_db.py               # Create and populate sample database
├── nl2sql_architecture_and_docs.md
├── requirements.txt
└── README.md
```

---

## 4. Step-by-step Query Processing Explanation

**Example Query:** "Show me the top 3 highest rated movies directed by Christopher Nolan."

1.  **Memory Integration**: Backend checks if the user previously asked context-setting questions (e.g., "Let's talk about movies").
2.  **Complexity Classification**: The NLP engine detects keywords "top 3", "highest rated". It marks the query as **Hard** (requires ordering, limits, and potentially joining `movies` and `directors`).
3.  **LLM Routing**: The query bypasses the pure rule-engine. 
4.  **Prompt Engineering**: The structured Prompt Generator serializes relevant parts of the `movies`, `directors`, and `ratings` schema, and formulates a JSON-response request for the LLM.
5.  **LLM Reasoning Generation**: LLM outputs a JSON payload indicating it needs to JOIN the tables on `director_id` and ORDER BY `rating` DESC LIMIT 3.
6.  **SQL Synthesis**: The template engine drafts: `SELECT m.title, r.rating FROM movies m JOIN directors d ON m.director_id = d.id JOIN ratings r ON m.id = r.movie_id WHERE d.name = 'Christopher Nolan' ORDER BY r.rating DESC LIMIT 3;`
7.  **Schema Validation Layer**: Confirms `movies.title`, `ratings.rating`, `movies.director_id` exist.
8.  **Execution & Catch**: Query is run on SQLite/MySQL. If a column was hallucinated, the DB returns an error. The error is instantly caught by the Error Correction Loop, fed back to the LLM ("Column not found: rating. Did you mean score?"), and regenerated.
9.  **Formatting**: The final tuples (e.g., Inception, Interstellar, The Dark Knight) are returned alongside the raw SQL to the UI.

---

## 5. Security Measures

1.  **SQL Injection Prevention**:
    *   Used Read-Only database users for execution.
    *   Block multi-statement execution (no semicolons followed by `DROP TABLE` or `DELETE`).
    *   Strict allow-lists inside the validation layer ensuring only `SELECT` queries are permitted.
2.  **API Key Handling**:
    *   All LLM API keys are stored in backend `.env` files.
    *   The Streamlit frontend never touches the LLM API directly.
3.  **Data Masking**:
    *   Schema serialization omits sensitive columns (e.g., `passwords`, `credit_cards`) from ever reaching the LLM prompt.

---

## 6. Advanced Feature Ideas for Higher Academic Marks

To elevate your final year project from an "A" to an "A+ / Outstanding":
1.  **Explainable AI (XAI) Toggle**: A UI button that visualizes *why* the system chose the LLM over the Rule-based engine, visually highlighting the schema links.
2.  **User-Feedback Loop (RLHF approach)**: Thumbs up/down buttons on generated SQL in the Chatbot. If downvoted, ask the user what was wrong and save it to an sqlite `training_data` DB for future fine-tuning.
3.  **Cost-Control Analytics Dashboard**: A Streamlit sidebar showing how many tokens were saved by routing easy queries to the Rules engine vs invoking the LLM.
4.  **Dynamic Schema Swapping**: A dropdown in the UI allowing the user to seamlessly switch between different databases (e.g., from IMDB to a Hospital database) proving cross-domain adaptability.

---

## 7. How this system improves over others

### Over Pure Rule-Based Systems:
Rules cannot handle implicitly stated logic well ("Who is the best worker?" -> requires pragmatically defining "best" as highest sales or lowest bugs). The LLM seamlessly handles the disambiguation that rules fail on.

### Over Pure LLM Systems:
Pure LLMs hallucinate badly. They invent columns (`SELECT user_rating FROM...` instead of `SELECT star_rating`). Our Schema Validator instantly identifies these, and the Hybrid nature means cheap/simple queries don't cost expensive LLM API tokens.

### Over Context-Free G-SQL (Base Paper):
Adding ChatGPT-style conversation memory. The base paper usually treats every NLQ as independent. Our system allows contextual follow-ups like:
*   User: "Show me movies by Nolan." -> `SELECT ... WHERE director = 'Nolan'`
*   User: "Which ones came out after 2010?" -> System merges context: `... WHERE director = 'Nolan' AND year > 2010`.
