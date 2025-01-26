# database.py
import sqlite3

import tkinter as tk

# Establish a connection to the SQLite database
conn = sqlite3.connect('student_database.db')
cursor = conn.cursor()

# Create the students table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_number TEXT UNIQUE
    )
''')

# Create the logged_in_students table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS logged_in_students (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        student_number TEXT UNIQUE,
        login_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

def register_student(student_number):
    cursor.execute('SELECT * FROM students WHERE student_number = ?', (student_number,))
    if cursor.fetchone():
        return False  # Student already registered
    else:
        cursor.execute('INSERT INTO students (student_number) VALUES (?)', (student_number,))
        conn.commit()
        return True  # Registration successful


def get_logged_in_students():
    cursor.execute('SELECT * FROM logged_in_students')
    return cursor.fetchall()

def show_logged_in_students():
    top = tk.Toplevel()
    top.title("Logged In Students")
    rows = get_logged_in_students()
    listbox = tk.Listbox(top, width=50, height=20, font=("Arial", 12))
    listbox.pack(pady=20)
    for row in rows:
        listbox.insert(tk.END, f"ID: {row[0]}, Student Number: {row[1]}, Login Time: {row[2]}")