import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "company.db")

def create_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Create Departments table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        location TEXT NOT NULL
    )
    """)

    # Create Employees table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        role TEXT NOT NULL,
        salary INTEGER NOT NULL,
        department_id INTEGER,
        FOREIGN KEY (department_id) REFERENCES departments(id)
    )
    """)

    # Create Students table (for demo purposes)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        grade TEXT,
        enrollment_date DATE
    )
    """)

    # Create Projects table (New default table)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        budget INTEGER,
        status TEXT DEFAULT 'Planning'
    )
    """)

    # Insert sample data
    cursor.executemany("INSERT INTO departments (name, location) VALUES (?, ?) ON CONFLICT DO NOTHING", [
        ("Engineering", "New York"),
        ("Sales", "London"),
        ("Marketing", "San Francisco")
    ])

    cursor.executemany("INSERT INTO employees (name, role, salary, department_id) VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING", [
        ("Alice Smith", "Software Engineer", 120000, 1),
        ("Bob Jones", "Data Scientist", 130000, 1),
        ("Charlie Brown", "Sales Manager", 95000, 2),
        ("Diana Prince", "Marketing Lead", 110000, 3)
    ])

    cursor.executemany("INSERT INTO students (name, age, grade, enrollment_date) VALUES (?, ?, ?, ?) ON CONFLICT DO NOTHING", [
        ("Hariharan", 21, "A", "2023-01-15"),
        ("Rahul Kumar", 22, "B", "2023-02-10"),
        ("Sneha Rao", 20, "A+", "2023-03-05")
    ])

    cursor.executemany("INSERT INTO projects (name, budget, status) VALUES (?, ?, ?) ON CONFLICT DO NOTHING", [
        ("Project Alpha", 50000, "Active"),
        ("Project Beta", 75000, "Completed"),
        ("Project Gamma", 30000, "Planning")
    ])

    conn.commit()
    conn.close()
    print(f"Database initialized successfully at {DB_PATH}")

if __name__ == "__main__":
    create_db()
