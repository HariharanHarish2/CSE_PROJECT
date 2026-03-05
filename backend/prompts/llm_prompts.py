import textwrap

class PromptTemplates:
    
    @staticmethod
    def get_sql_generation_prompt(schema_json: str, user_query: str) -> str:
        """Structured prompt to force the LLM into returning a JSON reasoning block and the final SQL."""
        return textwrap.dedent(f"""\
            You are a SQLite Expert and Natural Language to SQL (NL2SQL) engine.
            
            ### TASK
            Generate a valid SQLite query based ONLY on the provided schema. 
            Ensure accuracy and follow the formatting rules strictly.

            ### CONSTRAINTS
            1. DO NOT hallucinate columns or tables.
            2. Use SQLite syntax (e.g., date functions, string concat).
            3. If the user query is ambiguous, use common sense based on schema synonyms.
            4. Return ONLY the JSON object. No words before or after.

            ### DATABASE SCHEMA
            {schema_json}

            ### EXAMPLE 1
            User Query: "Find the top 3 highest paid employees in the Sales department"
            Output:
            {{
                "reasoning": "1. Join 'employees' with 'departments' on 'department_id'. 2. Filter by department name 'Sales'. 3. Order by 'salary' descending. 4. Limit to 3.",
                "sql": "SELECT e.* FROM employees e JOIN departments d ON e.department_id = d.id WHERE d.name = 'Sales' ORDER BY e.salary DESC LIMIT 3;"
            }}

            ### USER QUERY
            {user_query}

            ### OUTPUT FORMAT (JSON ONLY)
            {{
                "reasoning": "...",
                "sql": "..."
            }}
            """)

    @staticmethod
    def get_error_correction_prompt(schema_json: str, user_query: str, failed_sql: str, error_message: str) -> str:
        """Prompt to feed the stack trace back to the LLM to Auto-Correct."""
        return textwrap.dedent(f"""\
            You are a SQL Debugger. A query you generated failed to execute in SQLite.
            
            ### ORIGINAL INTENT
            {user_query}
            
            ### FAILED SQL
            {failed_sql}
            
            ### SQLite ERROR
            {error_message}
            
            ### DATABASE SCHEMA
            {schema_json}
            
            ### TASK
            Analyze the error and the schema. Provide a fixed SQLite query.
            Common issues: missing quotes, case sensitivity in strings, or column name typos.
            
            ### OUTPUT FORMAT (JSON ONLY)
            {{
                "reasoning": "Identify exactly why the previous query failed and how the fix addresses it.",
                "sql": "SELECT ... FROM ...;"
            }}
            """)

    @staticmethod
    def get_explanation_prompt(user_query: str, generated_sql: str) -> str:
        """Generates a natural language explanation of the SQL for the UI."""
        return textwrap.dedent(f"""\
            You are a friendly SQL Data Analyst. Explain the following technical query in plain English.
            
            ### CONTEXT
            User Query: "{user_query}"
            Generated SQL: `{generated_sql}`
            
            ### INSTRUCTIONS
            1. Provide a **High-level Summary** of what data is being retrieved.
            2. Provide a **Technical Breakdown** of the SQL logic (tables used, filters applied).
            3. Use **Markdown** for formatting (bolding, lists).
            4. Keep it concise but professional.
            
            ### EXPLANATIONS
            """)
