import tkinter as tk
from calendar import monthrange
from datetime import date
from tkinter import filedialog
import tkinter.font as tkFont
import customtkinter as ctk
import json
from PIL import Image, ImageTk

# Constants for consistent design
MONTH_LABEL_FONT = ('MS Sans Serif', 24)
DAY_BUTTON_FONT = ('MS Sans Serif', 12)
NAV_BUTTON_FONT = ('MS Sans Serif', 14)
MONTH_LABEL_BG = "lightblue"
DAY_BUTTON_BG = "white"
NAV_BUTTON_BG = "#FDD037"
DAY_BUTTON_WIDTH = 10
DAY_BUTTON_HEIGHT = 3
NAV_BUTTON_WIDTH = 10
NAV_BUTTON_HEIGHT = 2

def notepad(student_id):
    note = tk.Tk()
    note.title("Mysched")
    note.geometry("1200x700")


    def center_window(window, width, height):
        screen_width = window.winfo_screenwidth()  # Get screen width
        screen_height = window.winfo_screenheight()  # Get screen height
        x = (screen_width // 2) - (width // 2)  # Calculate x position
        y = (screen_height // 2) - (height // 2)  # Calculate y position
        window.geometry(f"{width}x{height}+{x}+{y}")  # Set window geometry

    # Center the window
    center_window(note, 1200, 700)
    
    # Create a canvas
    note_canvas = tk.Canvas(note, width=1200, height=700)
    note_canvas.pack(fill="both", expand=True)  # Pack the canvas into the window

    # Create a frame inside the canvas
    note_frame = tk.Frame(note_canvas, width=1200, height=700, bg="#F3FBFB")
    note_canvas.create_window((0, 0), window=note_frame, anchor="nw")

    sfont = tkFont.Font(family="MS Sans Serif", size=12, weight="bold")
    bfont = tkFont.Font(family="MS Sans Serif", size=20, weight="bold") 

    hex_color = "#FDD037"
    
    label = tk.Label(note_frame, text="Notepad", font=('MS Sans Serif', 24), bg="white")
    label.place(x=95, y=55)

    text_box_frame = tk.Frame(note_frame, width=800, height=800, bg="black")
    text_box_frame.place(x=100, y=100)

    text_box = ctk.CTkTextbox(text_box_frame, width=475, height=470, font=('Arial', 12), border_color="#272343", border_width=2)
    text_box.pack(fill="both", expand=True)

  
    calendar_frame = tk.Frame(note_frame, width=500, height=500, bg="lightblue")
    calendar_frame.place(x=600, y=100)

    # Get the current date
    today = date.today()
    year = today.year
    month = today.month

    # Get the number of days in the month
    num_days = monthrange(year, month)[1]

    # Create a calendar
    month_name = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]
    month_label = tk.Label(calendar_frame, text=f"{month_name[month-1]} {year}", font=('MS Sans Serif', 24), bg="lightblue")
    month_label.place(x=150, y=25)

    first_day = 2 
    for i in range(num_days):
        day_button = tk.Button(calendar_frame, text=str(i+1), width=10, height=3, bg="white", command=lambda day=i+1: change_day_color(day))
        day_button.place(x=((i + first_day - 1) % 7) * 70, y=((i + first_day - 1) // 7) * 50 + 100)
        # Function to change the color of a day
    def change_day_color(day):
        for widget in calendar_frame.winfo_children():
            if widget.cget("text") == str(day):
                if widget.cget("bg") == "white":
                    widget.config(bg="#fff9c7")
                else:
                    widget.config(bg="white")
        save_calendar_state()

    # Function to save the calendar state
    def save_calendar_state():
        calendar_file = f"calendar_state_{student_id}.json"
        try:
            with open(calendar_file, "r") as f:
                calendar_state = json.load(f)
        except FileNotFoundError:
            calendar_state = {}
        for widget in calendar_frame.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") != "Next" and widget.cget("text") != "Previous":
                
                try:
                    day = int(widget.cget("text"))
                    calendar_state[f"{year}-{month}-{day}"] = widget.cget("bg")
                except ValueError:
                    pass
        with open(calendar_file, "w") as f:
            json.dump(calendar_state, f)

    def load_calendar_state():
        calendar_file = f"calendar_state_{student_id}.json"
        try:
            with open(calendar_file, "r") as f:
                calendar_state = json.load(f)
            for widget in calendar_frame.winfo_children():
                if isinstance(widget, tk.Button) and widget.cget("text") != "Next" and widget.cget("text") != "Previous":
                    try:
                        day = int(widget.cget("text"))
                        widget.config(bg=calendar_state.get(f"{year}-{month}-{day}", "white"))
                    except ValueError:
                        pass
        except FileNotFoundError:
            pass

    # Function to go to the next month
    def next_month():
        nonlocal month, year, num_days
        if month == 12:
            month = 1
            year += 1
        else:
            month += 1
        num_days = monthrange(year, month)[1]
        update_calendar()

    # Function to go to the previous month
    def prev_month():
        nonlocal month, year, num_days
        if month == 1:
            month = 12
            year -= 1
        else:
            month -= 1
        num_days = monthrange(year, month)[1]
        update_calendar()

    # Function to update the calendar
    def update_calendar():
        for widget in calendar_frame.winfo_children():
            if widget != next_button and widget != prev_button:
                widget.destroy()
        month_label = tk.Label(calendar_frame, text=f"{month_name[month-1]} {year}", font=('MS Sans Serif', 24), bg="lightblue")
        month_label.place(x=150, y=25)
        
        for i in range(num_days):
            day_button = tk.Button(calendar_frame, text=str(i+1), width=10, height=3, bg="white", command=lambda day=i+1: change_day_color(day))
            day_button.place(x=((i + first_day - 1) % 7) * 70, y=((i + first_day - 1) // 7) * 50 + 100)
        next_button.place(x=285, y=400)
        prev_button.place(x=85, y=400)
        load_calendar_state()

    # CALENDAR BUTTONS
    next_button = tk.Button(calendar_frame, text="Next", width=10, height=2, font=sfont, command=next_month, bg="#FDD037", bd=0)
    next_button.place(x=285, y=400)

    prev_button = tk.Button(calendar_frame, text="Previous", width=10, height=2, font=sfont,command=prev_month, bg="#FDD037", bd=0)
    prev_button.place(x=85, y=400)

    def save_text_box_content():
        textbox_file = f"text_box_content_{student_id}.json"
        with open(textbox_file, "w") as f:
            json.dump({"content": text_box.get("1.0", tk.END)}, f)

    # Function to load the text box content
    def load_text_box_content():
        textbox_file = f"text_box_content_{student_id}.json"
        try:
            with open(textbox_file, "r") as f:
                data = json.load(f)
                text_box.delete("1.0", tk.END)  # Clear existing content
                text_box.insert(tk.END, data.get("content", ""))
        except FileNotFoundError:
            pass

    # Load the calendar state when the application starts
    load_calendar_state()
    load_text_box_content()

    def open_file():
        # Open the saved file
        file_path = filedialog.askopenfilename(initialdir="C:/Users/admin/Documents/project/Request Files",
                                            filetypes=[("Text file", ".txt"),
                                                        ("HTML file", ".html"),
                                                        ("All files", ".*")])
        if file_path:
            # Clear the Text widget
            text_box.delete(1.0, tk.END)

            # Open the file and read its contents
            with open(file_path, 'r') as file:
                file_contents = file.read()

            # Insert the file contents into the Text widget
            text_box.insert(tk.END, file_contents)

#OPEN FILE BUTTON
    open_button = tk.Button(note_frame, width=20, height=2, text='Open File', font=sfont, command=open_file, bg="#FDD037")
    open_button.place(x=195, y=580)
    note.protocol("WM_DELETE_WINDOW", lambda: (save_text_box_content(), note.destroy()))

        # New frame creation below all buttons and calendar
    footer_frame = tk.Frame(note_frame, width=1500, height=50, bg="lightblue", bd=1, relief="solid")
    footer_frame.place(x=0, y=0)  # Adjusted position

    # Create another footer frame
    footer_frame_1 = tk.Frame(note_frame, width=1500, height=50, bg="lightblue", bd=1, relief="solid")
    footer_frame_1.place(x=0, y=650)  # Adjusted position

    note.mainloop()