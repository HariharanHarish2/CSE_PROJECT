import re

class NLPProcessor:
    def __init__(self):
        # Keywords that indicate an Extra-Hard/Hard requirement that a pure Rule-Based engine will struggle with
        self.complex_keywords = [
            "highest", "lowest", "top", "best", "worst", "maximum", "minimum", 
            "average", "mean", "most", "least", "compare", "difference", "total"
        ]

    def classify_complexity(self, query: str) -> str:
        """
        Determines the complexity of a natural language query.
        Returns 'EASY', 'MEDIUM', 'HARD', or 'EXTRA_HARD'.
        """
        lower_q = query.lower()
        
        # Count explicit conditions and joins hints
        condition_count = lower_q.count(" and ") + lower_q.count(" or ") + lower_q.count(" with ") + lower_q.count(" where ")
        
        has_complex_keyword = any(kw in lower_q for kw in self.complex_keywords)
        
        # 3. Special Case: Force EASY for specific demo/common commands to ensure they are FREE
        demo_keywords = ["create", "insert", "add", "show", "get", "list", "students", "users"]
        if any(kw in lower_q for kw in demo_keywords):
            return "EASY"
            
        if has_complex_keyword and condition_count >= 2:
            return "EXTRA_HARD"
        elif has_complex_keyword:
            return "HARD"
        elif condition_count >= 1:
            return "MEDIUM"
        else:
            return "EASY"

    def rule_based_generation(self, query: str, schema_dict: dict) -> str:
        """
        Robust Regex-powered SQL Factory.
        Handles SELECT, INSERT, UPDATE, DELETE, and CREATE without LLM.
        """
        lower_q = query.lower().strip()
        tables = schema_dict.get("tables", {}).keys()
        
        # 1. Identify Target Table and Operation
        target_table = None
        for table in tables:
            if table in lower_q:
                target_table = table
                break
            for syn in schema_dict["tables"][table].get("synonyms", []):
                if syn in lower_q:
                    target_table = table
                    break
        
        # 2. Extract Columns and Table for SELECT
        is_select = any(kw in lower_q for kw in ["show", "get", "list", "query", "select", "display", "find"])
        is_delete = any(kw in lower_q for kw in ["delete", "remove", "drop from"])
        is_update = any(kw in lower_q for kw in ["update", "change", "set"])
        is_insert = any(kw in lower_q for kw in ["insert", "add", "put", "create new"])
        is_create = "create table" in lower_q

        if not target_table and not is_create:
            # New Feature: Provide generic templates for keyword requests
            if is_insert: return "INSERT INTO YourTable (column1, column2) VALUES (value1, value2);"
            if is_update: return "UPDATE YourTable SET column1 = value1 WHERE condition;"
            if is_delete: return "DELETE FROM YourTable WHERE condition;"
            if is_select and ("sample" in lower_q or "example" in lower_q or "code" in lower_q):
                return "SELECT * FROM YourTable LIMIT 10;"
            return None

        # 3. Enhanced WHERE Clause Extraction
        columns = schema_dict["tables"][target_table].get("columns", []) if target_table else []
        where_clause = ""
        for col in columns:
            pattern = rf"{col}\s*(?:is|are|=|matches)\s*['\"]?([\w\s-]+)['\"]?"
            match = re.search(pattern, lower_q)
            if match:
                val = match.group(1).strip()
                if not val.isdigit():
                    val = f"'{val}'"
                where_clause = f" WHERE {col} = {val}"
                break

        # 4. Operation Routing
        if is_create:
            tname = target_table.capitalize() if target_table else "NewTable"
            if "project" in lower_q:
                return """CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    budget INTEGER,
    status TEXT DEFAULT 'Planning'
);"""
            return f"""CREATE TABLE {tname} (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);"""

        elif is_insert:
            if not target_table: return None
            # Skip ID, and skip columns with defaults like 'status' if we want to show default logic
            relevant_cols = [c for c in columns if c not in ['id', 'status', 'created_at']]
            cols_str = ", ".join(relevant_cols)
            
            # Smart placeholders based on column names
            vals = []
            for col in relevant_cols:
                if 'budget' in col or 'salary' in col or 'age' in col:
                    vals.append("5000")
                else:
                    vals.append("'Sample Value'")
            
            vals_str = ", ".join(vals)
            return f"INSERT INTO {target_table} ({cols_str}) VALUES ({vals_str});"

        elif is_delete:
            return f"DELETE FROM {target_table}{where_clause};"

        elif is_update:
            set_clause = ""
            for col in columns:
                pattern = rf"(?:set|change)\s+{col}\s+(?:to|=)\s*['\"]?([\w\s-]+)['\"]?"
                match = re.search(pattern, lower_q)
                if match:
                    val = match.group(1).strip()
                    if not val.isdigit(): val = f"'{val}'"
                    set_clause = f" SET {col} = {val}"
                    break
            if set_clause:
                return f"UPDATE {target_table}{set_clause}{where_clause};"
            return None

        # Default to SELECT
        return f"SELECT * FROM {target_table}{where_clause};"

    def get_ai_suggestions(self, query: str) -> str:
        """Provides unique AI-powered SQL suggestions and recommended next steps."""
        suggestions = [
            "💡 **AI Tip**: Use `GROUP BY` to see totals per category (e.g., 'Total salary by department').",
            "💡 **AI Tip**: You can use `JOIN` to combine data from `employees` and `departments` automatically.",
            "💡 **AI Tip**: You can create new tables using 'Create a table for projects' to expand your database.",
            "💡 **AI Tip**: Always define a **Primary Key** (like 'id int') when creating tables to ensure unique records.",
            "💡 **AI Tip**: You can add data using 'Add a new employee...' to keep your records up to date."
        ]
        import random
        return random.choice(suggestions)
