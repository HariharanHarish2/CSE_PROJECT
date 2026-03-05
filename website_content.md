# Website Content Structure for "HSL-SQL" (Hybrid Schema-LLM NL2SQL)

This document outlines the exact textual structure and flow to use if you build a presentation website (e.g., in React, HTML/JS, or Streamlit) to showcase your final year project.

---

## 1. Hero Section (Home Page)
**Headline**: HSL-SQL: Redefining Database Interaction
**Sub-Headline**: A Hybrid Schema-Aware and LLM-Guided Architecture for Robust, Hallucination-Free Natural Language to SQL Translation.
**Call-to-Action Buttons**: [ Try the Live Demo ] | [ Read the IEEE Paper ]

---

## 2. About the Project
**Header**: Democratizing Data Access
**Content**:
Extracting actionable insights from relational databases traditionally requires deep expertise in SQL. HSL-SQL bridges this technical gap by allowing non-technical enterprise users to converse seamlessly with their data in plain English. 

Unlike traditional rule-based models (like G-SQL) which fail on complex logic, or pure Large Language Models (like GPT-4) which frequently hallucinate non-existent database columns, **HSL-SQL introduces a novel bipartite hybrid architecture**. It routes simple aggregations to an ultra-fast deterministic rule engine, reserving computationally expensive LLM invocations exclusively for logically complex, nested, or implicitly stated queries. Every generated query is strictly validated against a live Database Schema Graph, guaranteeing 100% executable SQL.

---

## 3. Core Features
*   **🧠 Intelligent Complexity Routing**
    *   *Icon*: Brain/Splitter
    *   *Description*: A custom NLP classifier tags incoming queries as Easy, Medium, Hard, or Extra-Hard, triggering either the lightweight Rules Engine or the heavy LLM Semantic Engine.
*   **🛡️ Absolute Schema Grounding**
    *   *Icon*: Shield
    *   *Description*: Structured Prompt Engineering forces the LLM to adhere strictly to the serialized JSON schema map, eliminating the risk of unmapped table or column hallucinations.
*   **🔄 Auto-Error Correction Loop**
    *   *Icon*: Refresh Arrows
    *   *Description*: When a runtime execution anomaly occurs, the stack trace is programmatically fed back into the LLM context window to enable autonomous self-correction.
*   **💬 Contextual Memory**
    *   *Icon*: Speech Bubbles
    *   *Description*: Full support for follow-up conversational queries where implicit entity references are resolved via the session history (e.g., "What about the ones in London?").

---

## 4. Architecture Explanation (The "How It Works" Section)
**Visual**: *(Embed your Architecture Diagram here)*
**Phase 1: Ingestion & Routing**
We tokenize the Natural Language Query (NLQ) and assess its mathematical complexity. Simple filters bypass the LLM entirely!
**Phase 2: Structured Reasoning**
Hard queries trigger the LLM to ingest the JSON-serialized schema and return a strict JSON mathematical reasoning block mapping the implicit logic to explicit SQL.
**Phase 3: Validation & Execution**
The synthesized SQL template is validated for constraint alignment. If the RDBMS rejects the syntax, the system loops the error string back to the LLM for adjustment.

---

## 5. Technology Stack
*   **Frontend Interface**: Streamlit / FastAPI
*   **Core NLP Processor**: Python (NLTK/Spacy), Regex Rule Engine
*   **LLM Backbone**: OpenAI GPT-3.5-Turbo / GPT-4 via REST API
*   **Execution Layer**: SQLAlchemy over PostgreSQL/SQLite
*   **Memory Management**: Custom Sliding-Window Context Arrays

---

## 6. Research Contribution & Comparison 
*(Ideal for Academic Evaluators)*

### How HSL-SQL Improves Upon G-SQL (The Base Paper)
The original G-SQL paper utilized a highly deterministic, schema-aware rule-guided approach. 
**Our Extension**:
1.  **Complexity Handling**: G-SQL degrades when encountering superlative ranking (e.g., "3rd highest"). HSL-SQL successfully parses these using the LLM Semantic Layer.
2.  **Conversational Memory**: G-SQL executes independent queries; our hybrid tracks session context.

### HSL-SQL vs. Pure LLMs
Pure LLMs like ChatGPT generate SQL based on pre-trained probabilistic weights, often resulting in un-executable syntax due to invented columns. HSL-SQL bounds the LLM tightly by passing a rigid JSON schema and applying deterministic post-validation, driving execution accuracy from ~70% to >90%.

---

## 7. Interactive Demo Explanation
**Header**: See it in Action!
**Content**:
In the demo below, try asking a simple question like, *"Show me all departments."* Notice the instant response time (0ms LLM latency) as the system routes it through the Rule Engine. 
Next, ask a highly complex question like, *"Who is the highest-paid engineer in the New York office?"* Watch the system invoke the LLM, compute the JOINs across the `employees` and `departments` tables, and correctly apply the `ORDER BY salary DESC LIMIT 1` constraint.

---

## 8. Contact Section Built By
"Developed by [Your Name / Team]"
"Final Year Computer Science Engineering Project - Class of [Year]"
"Under the guidance of [Professor's Name]"
*(Links to GitHub Repository / LinkedIn)*
