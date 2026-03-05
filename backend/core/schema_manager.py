import json

class SchemaManager:
    def __init__(self):
        # A hardcoded dummy schema representation spanning the structure of our SQLite db.
        # In a real final-year project, you would dynamically build this by querying PRAGMA table_info or INFORMATION_SCHEMA.
        self.schema = {
            "tables": {
                "departments": {
                    "columns": ["id", "name", "location"],
                    "primary_key": "id",
                    "synonyms": ["dept", "division", "sector"]
                },
                "employees": {
                    "columns": ["id", "name", "role", "salary", "department_id"],
                    "primary_key": "id",
                    "foreign_keys": {"department_id": "departments.id"},
                    "synonyms": ["staff", "workers", "team members", "folks"]
                },
                "students": {
                    "columns": ["id", "name", "age", "grade", "enrollment_date"],
                    "primary_key": "id",
                    "synonyms": ["pupils", "learners", "undergraduates"]
                },
                "projects": {
                    "columns": ["id", "name", "budget", "status"],
                    "primary_key": "id",
                    "synonyms": ["tasks", "initiatives", "assignments"]
                }
            },
            "relationships": [
                {"from": "employees.department_id", "to": "departments.id", "type": "MANY_TO_ONE"}
            ]
        }
        
    def get_serialized_schema(self, allowed_tables: list = None) -> str:
        """Returns the JSON serialization of the schema layout, optionally filtered."""
        if not allowed_tables:
            return json.dumps(self.schema, indent=2)
            
        filtered_schema = {
            "tables": {t: v for t, v in self.schema["tables"].items() if t in allowed_tables},
            "relationships": [r for r in self.schema["relationships"] 
                             if r["from"].split(".")[0] in allowed_tables 
                             and r["to"].split(".")[0] in allowed_tables]
        }
        return json.dumps(filtered_schema, indent=2)

    def validate_columns(self, table_name: str, requested_columns: list, allowed_tables: list = None) -> bool:
        """Validates if requested columns actually exist and the table is allowed."""
        if allowed_tables and table_name not in allowed_tables:
            return False
            
        if table_name not in self.schema["tables"]:
            return False
            
        valid_cols = self.schema["tables"][table_name]["columns"]
        for col in requested_columns:
            # We skip SQL functions like COUNT(*)
            if col != "*" and "(" not in col and col not in valid_cols:
                return False
        return True
