import tkinter as tk
from PIL import Image, ImageTk
import tkinter.font as tkFont
import customtkinter as ctk
from Mysched import *
from database import show_logged_in_students
from tkinter import filedialog
import json
import os



def main(user_type, student_id=None):
    new_window = tk.Tk()
    new_window.title("Main")
    new_window.geometry("1600x900")
    new_window.iconbitmap('C:/Users/admin/Documents/project/pics/appicon.ico')

        # Function to load and display the image
    def show_new_window():
        image_path = 'C:/Users/admin/Documents/project/pics/LOGIN.png'  # Update with your image path
        if not os.path.exists(image_path):
            print(f"Error: File does not exist at {image_path}")
            return

        try:
            image = Image.open(image_path)
            image = image.resize((3500, 187))
            photo1 = ImageTk.PhotoImage(image)
            
            # Create a label to display the image
            image_label = ctk.CTkLabel(header_frame, image=photo1)
            image_label.image = photo1  # Keep a reference to avoid garbage collection
            image_label.place(x=30, y=20)  # Adjust the position as needed
        except Exception as e:
            print(f"Error loading image: {e}")

    sfont = ctk.CTkFont(family="MS Sans Serif", size=12, weight="bold")
    bfont = ctk.CTkFont(family="MS Sans Serif", size=20, weight="bold")

    hex_color = "#FDD037"

    def on_mouse_wheel(event):

        canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    canvas = tk.Canvas(new_window, width=1280, height=680)
    scrollbar = ctk.CTkScrollbar(canvas, command=canvas.yview)
    scrollbar.grid(row=0, column=1, sticky="ns")
    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    new_window.bind_all("<MouseWheel>", on_mouse_wheel)

    content_frame = tk.Frame(canvas, width=1600, height=7000, bg="white", highlightbackground="black", highlightthickness=1)
    canvas.create_window((0, 0), window=content_frame, anchor="nw")

    # side panel // SELECTIONS
    side_panel = tk.Frame(new_window, width=250, height=900, bg="white", highlightbackground="black", highlightthickness=1)
    side_panel.place(x=0, y=0)

    header_frame = tk.Frame(side_panel, width=250, height=115, bg="#BAE8E8", highlightbackground="black", highlightthickness=1)  # Adjust height as needed
    header_frame.place(x=0, y=0)

    header_frame1 = tk.Frame(side_panel, width=250, height=4, bg="#BAE8E8", highlightbackground="black", highlightthickness=1)  # Adjust height as needed
    header_frame1.place(x=0, y=634)
    
    bfont = ("MS Sans Serif", 14)

    label_schedules = tk.Label(content_frame, text="Schedules", font=('MS Sans Serif', 24), bg="white")
    label_schedules.place(x=280, y=10)

    week_schedules = tk.Label(content_frame, text="Weekly Schedule", font=('MS Sans Serif', 25), bg="white")
    week_schedules.place(x=280, y=133)

#BUTTONS SA SIDE PANEL
    button1 = ctk.CTkButton(side_panel, text="Schedule", width=210, height=70, font=("MS Sans Serif", 16), 
                         command=lambda: scroll_to_cal_canvas(), fg_color="#BAE8E8", text_color="black", border_width=1, border_color="#272343")
    button1.place(x=17, y=190)

    button2 = ctk.CTkButton(side_panel, text="Make a Schedule", width=210, height=70, font=("MS Sans Serif", 16),
                         command=lambda: scroll_to_make_sched(), fg_color="#BAE8E8", text_color="black", border_width=1, border_color="#272343")
    button2.place(x=17, y=290)

    button3 = ctk.CTkButton(side_panel, text="My Schedule", width=210, height=70, font=("MS Sans Serif", 16),  
                        command=lambda: notepad(student_id), fg_color="#BAE8E8", text_color="black", border_width=1, border_color="#272343")
    button3.place(x=17, y=390)

    button4 = ctk.CTkButton(side_panel, text="PROJECTORS", width=210, height=70, font=("MS Sans Serif", 16),
                        command=lambda: scroll_to_equip_canvas(), fg_color="#BAE8E8", text_color="black", border_width=1, border_color="#272343")
    button4.place(x=17, y=490)

    button5 = ctk.CTkButton(side_panel, text="LOGOUT", width=210, height=70, font=("MS Sans Serif", 16), 
                        command=(new_window.quit), fg_color="#BAE8E8", text_color="black", border_width=1, border_color="#272343")
    button5.place(x=17, y=700)

# SCHEDULE CANVA UNG SINUSULATAN
    cal_canvas = tk.Canvas(content_frame, width=1200, height=900)
    cal_canvas.place(x=280, y=169)

    cal_frame = ctk.CTkFrame(cal_canvas, fg_color="lightblue",height=200, border_color="#272343", border_width=1)
    cal_canvas.create_window((0,0), window=cal_frame, anchor='nw')

    days = ["MON", "TUE", "WED", "THURS", "FRI", "SAT", "SUN"]
    text_widgets = {day: {} for day in days}
    text_data = {day: {f"Timeslot {j + 1}": "" for j in range(7)} for day in days}

    def load_projector_data():
        if os.path.exists("projector_data.json"):
            with open("projector_data.json", "r") as json_file:
                loaded_data = json.load(json_file)
                for day in days:
                    for timeslot in range(7):
                        cal_entry = text_widgets[day][f"Timeslot {timeslot + 1}"]
                        cal_entry.delete("1.0", tk.END) 
                        cal_entry.insert(tk.END, loaded_data.get(day, {}).get(f"Timeslot {timeslot + 1}", ""))
                        cal_entry.config(state=tk.NORMAL if user_type == "admin" else tk.DISABLED)
        
    def save_projector_data():
        data_to_save = {day: {f"Timeslot {j + 1}": text_widgets[day][f"Timeslot {j + 1}"].get("1.0", tk.END).strip() for j in range(7)} for day in days}
        with open("projector_data.json", "w") as json_file:
            json.dump(data_to_save, json_file, indent=4)  
        
    
    for i, day in enumerate(days):
        day_label = tk.Label(cal_frame, text=day, font=('MS Sans Serif', 12), bg="light blue")
        day_label.grid(row=0, column=i, padx=0, pady=0)

        for timeslot in range(7):
            cal_entry = tk.Text(cal_frame, width=15, height=5, font=('Arial', 14), wrap="word", highlightthickness=1, highlightbackground="#272343")
            cal_entry.grid(row=timeslot + 1, column=i, padx=0, pady=0)
            text_widgets[day][f"Timeslot {timeslot + 1}"] = cal_entry

    load_projector_data()
   
    if user_type == "admin":
        save_button = tk.Button(cal_canvas, text="Save", font=("MS Sans Serif", 12), command=save_projector_data, bd=0, bg="#FDD037", width=15, height=1)
        save_button.place(x=30, y=855)
    else:
        save_button = tk.Button(cal_canvas, text="Save", font=("MS Sans Serif", 12), bd=0, bg="#FDD037", width=15, height=1, state=tk.DISABLED)
        save_button.place(x=30, y=855)    

    button_view_logged_in_students = tk.Button(cal_canvas, text="View Logged In Students", font=("MS Sans Serifl", 12), bd=0, bg="#FDD037", command=show_logged_in_students, width=20, height=1)
    button_view_logged_in_students.place(x=190, y=855)

    if user_type == "admin":
        button_view_logged_in_students.config(state=tk.NORMAL)  # Allow editing for admin
    else:
        button_view_logged_in_students.config(state=tk.DISABLED)

        # Save data when the window is closed
    new_window.protocol("WM_DELETE_WINDOW", lambda: [save_projector_data(), new_window.destroy()])

#SEARCH PANEEEEEL ITU
    search_panel = ctk.CTkFrame(content_frame, width=1100, height=127, fg_color=hex_color, border_color="#272343", border_width=2)
    search_panel.place(x=280, y=50)

    search_entry = ctk.CTkEntry(search_panel, width=1100, font=('Arial', 14), border_color="#272343", border_width=1)
    search_entry.pack(side=tk.LEFT, padx=50, pady=20)

    result_frame = tk.Frame(content_frame, width=1100, height=300)
    result_frame.place(x=3500, y=95)  # Position it just below the search bar
    
    def show_results(event):
        result_frame.place(x=350, y=95)


    #Text widget to display search results
    result_text = tk.Text(result_frame, width=110, height=15, font=('Arial', 12), wrap="word")
    result_text.pack()


    def hide_results(event):
        result_frame.place(x=3500, y=205)
    

    # Function to perform the search
    def perform_search(event=None):
        search_term = search_entry.get().strip().lower()  # Get the search term
        result_text.delete("1.0", tk.END)  # Clear previous results
        

        found = False  
        if "projector 1" in search_term:
            result_text.insert(tk.END, specs_text.get("1.0", tk.END)) 
            found = True
        if "projector 2" in search_term:
            result_text.insert(tk.END, specs2_text.get("1.0", tk.END)) 
            found = True
        if "projector 3" in search_term:
            result_text.insert(tk.END, specs3_text.get("1.0", tk.END))  
            found = True
        if "projector 4" in search_term:
            result_text.insert(tk.END, specs4_text.get("1.0", tk.END))  
            found = True
        if "projector 5" in search_term:
            result_text.insert(tk.END, specs5_text.get("1.0", tk.END))  
            found = True
        if "projector 6" in search_term:
            result_text.insert(tk.END, specs6_text.get("1.0", tk.END)) 
            found = True
        if "speaker 1" in search_term:
            result_text.insert(tk.END, specs7_text.get("1.0", tk.END))  
            found = True
        if "speaker 2" in search_term:
            result_text.insert(tk.END, specs8_text.get("1.0", tk.END))  
            found = True

        if not found:
            result_text.insert(tk.END, "No results found.") 

    search_entry.bind("<FocusIn>", show_results)
    search_entry.bind("<FocusOut>", hide_results)
    search_entry.bind("<KeyRelease>", perform_search)

#CANVAS PARA SA PROJECTOR

    equip_canvas = tk.Canvas(content_frame, width=1190, height=4700, bg="#BAE8E8", bd=1, relief="solid")
    equip_canvas.place(x=280, y=2000)  # Place it below the cal_canvas
    equip_frame = tk.Frame(canvas,)
    canvas.create_window((0, 0), window=equip_frame, anchor='nw')
    
  # proj 1
    specs_text = tk.Text(equip_canvas, width=60, height=15, font=('Times New Roman', 16), wrap="word", bg="white", bd=2)
    specs_text.place(x=50, y=100)

    projector_1_label = tk.Label(equip_canvas, text="Projector 1", font=('Times New Roman', 21), bg="#BAE8E8")
    projector_1_label.place(x=50, y=50)
    # Insert some sample specs into the text widget
    specs_text.insert(tk.END, "    \n")
    specs_text.insert(tk.END, "    \n")
    specs_text.insert(tk.END, "    • Projector Specs:\n")
    specs_text.insert(tk.END, "    • Model: EPSON EB-2255U\n")
    specs_text.insert(tk.END, "    • Resolution: 1920x1200\n")
    specs_text.insert(tk.END, "    • Brightness: 2600 lumens\n")
    specs_text.insert(tk.END, "    • Contrast Ratio: 15000:1\n")
    specs_text.insert(tk.END, "    • Connectivity: HDMI, USB, Wireless\n")
    specs_text.config(state=tk.DISABLED)

# proj 2
    specs2_text = tk.Text(equip_canvas, width=60, height=15, font=('Times New Roman', 16), wrap="word", bg="white", bd=2)
    specs2_text.place(x=50, y=600)

    projector_2_label = tk.Label(equip_canvas, text="Projector 2", font=('Times New Roman',21), bg="#BAE8E8")
    projector_2_label.place(x=50, y=550)
    # Insert some sample specs into the text widget
    specs2_text.insert(tk.END, "    \n")
    specs2_text.insert(tk.END, "    \n")
    specs2_text.insert(tk.END, "    • Projector Specs:\n")
    specs2_text.insert(tk.END, "    • Model: EPSON EB-2255U\n")
    specs2_text.insert(tk.END, "    • Resolution: 1920x1200\n")
    specs2_text.insert(tk.END, "    • Brightness: 2600 lumens\n")
    specs2_text.insert(tk.END, "    • Contrast Ratio: 15000:1\n")
    specs2_text.insert(tk.END, "    • Connectivity: HDMI, USB, Wireless\n")
    specs2_text.config(state=tk.DISABLED)

#proj 3
    specs3_text = tk.Text(equip_canvas, width=60, height=15, font=('Times New Roman', 16), wrap="word", bg="white", bd=2)
    specs3_text.place(x=50, y=1100)

    projector_3_label = tk.Label(equip_canvas, text="Projector 3", font=('Times New Roman', 21), bg="#BAE8E8")
    projector_3_label.place(x=50, y=1050)
    # Insert some sample specs into the text widget
    specs3_text.insert(tk.END, "    \n")
    specs3_text.insert(tk.END, "    \n")
    specs3_text.insert(tk.END, "    • Projector Specs:\n")
    specs3_text.insert(tk.END, "    • Model: EPSON EB-2255U\n")
    specs3_text.insert(tk.END, "    • Resolution: 1920x1200\n")
    specs3_text.insert(tk.END, "    • Brightness: 2600 lumens\n")
    specs3_text.insert(tk.END, "    • Contrast Ratio: 15000:1\n")
    specs3_text.insert(tk.END, "    • Connectivity: HDMI, USB, Wireless\n")
    specs3_text.config(state=tk.DISABLED)


#proj 4
    specs4_text = tk.Text(equip_canvas, width=60, height=15, font=('Times New Roman', 16), wrap="word", bg="white", bd=2)
    specs4_text.place(x=50, y=1600)

    projector_4_label = tk.Label(equip_canvas, text="Projector 4", font=('Times New Roman', 21), bg="#BAE8E8")
    projector_4_label.place(x=50, y=1550)
    # Insert some sample specs into the text widget
    specs4_text.insert(tk.END, "    \n")
    specs4_text.insert(tk.END, "    \n")
    specs4_text.insert(tk.END, "    • Projector Specs:\n")
    specs4_text.insert(tk.END, "    • Model: EPSON EB-2255U\n")
    specs4_text.insert(tk.END, "    • Resolution: 1920x1200\n")
    specs4_text.insert(tk.END, "    • Brightness: 2600 lumens\n")
    specs4_text.insert(tk.END, "    • Contrast Ratio: 15000:1\n")
    specs4_text.insert(tk.END, "    • Connectivity: HDMI, USB, Wireless\n")
    specs4_text.config(state=tk.DISABLED)


#proj 5
    specs5_text = tk.Text(equip_canvas, width=60, height=15, font=('Times New Roman', 16), wrap="word", bg="white", bd=2)
    specs5_text.place(x=50, y=2100)

    projector_5_label = tk.Label(equip_canvas, text="Projector 5", font=('Times New Roman', 21), bg="#BAE8E8")
    projector_5_label.place(x=50, y=2000)
    # Insert some sample specs into the text widget
    specs5_text.insert(tk.END, "    \n")
    specs5_text.insert(tk.END, "    \n")
    specs5_text.insert(tk.END, "    • Projection Technology:\n")
    specs5_text.insert(tk.END, "    • RGB liquid crystal shutter projection system (3LCD)\n")
    specs5_text.insert(tk.END, "    • Resolution: 1920x1200\n")
    specs5_text.insert(tk.END, "    • Brightness: 2600 lumens\n")
    specs5_text.insert(tk.END, "    • Ratio: 15000:1\n")
    specs5_text.insert(tk.END, "    • Connectivity: HDMI, USB, Wireless\n")
    specs5_text.config(state=tk.DISABLED)


#proj 6
    specs6_text = tk.Text(equip_canvas, width=60, height=15, font=('Times New Roman', 16), wrap="word", bg="white", bd=2)
    specs6_text.place(x=50, y=2500)

    projector_6_label = tk.Label(equip_canvas, text="Projector 6", font=('Times New Roman', 21), bg="#BAE8E8")
    projector_6_label.place(x=50, y=2550)
    # Insert some sample specs into the text widget
    specs6_text.insert(tk.END, "    Projector Specs:\n")
    specs6_text.insert(tk.END, "    •Model: EPSON EB-2255U\n")
    specs6_text.insert(tk.END, "\n")
    specs6_text.insert(tk.END, "    •Connectivity:\n")
    specs6_text.insert(tk.END, "    •USB Interface:\n")
    specs6_text.insert(tk.END, "    - USB Type A: 1 (For Wireless LAN, Firmware Update, Copy OSD Settings)\n")
    specs6_text.insert(tk.END, "    - USB Type B: 1 (For Firmware Update, Copy OSD Settings\n")
    specs6_text.insert(tk.END, "    •Network:\n")
    specs6_text.insert(tk.END, "    - Wireless: Optional (ELPAP11)\n")
    specs6_text.insert(tk.END, "    - Composite: 1 RCA\n")
    specs6_text.insert(tk.END, "    - Composite: 1 RCD-Sub 15pin:1\n")
    specs6_text.insert(tk.END, "    •Digital Input:\n")
    specs6_text.insert(tk.END, "    - HDMI: 1 (MHL not supported)\n")
    specs6_text.insert(tk.END, "    •Audio Input:\n")
    specs6_text.insert(tk.END, "    - 2 RCA: 16\n")
    
    specs6_text.config(state=tk.DISABLED)


#proj 7
    specs7_text = tk.Text(equip_canvas, width=60, height=15, font=('Times New Roman', 16), wrap="word", bg="white", bd=2)
    specs7_text.place(x=50, y=3600)

    speaker_1_label = tk.Label(equip_canvas, text="Speaker 1", font=('Times New Roman', 21), bg="#BAE8E8")
    speaker_1_label.place(x=50, y=3550)
    # Insert some sample specs into the text widget
    specs7_text.insert(tk.END, "    Speaker details:\n")
    specs7_text.insert(tk.END, "    •Height (cm): 52.5\n")
    specs7_text.insert(tk.END, "    •Width (cm): 34.5\n")
    specs7_text.insert(tk.END, "    •Length (cm): 33.5\n")
    specs7_text.insert(tk.END, "    •Gross Weight (kg): 9.5kg\n")
    specs7_text.insert(tk.END, "    •Net Weight (kg): 8.5kg\n")
    specs7_text.insert(tk.END, "    •Power: 200 watts\n")
    specs7_text.insert(tk.END, "    vConnectivity: Bluetooth\n")
    specs7_text.insert(tk.END, "    •Warranty: 1 year on parts, labor, and service\n")
    specs7_text.insert(tk.END, "\n")
    specs7_text.insert(tk.END, "    Speaker Issues:\n")
    specs7_text.insert(tk.END, "    •Disorted audio\n")
    specs7_text.config(state=tk.DISABLED)


#proj 8
    specs8_text = tk.Text(equip_canvas, width=60, height=15, font=('Times New Roman', 16), wrap="word", bg="white", bd=2)
    specs8_text.place(x=50, y=4000)

    speaker_2_label = tk.Label(equip_canvas, text="Speaker 2", font=('Times New Roman', 21), bg="#BAE8E8")
    speaker_2_label.place(x=50, y=3950)
    # Insert some sample specs into the text widget
    
    specs8_text.insert(tk.END, "Speaker details:\n")
    specs8_text.insert(tk.END, "•Height (cm): 52.5\n")
    specs8_text.insert(tk.END, "•Width (cm): 34.5\n")
    specs8_text.insert(tk.END, "•Length (cm): 33.5\n")
    specs8_text.insert(tk.END, "•Gross Weight (kg): 9.5kg\n")
    specs8_text.insert(tk.END, "•Net Weight (kg): 8.5kg\n")
    specs8_text.insert(tk.END, "•Power: 200 watts\n")
    specs8_text.insert(tk.END, "•Connectivity: Bluetooth\n")
    specs8_text.insert(tk.END, "•Warranty: 1 year on parts, labor, and service\n")
    specs8_text.config(state=tk.DISABLED)

    equip_canvas.configure(scrollregion=equip_canvas.bbox("all"))  
   
#make a schedule section!!!!!!!
    file_canvas = tk.Canvas(content_frame, width=1190, height=700, bg="white", bd=1, relief="solid")
    file_canvas.place(x=280, y=1200)

    file_frame = tk.Frame(file_canvas, bg="lightblue", width=1190, height=700, bd=1, relief="solid")
    file_canvas.create_window((0, 0), window=file_frame, anchor='nw')

    sched_label = tk.Label(file_frame, text="Make a schedule", font=('MS Sans Serif', 24), bg="lightblue")
    sched_label.place(x=60,y=47)

    # Create a frame with a dark blue background
    design_frame = tk.Frame(file_frame, bg="#2b4257", width=380, height=508, bd=1, relief="solid")
    design_frame.place(x=698, y=90)

    steps = tk.Label(file_frame, text=" (Date)\n\n"
                         "[Recipient's Name]\n"
                         "[Recipient's Position/Title]\n"
                         "[Recipient's Year & Program]\n\n"
                         "Subject: Request for Projector\n\n"
                         "Dear MYLA G. HERNANDEZ,\n\n"
                         "Pleasantries!\n\n"
                         "We, [Recipient's Year & Program], would like to request permission to use one of the administrative\n"
                         "projectors for our class discussion on the following schedule:\n\n"
                         "[Date & Time] | [Course]\n\n"
                         "Sincerely,\n"
                         "[Your Full Name]\n\n"
                         "|| RESPONSE:", font=('Times New Roman', 12), bg="lightblue", wraplength=400, anchor='e', justify='left')
    steps.place(x=703,y=97)

    def saveFile():
        file = filedialog.asksaveasfile(initialdir="C:/Users/admin/Documents/project/Request Files",
                                        defaultextension='.txt',
                                        filetypes=[
                                            ("Text file", ".txt"),
                                            ("HTML file", ".html"),
                                            ("All files", ".*"),
                                        ])
        if file is None:
            return
        filetext = str(text.get(1.0, tk.END))
        file.write(filetext)
        file.close()

        # Create the Text widget || MAKE A SCHEDULE TXTBOX!!!!!!!!!!!
    text = ctk.CTkTextbox(file_frame, width=637, height=510, font=('Times New Roman', 16), wrap="word", border_color="#272343", border_width=2)
    text.place(x=55, y=90)

    pre_existing_text = '''This is pre-existing text that cannot be deleted.
Please use the following paragraph as a guide when drafting your request letter.''' 
    
    text.insert(tk.END, pre_existing_text)
   
    pre_existing_length = len(pre_existing_text)

    def prevent_deletion(event):
        
        try:
            start_index = text.index(tk.SEL_FIRST)
            end_index = text.index(tk.SEL_LAST)
        except tk.TclError:
           
            start_index = text.index(tk.INSERT)
            end_index = start_index

        if text.compare(start_index, "<", f"1.0+{pre_existing_length}c"):
            return "break"

    text.bind("<BackSpace>", prevent_deletion)
    text.bind("<Delete>", prevent_deletion)

    save_button = tk.Button(file_frame, width=20, height=2, text='Save file',font=('MS Sans Serif', 12), command=saveFile, bd=0, bg="#FDD037", highlightthickness=0)
    save_button.place(x=155, y=620)

    def update_file():
    
        file_path = filedialog.askopenfilename(initialdir="C:/Users/admin/Documents/project/Request Files",
                                            filetypes=[("Text file", ".txt"),
                                                        ("HTML file", ".html"),
                                                        ("All files", ".*")])
        if file_path:
        
            open_file_in_new_window(file_path)

    def open_file_in_new_window(file_path):
    
        edit_window = tk.Toplevel(new_window)
        edit_window.title("Edit File")
        edit_window.geometry("800x540")
        edit_window.iconbitmap('C:/Users/admin/Documents/project/pics/appicon.ico')

        edit_window.configure(bg="white")

        # Create a Text widget to display and edit the file content
        text_edit = ctk.CTkTextbox(edit_window, width=760, height=420, font=('Times New Roman', 16), wrap="word",  border_color="#272343", border_width=2)
        text_edit.place(x=20, y=20)

        # Load the file content into the Text widget
        with open(file_path, 'r') as file:
            file_contents = file.read()
        text_edit.insert(tk.END, file_contents)

        # Create a Save button to save the changes
        save_button = tk.Button(edit_window, text="Save", font= sfont, width=20, height=2, command=lambda: save_changes(file_path, text_edit), bg="#BAE8E8")
        save_button.place(x=320, y=450)

    def save_changes(file_path, text_edit):
        # Save the changes back to the file
        with open(file_path, 'w') as file:
            file.write(text_edit.get(1.0, tk.END))
        tk.messagebox.showinfo("Success", "File updated successfully!")
        
    update_button = tk.Button(file_frame, width=20, height=2, text='Update', font=('MS Sans Serif', 12), command=update_file, bd=0, bg="#FDD037", highlightthickness=0)
    update_button.place(x=810, y=620)

    # Enable or disable the Update button based on user type
    if user_type == "admin":
        update_button.config(state="normal")  # Allow editing for admin
    else:
        update_button.config(state="disabled")

    def delete_file():
    # Open a file dialog to select a file
        file_path = filedialog.askopenfilename(initialdir="C:/Users/admin/Documents/project/Request Files",
                                            filetypes=[("All files", ".*")])
        if file_path:
            try:
                os.remove(file_path)  # Delete the selected file
                tk.messagebox.showinfo("Success", "File deleted successfully!")
            except Exception as e:
                tk.messagebox.showerror("Error", f"Failed to delete file: {e}")

    delete_button = tk.Button(file_frame, width=20, height=2, text='Delete',font=('MS Sans Serif', 12), command=delete_file, bd=0, bg="#FDD037", highlightthickness=1)
    delete_button.place(x=390, y=620)

    content_frame.update_idletasks()
    canvas.configure(scrollregion=canvas.bbox("all"))
    cal_canvas.configure(scrollregion=cal_canvas.bbox("all"))
    file_canvas.configure(scrollregion=file_canvas.bbox("all"))
    equip_canvas.configure(scrollregion=equip_canvas.bbox("all"))
    
    #button scroll function
    def scroll_to_equip_canvas(): 
        equip_canvas_y = 2000  
        canvas.yview_moveto(equip_canvas_y / 7000)

    def scroll_to_cal_canvas(): 
        cal_canvas_y = 125 
        canvas.yview_moveto(cal_canvas_y / 7000)
    
    def scroll_to_make_sched(): 
        cal_canvas_y = 1150  
        canvas.yview_moveto(cal_canvas_y / 7000)

    scroll_to_top_button = tk.Button(new_window, text="Back to top", width=9, height=2, bg="#404040", fg="white", font=('Arial', 10, 'bold'), command=lambda: canvas.yview_moveto(0))
    scroll_to_top_button.place(x=1500, y=775)  # Place the button at the bottom right of the content frame
    
    show_new_window()
    new_window.mainloop()