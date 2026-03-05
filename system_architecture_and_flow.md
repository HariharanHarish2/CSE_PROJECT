# System Architecture, Flowchart, and Algorithms

## 1. System Architecture Diagram Explanation (Textual)

The HSL-SQL system is structured into five distinct operational tiers:

**Tier 1: Input & Context Layer**
*   **User Interface (Streamlit)**: Accepts the Natural Language Query (NLQ).
*   **Conversation Memory Hub**: Appends historical dialogue context to resolve coreferences (e.g., "Show me his salary").

**Tier 2: Complexity Routing Matrix**
*   **NLP Preprocessor**: Tokenizes, POS-tags, and dependency-parses the NLP.
*   **Complexity Classifier**: Flags the query as Easy, Medium, Hard, or Extra-Hard. It searches for superlative adjectives ("highest"), comparative keywords, or multi-condition filtering.

**Tier 3: Generation Pathways (The Hybrid Component)**
*   *Path A: Rule-Based Engine (Fast Path)*: If Easy/Medium, maps tokens directly to the `JSON_Schema_Graph`. Combines raw nouns to table/column coordinates via Levenshtein distance matching.
*   *Path B: LLM Semantic Engine (Slow & Deep Path)*: If Hard/Extra-hard, wraps the `JSON_Schema_Graph` into a rigid Prompt Template. An API call fetches a structured JSON reasoning block dictating the heavy aggregation logic and nested joints.

**Tier 4: Synthesis & Validation Sandbox**
*   **Template Synthesizer**: Merges output from either Path A or B into raw SQL.
*   **Schema Validator**: Cross-checks every referenced column against the active database schema to prune hallucinations.

**Tier 5: Execution & Error Correction Loop**
*   **SQLAlchemy Execution Sandbox**: Runs the query on a Read-Only transaction thread.
*   *Error Trap*: If a runtime exception occurs (e.g., Column `dept_name` not found), the string is fed back to the LLM with the instruction to self-correct based on the schema.
*   **Response Formatter**: Generates a natural language explanation alongside the final returned RDBMS tuples.

---

## 2. Detailed Algorithm (Pseudocode)

```pseudocode
INPUT: Natural_Language_Query (NLQ), Database_Schema (S)
OUTPUT: Executable_SQL (Q), Data_Result (R)

FUNCTION HSL_SQL_Pipeline(NLQ, S):
    // Step 1: Serialize Schema
    Schema_Graph = SerializeToJSON(S)
    
    // Step 2: Inject Conversational Memory
    Context_Query = MemoryHub.resolve_anaphora(NLQ)
    
    // Step 3: Complexity Routing
    Complexity_Score = NLP_Classifier.analyze(Context_Query)
    
    IF Complexity_Score in ["EASY", "MEDIUM"]:
        // Deterministic Base (G-SQL Style)
        Tokens = Tokenize_and_Tag(Context_Query)
        SQL_Skeleton = RuleEngine.map_to_schema(Tokens, Schema_Graph)
    ELSE:
        // Semantic Deep-Dive (Hybrid Upgrade)
        Prompt = PromptBuilder.generate(Schema_Graph, Context_Query)
        LLM_Response = Call_LLM_API(Prompt, format="JSON")
        SQL_Skeleton = Extract_SQL_From_JSON(LLM_Response)
    
    // Step 4: Schema Validation (Anti-Hallucination Barrier)
    IsValid = Validator.check_columns_and_tables(SQL_Skeleton, Schema_Graph)
    
    IF NOT IsValid:
        // Minor Hallucination mapping algorithm logic
        SQL_Skeleton = SchemaLinker.force_map_closest_synonym(SQL_Skeleton, Schema_Graph)
        
    // Step 5: Execution & Auto-Correction
    Attempts = 0
    While Attempts < MAX_RETRIES:
        Result, Error = Execute_On_Database(SQL_Skeleton)
        IF Error:
            Feedback_Prompt = PromptBuilder.create_error_correction(Schema_Graph, SQL_Skeleton, Error)
            SQL_Skeleton = Extract_SQL_From_JSON(Call_LLM_API(Feedback_Prompt))
            Attempts += 1
        ELSE:
            MemoryHub.save_state(NLQ, SQL_Skeleton)
            RETURN SQL_Skeleton, Result
            
    RETURN "EXECUTION FAILED: Max Iterations Reached", NULL
```

---

## 3. Flowchart Flow Explanation

1.  **[START]** -> Receive NLQ.
2.  **[DECISION]** -> Does query have missing context? (Yes -> Pull from Memory -> **[PROCESS]**).
3.  **[CLASSIFICATION]** -> Parse NLP Complexity.
    *   *Branch 1 (Low Complexity)* -> **[Rule Engine Model]** -> Extract Table names -> Build `SELECT/WHERE/FROM`.
    *   *Branch 2 (High Complexity)* -> **[LLM Builder]** -> Input JSON Schema -> Fetch Reasoning Block -> Generate Aggregated SQL.
4.  **[MERGE POINT]** -> Validate generated query against Live DB schema headers.
5.  **[DECISION]** -> Are columns hallucinatory? (Yes -> **[Syntax Mapper]** assigns closest synonyms -> **[PROCESS]**).
6.  **[EXECUTION]** -> Run SQL Command.
7.  **[DECISION]** -> Did DB throw an error? 
    *   (Yes -> **[Error Correction Loop]** -> Send StackTrace to LLM -> Back to Execution).
8.  **[OUTPUT]** -> Display Results Table + Human Readable Explanation.
9.  **[END]**.

---

## 4. Sample Dataset Usage (Spider-Style Enterprise Schema)

For demonstration, a 3-table relational structure resembling an Enterprise ERP system is used.
This dataset tests complex joins and filtering logic.

**Table 1: Departments**
*   `id` (PK)
*   `name` (VARCHAR)
*   `location` (VARCHAR)

**Table 2: Employees**
*   `id` (PK)
*   `name` (VARCHAR)
*   `role` (VARCHAR)
*   `salary` (INT)
*   `department_id` (FK to Departments.id)

**Table 3: Employee_Reviews**
*   `id` (PK)
*   `employee_id` (FK to Employees.id)
*   `review_score` (INT 1-100)
*   `review_date` (DATE)

---

## 5. Sample Example Query Processing (Step-by-step)

**User Input (NLQ):** *"Which employee in the marketing department has the best review score?"*

**Step 1: Context & NLP**
Tokens tagged: `["employee", "marketing", "department", "best", "review", "score"]`
Complexity classified as **EXTRA-HARD** due to implicit superlative keyword "best" requiring a table join and numeric sorting.

**Step 2: Routing**
The query bypasses the Rule Engine and triggers the LLM Pipeline. The backend serializes the `Employees`, `Departments`, and `Employee_Reviews` tables into a lightweight JSON string.

**Step 3: Reasoning (LLM Output)**
```json
{
  "reasoning": "Need to join Employees with Departments to filter by 'marketing', and join with Employee_Reviews to rank by review_score descending. 'Best' implies highest score, so we limit to 1.",
  "sql": "SELECT e.name FROM Employees e JOIN Departments d ON e.department_id = d.id JOIN Employee_Reviews r ON e.id = r.employee_id WHERE d.name = 'Marketing' ORDER BY r.review_score DESC LIMIT 1;"
}
```

**Step 4: Schema Validation**
Validator confirms `Employees.department_id`, `Departments.id`, and `Employee_Reviews.review_score` exist. Check passed.

**Step 5: Execution**
The query hits the SQLite DB.
*Result Returned*: `["Diana Prince"]`.

**Step 6: UI Rendering**
The Chatbox updates with the natural language answer: *The employee in the marketing department with the highest review score is Diana Prince.* The SQL is attached for developer transparency.
