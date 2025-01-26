import tkinter as tk
import customtkinter as ctk  # Import customtkinter
from tkinter import messagebox
from main import main
from database import show_logged_in_students, conn, cursor
import re
import os
import json
import tkinter.font as tkFont
from PIL import Image, ImageTk

# Sample credentials for demonstration
admin_credentials = {
    "1": "1"  # Replace with your own admin username and password
}

# Global variables for entry fields
entry_student_number = None
entry_username = None
entry_password = None

def student_login():
    global entry_student_number
    student_number = entry_student_number.get()

    if not re.match(r"^[a-zA-Z0-9._%+-]+@iskolarngbayan\.pup\.edu\.ph$", student_number):
        messagebox.showwarning("Input Error", "Invalid student webmail format.")
        return
    
    if student_number:  # Check if student number is provided
        cursor.execute('SELECT * FROM students WHERE student_number = ?', (student_number,))
        student = cursor.fetchone()
        if not student:
            cursor.execute('INSERT INTO students (student_number) VALUES (?)', (student_number,))
            conn.commit()

        cursor.execute('SELECT * FROM logged_in_students WHERE student_number = ?', (student_number,))
        logged_in_student = cursor.fetchone()
        if not logged_in_student:
            cursor.execute('INSERT INTO logged_in_students (student_number) VALUES (?)', (student_number,))
            conn.commit()

        student_id = cursor.execute('SELECT id FROM students WHERE student_number = ?', (student_number,)).fetchone()[0]
        calendar_file = f"calendar_state_{student_id}.json"
        textbox_file = f"text_box_content_{student_id}.json"

        if not os.path.exists(calendar_file):
            with open(calendar_file, 'w') as f:
                json.dump({}, f)
        
        if not os.path.exists(textbox_file):
            with open(textbox_file, 'w') as f:
                json.dump({"content": ""}, f)

        messagebox.showinfo("Login Successful", f"Welcome Student {student_number}!")
        login_window.withdraw()

        main("student", student_id) 

    else:
        messagebox.showwarning("Input Error", "Please enter your student webmail.")

# Function to handle admin login
def admin_login():
    global entry_username, entry_password
    username = entry_username.get()
    password = entry_password.get()
    if username in admin_credentials and admin_credentials[username] == password:
        messagebox.showinfo("Login Successful", f"Welcome Admin {username}!")
        login_window.withdraw()
        main("admin") 
        
    else:
        messagebox.showwarning("Login Error", "Invalid username or password.")

# Function to clear the current window content
def clear_window(window):
    for widget in window.winfo_children():
        widget.destroy()

# Function to show the student login screen
def show_student_login(window):
    global entry_student_number
    clear_window(window)  # Clear the current content
    window.title("Student Login")

    image_path = "C:/Users/admin/Documents/project/pics/LOGIN.png"
    try:
       
        image = Image.open(image_path)
        image = image.resize((3650, 187))  
        photo_image = ImageTk.PhotoImage(image)  

        
        image_label = tk.Label(window, image=photo_image)
        image_label.image = photo_image  
        image_label.place(x=-100, y=0)  
    except Exception as e:
        print(f"Error loading image: {e}")

    # Add student login components
    label_student_number = tk.Label(window, text="Student Webmail:", font=("MS Sans Serif", 12))
    label_student_number.place(x=200, y=60) 

    entry_student_number = ctk.CTkEntry(window, width=250, font=("MS Sans Serif", 14), border_color="#272343", border_width=2)
    entry_student_number.place(x=130, y=100)

    # Use CTkButton for the login button
    button_login = ctk.CTkButton(window, text="Login", font=("MS Sans Serif", 15), command=student_login, width=250, height=50, fg_color="#BAE8E8", text_color="black")
    button_login.place(x=130, y=140)  

    label_switch = tk.Label(window, text="Switch to Admin Login", fg="blue", cursor="hand2", font=("MS Sans Serif", 11))
    label_switch.place(x=350, y=270)
    label_switch.bind("<Button-1>", lambda e: show_admin_login(window))  # Bind click event to show_admin_login

def show_admin_login(window):
    global entry_username, entry_password
    clear_window(window)  
    window.title("Admin Login")

    image_path = "C:/Users/admin/Documents/project/pics/LOGIN.png"
    try:
       
        image = Image.open(image_path)
        image = image.resize((3650, 185))  
        photo_image = ImageTk.PhotoImage(image)  

        
        image_label = tk.Label(window, image=photo_image)
        image_label.image = photo_image  
        image_label.place(x=-100, y=0)  
    except Exception as e:
        print(f"Error loading image: {e}")

    label_username = tk.Label(window, text="Username:", font=("MS Sans Serif", 12))
    label_username.place(x=213, y=50)

    entry_username = ctk.CTkEntry(window, width=250, font=("MS Sans Serif", 14), border_color="#272343", border_width=2)
    entry_username.place(x=130, y=80)

    label_password = tk.Label(window, text="Password:", font=("MS Sans Serif", 12))
    label_password.place(x=213, y=120)

    entry_password = ctk.CTkEntry(window, width=250, font=("MS Sans Serif", 14), show='*', border_color="#272343", border_width=2)
    entry_password.place(x=130, y=150)

    # Use CTkButton for the login button
    button_login = ctk.CTkButton(window, text="Login", font=("MS Sans Serif", 15), command=admin_login, width=250, height=50, fg_color="#BAE8E8", text_color="black")
    button_login.place(x=130, y=190)

    label_switch = tk.Label(window, text="Switch to Student Login", fg="blue", cursor="hand2", font=("MS Sans Serif", 11))
    label_switch.place(x=350, y=270)
    label_switch.bind("<Button-1>", lambda e: show_student_login(window))

def show_selection_screen(window):
    clear_window(window)  
    window.title("Login")
    
    label_title = tk.Label(window, text="LOGIN AS", font=("MS Sans Serif", 20))
    label_title.place(x=300, y=80)

    # Use CTkButton for the admin button
    button_admin = ctk.CTkButton(window, text="Admin", font=("MS Sans Serif", 14), command=lambda: show_admin_login(window), width=150, height=50, fg_color="#BAE8E8", text_color="black")
    button_admin.place(x=300, y=100)
    
    # Use CTkButton for the student button
    button_student = ctk.CTkButton(window, text="Student", font=("MS Sans Serif", 14), command=lambda: show_student_login(window), width=150, height=50, fg_color="#BAE8E8", text_color="black")
    button_student.place(x=75, y=100)

def center_window(window, width, height):
    screen_width = window.winfo_screenwidth()
    screen_height = window.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    window.geometry(f"{width}x{height}+{x}+{y}")

# Initialize the main login window
login_window = tk.Tk()  # Keep using Tk for the main window
login_window.geometry("500x300")
center_window(login_window, 500, 300)
login_window.iconbitmap('C:/Users/admin/Documents/project/pics/appicon.ico')    

sfont = ctk.CTkFont(family="MS Sans Serif", size=12, weight="bold")
bfont = ctk.CTkFont(family="MS Sans Serif", size=20, weight="bold")
hex_color = "#FDD037"

show_selection_screen(login_window)

# Load the background image using PIL
background_image = Image.open('C:/Users/admin/Documents/project/pics/background.png')
background_image = background_image.resize((500, 300))  # Resize to fit the window
background_photo = ImageTk.PhotoImage(background_image)

# Create a Label widget for the background image
background_label = tk.Label(login_window, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the entire window
background_label.image = background_photo  # Keep a reference to the image

# Load the image using PIL
image = Image.open('C:/Users/admin/Documents/project/pics/admin.png')
image = image.resize((135, 135))
photo_image = ImageTk.PhotoImage(image)

# Create a Label widget and set the image to it
image_label = tk.Label(login_window, image=photo_image, bg='white', borderwidth=0, highlightthickness=0)
image_label.image = photo_image  
image_label.place(x=60, y=73)

# Load the second image using PIL
image2 = Image.open('C:/Users/admin/Documents/project/pics/student.jpg')
image2 = image2.resize((135, 135))
photo_image2 = ImageTk.PhotoImage(image2)

# Create a Label widget and set the second image to it
image_label2 = tk.Label(login_window, image=photo_image2, bg='white', borderwidth=0, highlightthickness=0)
image_label2.image = photo_image2  
image_label2.place(x=290, y=73)

# Place the "Login As" title and buttons **after** the background and images
label_title = tk.Label(login_window, text="LOGIN AS", font=bfont, bg='white')
label_title.place(x=190, y=45)

# Use CTkButton for the admin button
button_admin = ctk.CTkButton(
    login_window,
    text="Admin",
    font=sfont,
    width=82,
    height=34,
    command=lambda: show_admin_login(login_window),
    fg_color="#BAE8E8", 
    text_color="black"
)
button_admin.place(x=315, y=195)

# Use CTkButton for the student button
button_student = ctk.CTkButton(
    login_window,
    text="Student",
    font=sfont,
    width=82,
    height=34,
    command=lambda: show_student_login(login_window),
    fg_color="#BAE8E8", 
    text_color="black"
)
button_student.place(x=85, y=195)

login_window.mainloop()