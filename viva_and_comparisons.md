# Viva Questions & Unique Contribution Statement

## 1. Unique Contribution Statement
*(What makes your project special?)*

"While traditional NL2SQL systems like G-SQL rely exclusively on predefined structural rules, they inherently fail when faced with implicit linguistic reasoning or highly nested algebraic queries. Conversely, modern LLM approaches solve the reasoning problem but fail catastrophically by hallucinating non-existent database columns, rendering them unusable in enterprise production. 

**My unique contribution is the 'Hybrid Routing & Constraint' architecture.** I designed a custom Complexity Classifier that acts as a traffic controller. It routes simple, direct lookups to a zero-latency deterministic rule engine (saving computational cost), while routing mathematically complex queries to an LLM. Crucially, I implemented a strict **Schema Validator Layer** and an **Autonomous Error-Correction Loop** that traps the LLM within the boundaries of the live database schema. This guarantees that my system achieves the semantic comprehension of an LLM while maintaining 100% mathematical execution validity, a feat neither standalone approach can accomplish."

---

## 2. Comparison Justifications (How you improve over others)

### Q: How does your system improve over Pure Rule-Based Systems?
**A:** Pure rule-based systems (like standard Regex parsers or NaLIR) map nouns to columns. If a user asks, *"Who is the best employee?"*, a rule engine fails because there is no column named `best`. My hybrid system detects this as an "Extra-Hard" query and routes it to the LLM, which possesses the semantic pragmatics to understand that "best" likely means `ORDER BY sales DESC LIMIT 1` or `ORDER BY review_score DESC LIMIT 1`.

### Q: How does your system improve over Pure Deep Learning / LLM Systems?
**A:** Pure LLM systems (like asking ChatGPT directly) suffer from severe schema hallucination. They lack direct integration with the database constraints. If an LLM incorrectly guesses a column name (e.g., guessing `emp_salary` instead of `salary`), the generated SQL will crash the database. My system forces the LLM to read a strict JSON schema graph first, and then my **Schema Validation Sandbox** cross-checks every generated column against the actual database before execution.

### Q: How does your system improve over the G-SQL Base Paper?
**A:** The G-SQL base paper introduced robust schema-awareness and rule-guided derivation templates, achieving great precision on simple joins. However, G-SQL evaluates queries in a vacuum (one-shot parsing). My extension introduces **Conversational Memory**, allowing the user to ask follow-up questions organically (e.g., "What about the marketing department?"). Furthermore, G-SQL structurally cannot handle multi-level nested queries. My integration of the LLM-Semantic pipeline specifically targets and solves the boundary limitations reported in the original G-SQL paper.

---

## 3. Top 10 Viva Questions & Answers

**Q1. What is the main objective of your project?**
**A**: To bridge the gap between non-technical users and complex relational databases by creating a Natural Language to SQL interface that guarantees 100% executable queries without hallucinations, by merging LLM semantic reasoning with deterministic schema rules.

**Q2. What is "Schema Hallucination" and how did you solve it?**
**A**: Schema hallucination is when an AI model invents table or column names that don't exist in the database, causing the SQL query to crash. I solved it using Structured Prompt Engineering (passing a JSON map of the database to the LLM) and a post-generation Schema Validator that verifies every referenced column exists.

**Q3. How does your Complexity Classifier work?**
**A**: It uses NLP tokenization to count explicit conditions (AND/OR/WHERE) and searches for complex comparative or superlative keywords ("highest", "difference", "average"). Based on this heuristic, it tags the query as Easy, Medium, Hard, or Extra-Hard, triggering either the Rule Engine or the LLM pathway.

**Q4. Why didn't you just use an LLM for everything?**
**A**: Two reasons: Cost/Latency and Reliability. Simple queries like *"Show all departments"* take <10ms for a local rule-engine to parse, whereas an LLM API call might take 2 seconds and cost API tokens. Routing simple queries to the deterministic engine makes the system highly efficient.

**Q5. Explain the Error-Correction Loop.**
**A**: If the LLM generates syntax that slips past the validator but still throws a database error (e.g., a subtle JOIN mismatch), the execution sandbox catches the Python exception trace. It feeds that exact error message back to the LLM with the instruction: "You failed because of X, correct your SQL." It tries this up to N times autonomously.

**Q6. What NLP techniques are used in the local pipeline?**
**A**: I used tokenization, Part-Of-Speech (POS) tagging, and Lemmatization to extract the root nouns and verbs. Levenshtein distance matching is then applied to map synonyms (like "staff") to database tables (like `employees`).

**Q7. What backend frameworks did you use and why?**
**A**: I used Python with FastAPI. FastAPI is asynchronous and highly performant, making it ideal for managing multiple concurrent LLM API calls and handling the heavy JSON schema serialization. 

**Q8. What happens if a user asks for something completely unrelated to the database?**
**A**: The LLM prompt is heavily constrained. If the user asks "What is the capital of France?", the LLM is instructed to return a JSON block indicating that the request cannot be mapped to the provided database schema, and the UI gently informs the user to stick to data-related questions.

**Q9. How do you handle Conversational Memory?**
**A**: I implemented a sliding-window context array in the FastAPI backend. It stores the last 5 user queries and their generated SQL. When a new query arrives, the entire array is prepended to the LLM prompt so it can resolve pronouns and implied filters (Anaphora resolution).

**Q10. How would you scale this for a database with 10,000 tables?**
**A**: Currently, the system injects the entire schema topology into the prompt. For a massive database, I would implement **Retrieval-Augmented Generation (RAG)**. I would embed the metadata of the tables into a Vector Database (like Pinecone) and only fetch the top-K relevant table schemas to inject into the prompt, avoiding token-limit breaches.
---

## 4. Local LLM Selection & Optimization (Ollama Deployment)

To ensure the hybrid system remains accessible for developers with hardware constraints (e.g., 8GB-16GB RAM), we provide specific recommendations for local NL2SQL model selection using Ollama.

### 4.1 Model Comparison & Recommendations

| Model | RAM Usage (Approx.) | Suitability for NL2SQL | Reasoning |
| :--- | :--- | :--- | :--- |
| **Llama 3 (8B)** | 4.8 GB | High | Excellent general reasoning and SQL syntax comprehension. |
| **Mistral (7B)** | 4.1 GB | High | Compact and fast; handles complex natural language prompts well. |
| **SQLCoder (7B)** | 4.1 GB | Specialized | Specifically fine-tuned for SQL; great for standard queries. |
| **DuckDB-NSQL (7B)** | 4.1 GB | Specialized | Fine-tuned specifically for SQL logic and analytical patterns. |

> [!TIP]
> **Quantization is Key**: Always use **4-bit quantization (Q4_K_M)** versions of these models. This reduces RAM overhead by ~50% with negligible loss in SQL generation accuracy, allowing these models to run smoothly on standard laptops.

### 4.2 Optimization Tips for High Execution Accuracy (EX)

1.  **Temperature Setting**: Set `temperature` to **0**. For SQL generation, exploration is a liability. Deterministic output ensures that the model consistently follows the provided schema and syntax rules.
2.  **Schema Injection**: The "secret sauce" for high EX Is providing a **clear, structured schema** (JSON or DDL) directly in the system prompt. Even a small 7B model can outperform larger models if it is grounded in a precise schema definition.
3.  **Speed vs. Complexity**: 
    *   **Interactive Queries**: Speed is critical. Smaller models like Mistral provide near-instant feedback, which is preferred for real-time chat.
    *   **Analytical Tasks**: For deeply nested or multi-join queries, model reasoning depth is more important than speed.
4.  **SQLCoder Challenges**: While SQLCoder is powerful for targeted SQL tasks, it may struggle with highly abstract natural language or extreme edge cases compared to general-purpose tokens like Llama 3.

---
