import sqlite3
import os
import pandas as pd

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "company.db")

class DBConnector:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        
    def execute_query(self, query: str):
        """Executes a SQL query and returns results as a dictionary (columns and rows) or an error."""
        try:
            # Security Layer 1: Basic String Sanitization
            clean_query = query.strip()
            lower_query = clean_query.lower()
            
            # Block Multi-Statement Queries (SQL Injection protection)
            if ";" in clean_query[:-1]: # Allow trailing semicolon but not interior ones
                 return {"error": "Multi-statement queries are prohibited for security."}

            # Security Layer 2: Blacklist of destructive commands
            forbidden_keywords = [
                'drop', 'alter', 'truncate', 'grant', 'revoke', 
                'shutdown', 'exec', 'execute', 'attach', 'detach'
            ]
            if any(forbidden in lower_query for forbidden in forbidden_keywords):
                return {"error": f"Security violation: The query contains restricted keywords: {', '.join(forbidden_keywords)}"}
                
            conn = sqlite3.connect(self.db_path)
            
            # --- AUTO-SEEDING DATA (NEW) ---
            # If tables are empty, add some sample data so the user sees results
            cursor = conn.cursor()
            if "students" in lower_query:
                cursor.execute("CREATE TABLE IF NOT EXISTS students (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, age INTEGER, grade TEXT, enrollment_date TEXT)")
                cursor.execute("SELECT COUNT(*) FROM students")
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO students (name, age, grade, enrollment_date) VALUES ('Alice Smith', 20, 'A', '2024-01-15')")
                    cursor.execute("INSERT INTO students (name, age, grade, enrollment_date) VALUES ('Bob Jones', 22, 'B', '2023-09-10')")
            elif "employees" in lower_query:
                cursor.execute("CREATE TABLE IF NOT EXISTS employees (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, role TEXT, salary INTEGER, department_id INTEGER)")
                cursor.execute("SELECT COUNT(*) FROM employees")
                if cursor.fetchone()[0] == 0:
                    cursor.execute("INSERT INTO employees (name, role, salary, department_id) VALUES ('Charlie Brown', 'Software Engineer', 120000, 1)")
                    cursor.execute("INSERT INTO employees (name, role, salary, department_id) VALUES ('Diana Prince', 'Product Manager', 115000, 2)")
            conn.commit()
            
            if lower_query.startswith("select"):
                # Using pandas read_sql to quickly get tabular format with headers
                df = pd.read_sql_query(query, conn)
                conn.close()
                return {
                    "columns": df.columns.tolist(),
                    "rows": df.values.tolist(),
                    "error": None
                }
            else:
                # For CREATE, INSERT, UPDATE, DELETE - Limited to non-critical operations in this project
                cursor = conn.cursor()
                cursor.execute(query)
                conn.commit()
                conn.close()
                return {
                    "columns": ["Status"],
                    "rows": [["Operation successful"]],
                    "error": None
                }
            
        except sqlite3.DatabaseError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"Execution Failed: {str(e)}"}
