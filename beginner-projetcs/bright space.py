from tkinter import *
from tkinter import messagebox
import sqlite3
import os
import json

# Database connection
conn = sqlite3.connect('students.db')
cursor = conn.cursor()

# Create table if not exists
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    program TEXT NOT NULL,
    year INTEGER NOT NULL
)
""")
conn.commit()


PRIMARY_COLOR = "#2c3e50"
SECONDARY_COLOR = "#3498db"
ACCENT_COLOR = "#e74c3c"
SUCCESS_COLOR = "#27ae60"
WARNING_COLOR = "#f39c12"
BG_LIGHT = "#ecf0f1"
TEXT_DARK = "#2c3e50"
TEXT_LIGHT = "#bdc3c7"


class LoginSystem:
    def __init__(self):
        self.users_file = "users.json"
        self.load_users()

    def load_users(self):
        if os.path.exists(self.users_file):
            with open(self.users_file, 'r') as f:
                self.users = json.load(f)
        else:
            self.users = {"admin": {"password": "admin123", "role": "admin"}}
            self.save_users()

    def save_users(self):
        with open(self.users_file, 'w') as f:
            json.dump(self.users, f)

    def authenticate(self, username, password):
        if username in self.users and self.users[username]["password"] == password:
            return True
        return False

    def add_user(self, username, password, role="user"):
        if username not in self.users:
            self.users[username] = {"password": password, "role": role}
            self.save_users()
            return True
        return False


login_system = LoginSystem()
current_user = None


def show_login_screen(win, show_main_callback):
    for widget in win.winfo_children():
        widget.destroy()

    win.title("Login - Student Record System")
    win.geometry("500x550")
    win.resizable(False, False)

    main_frame = Frame(win)
    main_frame.pack(fill="both", expand=True)
    main_frame.configure(bg=PRIMARY_COLOR)

    decoration = Frame(main_frame, bg=SECONDARY_COLOR, height=5)
    decoration.pack(fill=X)

    title_label = Label(main_frame, text="📚 WELCOME TO BRIGHT SPACE",
                        font=('Arial', 20, 'bold'),
                        fg="white", bg=PRIMARY_COLOR)
    title_label.pack(pady=30)

    subtitle_label = Label(main_frame, text="Please Login to Continue",
                           font=('Arial', 11),
                           fg=TEXT_LIGHT, bg=PRIMARY_COLOR)
    subtitle_label.pack(pady=5)

    login_card = Frame(main_frame, bg="white", bd=0, relief=FLAT)
    login_card.pack(pady=30, padx=40, fill="both", expand=True)

    
    content_frame = Frame(login_card, bg="white")
    content_frame.pack(padx=30, pady=30, fill="both", expand=True)

    Label(content_frame, text="Username", font=('Arial', 11, 'bold'),
          bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))
    username_entry = Entry(content_frame, font=('Arial', 11),
                           bd=1, relief=SOLID, bg=BG_LIGHT, fg=TEXT_DARK)
    username_entry.pack(fill="x", pady=(0, 15), ipady=10)

    Label(content_frame, text="Password", font=('Arial', 11, 'bold'),
          bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))
    password_entry = Entry(content_frame, font=('Arial', 11),
                           show="•", bd=1, relief=SOLID, bg=BG_LIGHT, fg=TEXT_DARK)
    password_entry.pack(fill="x", pady=(0, 20), ipady=10)

    error_label = Label(content_frame, text="", fg=ACCENT_COLOR,
                        bg="white", font=('Arial', 9, 'bold'))
    error_label.pack(pady=(0, 10))

    def do_login():
        username = username_entry.get().strip()
        password = password_entry.get()

        if not username or not password:
            error_label.config(text="❌ Please enter username and password")
            return

        if login_system.authenticate(username, password):
            global current_user
            current_user = username
            messagebox.showinfo("Login Success", f"Welcome, {username}!")
            show_main_callback()
        else:
            error_label.config(text="❌ Invalid username or password")

    def do_login_enter(event):
        do_login()

    def show_register():
        for widget in content_frame.winfo_children():
            widget.destroy()

        Label(content_frame, text="CREATE NEW ACCOUNT",
              font=('Arial', 14, 'bold'),
              bg="white", fg=TEXT_DARK).pack(pady=(0, 20))

        Label(content_frame, text="Username", font=('Arial', 11, 'bold'),
              bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))
        reg_username = Entry(content_frame, font=('Arial', 11),
                             bd=1, relief=SOLID, bg=BG_LIGHT, fg=TEXT_DARK)
        reg_username.pack(fill="x", pady=(0, 15), ipady=10)

        Label(content_frame, text="Password", font=('Arial', 11, 'bold'),
              bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))
        reg_password = Entry(content_frame, font=('Arial', 11),
                             show="•", bd=1, relief=SOLID, bg=BG_LIGHT, fg=TEXT_DARK)
        reg_password.pack(fill="x", pady=(0, 15), ipady=10)

        Label(content_frame, text="Confirm Password", font=('Arial', 11, 'bold'),
              bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))
        reg_confirm = Entry(content_frame, font=('Arial', 11),
                            show="•", bd=1, relief=SOLID, bg=BG_LIGHT, fg=TEXT_DARK)
        reg_confirm.pack(fill="x", pady=(0, 20), ipady=10)

        reg_error = Label(content_frame, text="", fg=ACCENT_COLOR,
                          bg="white", font=('Arial', 9, 'bold'))
        reg_error.pack(pady=(0, 10))

        def do_register():
            username = reg_username.get().strip()
            password = reg_password.get()
            confirm = reg_confirm.get()

            if not username or not password:
                reg_error.config(text="❌ Please fill all fields")
                return

            if password != confirm:
                reg_error.config(text="❌ Passwords do not match")
                return

            if login_system.add_user(username, password, "user"):
                reg_error.config(text="✅ Registration successful!", fg=SUCCESS_COLOR)
                content_frame.after(2000, lambda: create_login_form())
            else:
                reg_error.config(text="❌ Username already exists")

        def back_to_login():
            create_login_form()

        Button(content_frame, text="REGISTER", command=do_register,
               bg=SUCCESS_COLOR, fg="white", font=('Arial', 11, 'bold'),
               width=20, pady=10, bd=0, cursor="hand2", activebackground="#229954").pack(pady=(10, 10))

        Button(content_frame, text="← Back to Login", command=back_to_login,
               bg="#95a5a6", fg="white", font=('Arial', 11),
               width=20, pady=10, bd=0, cursor="hand2", activebackground="#7f8c8d").pack()

    def create_login_form():
        for widget in content_frame.winfo_children():
            widget.destroy()
        Label(content_frame, text="Username", font=('Arial', 11, 'bold'),
              bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))
        username_entry = Entry(content_frame, font=('Arial', 11),
                               bd=1, relief=SOLID, bg=BG_LIGHT, fg=TEXT_DARK)
        username_entry.pack(fill="x", pady=(0, 15), ipady=10)

        Label(content_frame, text="Password", font=('Arial', 11, 'bold'),
              bg="white", fg=TEXT_DARK).pack(anchor="w", pady=(0, 8))
        password_entry = Entry(content_frame, font=('Arial', 11),
                               show="•", bd=1, relief=SOLID, bg=BG_LIGHT, fg=TEXT_DARK)
        password_entry.pack(fill="x", pady=(0, 20), ipady=10)

        error_label = Label(content_frame, text="", fg=ACCENT_COLOR,
                            bg="white", font=('Arial', 9, 'bold'))
        error_label.pack(pady=(0, 10))

        def do_login():
            username = username_entry.get().strip()
            password = password_entry.get()

            if not username or not password:
                error_label.config(text="❌ Please enter username and password")
                return

            if login_system.authenticate(username, password):
                global current_user
                current_user = username
                messagebox.showinfo("Login Success", f"Welcome, {username}!")
                show_main_callback()
            else:
                error_label.config(text="❌ Invalid username or password")

        def do_login_enter(event):
            do_login()

        Button(content_frame, text="LOGIN", command=do_login,
               bg=SECONDARY_COLOR, fg="white", font=('Arial', 11, 'bold'),
               width=20, pady=10, bd=0, cursor="hand2", activebackground="#2980b9").pack(pady=(10, 10))

        Button(content_frame, text="Create New Account", command=show_register,
               bg=WARNING_COLOR, fg="white", font=('Arial', 11),
               width=20, pady=10, bd=0, cursor="hand2", activebackground="#e67e22").pack()

        username_entry.bind('<Return>', do_login_enter)
        password_entry.bind('<Return>', do_login_enter)

    create_login_form()


class Database:
    def __init__(self, connection, cursor):
        self.conn = connection
        self.cursor = cursor

    def add(self, student):
        try:
            self.cursor.execute(
                "INSERT INTO students (id, name, program, year) VALUES (?, ?, ?, ?)",
                (student['id'], student['name'], student['program'], int(student['year']))
            )
            self.conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error adding student: {e}")
            return False

    def get_all(self):
        self.cursor.execute("SELECT id, name, program, year FROM students ORDER BY id")
        rows = self.cursor.fetchall()
        students = []
        for row in rows:
            students.append({
                'id': row[0],
                'name': row[1],
                'program': row[2],
                'year': str(row[3])
            })
        return students

    def get(self, student_id):
        self.cursor.execute("SELECT id, name, program, year FROM students WHERE id = ?", (student_id,))
        row = self.cursor.fetchone()
        if row:
            return {
                'id': row[0],
                'name': row[1],
                'program': row[2],
                'year': str(row[3])
            }
        return None

    def update(self, student_id, new_data):
        try:
            self.cursor.execute(
                "UPDATE students SET name = ?, program = ?, year = ? WHERE id = ?",
                (new_data['name'], new_data['program'], int(new_data['year']), student_id)
            )
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error updating student: {e}")
            return False

    def delete(self, student_id):
        try:
            self.cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
            self.conn.commit()
            return self.cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error deleting student: {e}")
            return False


class Stack:
    def __init__(self):
        self.items = []

    def push(self, op): self.items.append(op)

    def pop(self): return self.items.pop() if self.items else None

    def is_empty(self): return len(self.items) == 0


class Queue:
    def __init__(self):
        self.items = []

    def enqueue(self, sid): self.items.append(sid)

    def dequeue(self): return self.items.pop(0) if self.items else None

    def is_empty(self): return len(self.items) == 0


db, stack, queue = Database(conn, cursor), Stack(), Queue()
updating = None


def refresh():
    listbox.delete(0, END)
    for idx, student in enumerate(db.get_all()):
        # Alternate row colors for better readability
        display_text = f"{student['id']:^10} | {student['name']:^20} | {student['program']:^15} | Year {student['year']}"
        listbox.insert(END, display_text)


def add_update():
    global updating
    student_id, name, program, year = id_e.get(), name_e.get(), prog_e.get(), year_e.get()
    if not (student_id and name and program and year):
        messagebox.showerror("Error", "❌ All fields required!")
        return

    student = {"id": student_id, "name": name, "program": program, "year": year}

    if updating:
        old_student = db.get(updating)
        stack.push({'type': 'UPDATE', 'old': old_student, 'id': updating})
        db.update(updating, student)
        messagebox.showinfo("Success", "✅ Student updated successfully!")
        updating = None
        add_btn.config(text="ADD", bg=SUCCESS_COLOR)
    else:
        if db.get(student_id):
            messagebox.showerror("Error", "❌ ID already exists!")
            return
        stack.push({'type': 'ADD', 'student': student})
        db.add(student)
        messagebox.showinfo("Success", "✅ Student added successfully!")

    refresh()
    clear()


def search():
    student = db.get(id_e.get())
    if student:
        clear()
        id_e.insert(0, student['id'])
        name_e.insert(0, student['name'])
        prog_e.insert(0, student['program'])
        year_e.insert(0, student['year'])
        messagebox.showinfo("Found", "✅ Student found!")
    else:
        messagebox.showerror("Error", "❌ Student not found!")


def select_update():
    try:
        selected_index = listbox.curselection()[0]
        student = db.get_all()[selected_index]
        global updating
        updating = student['id']
        clear()
        id_e.insert(0, student['id'])
        name_e.insert(0, student['name'])
        prog_e.insert(0, student['program'])
        year_e.insert(0, student['year'])
        add_btn.config(text="UPDATE", bg=WARNING_COLOR)
    except:
        messagebox.showerror("Error", "❌ Please select a student!")


def delete():
    try:
        selected_index = listbox.curselection()[0]
        student = db.get_all()[selected_index]
        if messagebox.askyesno("Confirm", f"Delete {student['name']}?"):
            stack.push({'type': 'DELETE', 'student': student})
            db.delete(student['id'])
            if updating == student['id']:
                cancel()
            refresh()
            messagebox.showinfo("Success", "✅ Student deleted successfully!")
    except:
        messagebox.showerror("Error", "❌ Please select a student!")


def undo():
    if stack.is_empty():
        messagebox.showinfo("Undo", "ℹ️ Nothing to undo!")
        return
    operation = stack.pop()
    if operation['type'] == 'ADD':
        db.delete(operation['student']['id'])
    elif operation['type'] == 'DELETE':
        db.add(operation['student'])
    elif operation['type'] == 'UPDATE':
        db.update(operation['id'], operation['old'])
    refresh()
    messagebox.showinfo("Undo", "✅ Action undone!")


def add_queue():
    try:
        selected_index = listbox.curselection()[0]
        student = db.get_all()[selected_index]
        queue.enqueue(student['id'])
        messagebox.showinfo("Queue", f"✅ {student['name']} added to queue!")
    except:
        messagebox.showerror("Error", "❌ Please select a student!")


def process_queue():
    if queue.is_empty():
        messagebox.showinfo("Queue", "ℹ️ Queue is empty!")
        return
    student_id = queue.dequeue()
    student = db.get(student_id)
    if student:
        messagebox.showinfo("Processing", f"📋 Processing: {student['name']}")
    else:
        messagebox.showwarning("Warning", "⚠️ Student not found!")


def show_queue():
    if queue.is_empty():
        messagebox.showinfo("Queue", "ℹ️ Queue is empty!")
        return
    message_text = "📋 REGISTRATION QUEUE:\n" + "=" * 40 + "\n"
    for position, student_id in enumerate(queue.items, 1):
        student = db.get(student_id)
        if student:
            message_text += f"{position}. {student['name']} (ID: {student_id})\n"
    messagebox.showinfo("Queue", message_text)


def clear():
    id_e.delete(0, END)
    name_e.delete(0, END)
    prog_e.delete(0, END)
    year_e.delete(0, END)


def cancel():
    global updating
    updating = None
    clear()
    add_btn.config(text="ADD", bg=SUCCESS_COLOR)


def show_main_app(win):
    for widget in win.winfo_children():
        widget.destroy()

    win.title("Student Record System")
    win.geometry("900x700")
    win.resizable(True, True)

    global id_e, name_e, prog_e, year_e, add_btn, listbox


    user_frame = Frame(win, bg=PRIMARY_COLOR, height=60)
    user_frame.pack(fill=X, padx=0, pady=0)

    Label(user_frame, text=f"👤 Logged in as: {current_user}", font=('Arial', 10, 'bold'),
          bg=PRIMARY_COLOR, fg="white").pack(side=LEFT, padx=15, pady=10)

    def logout():
        if messagebox.askyesno("Logout", "Are you sure you want to logout?"):
            show_login_screen(win, lambda: show_main_app(win))

    Button(user_frame, text="🚪 Logout", command=logout, bg=ACCENT_COLOR, fg="white",
           font=('Arial', 9, 'bold'), padx=15, pady=8, bd=0, cursor="hand2").pack(side=RIGHT, padx=15, pady=10)


    title_frame = Frame(win, bg=BG_LIGHT)
    title_frame.pack(fill=X, padx=0, pady=10)
    Label(title_frame, text='📚 STUDENT RECORD SYSTEM', font=('Arial', 16, 'bold'),
          bg=BG_LIGHT, fg=TEXT_DARK).pack()


    input_card = LabelFrame(win, text=" STUDENT INFORMATION ", font=('Arial', 10, 'bold'),
                            bg=BG_LIGHT, fg=TEXT_DARK, padx=15, pady=15)
    input_card.pack(padx=15, pady=10, fill="x")


    left_frame = Frame(input_card, bg=BG_LIGHT)
    left_frame.pack(side=LEFT, padx=10)

    Label(left_frame, text='ID:', font=('Arial', 10, 'bold'), bg=BG_LIGHT, fg=TEXT_DARK).pack(anchor="w", pady=(0, 5))
    id_e = Entry(left_frame, font=('Arial', 10), bd=1, relief=SOLID, bg="white", width=20)
    id_e.pack(fill="x", pady=(0, 15))

    Label(left_frame, text='Program:', font=('Arial', 10, 'bold'), bg=BG_LIGHT, fg=TEXT_DARK).pack(anchor="w",
                                                                                                   pady=(0, 5))
    prog_e = Entry(left_frame, font=('Arial', 10), bd=1, relief=SOLID, bg="white", width=20)
    prog_e.pack(fill="x", pady=(0, 15))

    right_frame = Frame(input_card, bg=BG_LIGHT)
    right_frame.pack(side=LEFT, padx=10)

    Label(right_frame, text='Name:', font=('Arial', 10, 'bold'), bg=BG_LIGHT, fg=TEXT_DARK).pack(anchor="w",
                                                                                                 pady=(0, 5))
    name_e = Entry(right_frame, font=('Arial', 10), bd=1, relief=SOLID, bg="white", width=20)
    name_e.pack(fill="x", pady=(0, 15))

    Label(right_frame, text='Year:', font=('Arial', 10, 'bold'), bg=BG_LIGHT, fg=TEXT_DARK).pack(anchor="w",
                                                                                                 pady=(0, 5))
    year_e = Entry(right_frame, font=('Arial', 10), bd=1, relief=SOLID, bg="white", width=20)
    year_e.pack(fill="x", pady=(0, 15))


    button_frame = Frame(win, bg="white")
    button_frame.pack(padx=15, pady=10, fill="x")


    Label(button_frame, text="DATA OPERATIONS", font=('Arial', 9, 'bold'),
          bg="white", fg=TEXT_DARK).pack(anchor="w", padx=5, pady=(5, 10))

    row1 = Frame(button_frame, bg="white")
    row1.pack(fill="x", padx=5, pady=5)

    add_btn = Button(row1, text="➕ ADD", command=add_update, bg=SUCCESS_COLOR, fg="white",
                     font=('Arial', 10, 'bold'), padx=15, pady=8, bd=0, cursor="hand2", width=12)
    add_btn.pack(side=LEFT, padx=5)

    Button(row1, text="✏️ UPDATE", command=select_update, bg=WARNING_COLOR, fg="white",
           font=('Arial', 10, 'bold'), padx=15, pady=8, bd=0, cursor="hand2", width=12).pack(side=LEFT, padx=5)

    Button(row1, text="🗑️ DELETE", command=delete, bg=ACCENT_COLOR, fg="white",
           font=('Arial', 10, 'bold'), padx=15, pady=8, bd=0, cursor="hand2", width=12).pack(side=LEFT, padx=5)

    Button(row1, text="🔍 SEARCH", command=search, bg=SECONDARY_COLOR, fg="white",
           font=('Arial', 10, 'bold'), padx=15, pady=8, bd=0, cursor="hand2", width=12).pack(side=LEFT, padx=5)


    Label(button_frame, text="UTILITIES", font=('Arial', 9, 'bold'),
          bg="white", fg=TEXT_DARK).pack(anchor="w", padx=5, pady=(15, 10))

    row2 = Frame(button_frame, bg="white")
    row2.pack(fill="x", padx=5, pady=5)

    Button(row2, text="🔄 UNDO", command=undo, bg="#795548", fg="white",
           font=('Arial', 10, 'bold'), padx=15, pady=8, bd=0, cursor="hand2", width=12).pack(side=LEFT, padx=5)

    Button(row2, text="✨ CLEAR", command=clear, bg="#9C27B0", fg="white",
           font=('Arial', 10, 'bold'), padx=15, pady=8, bd=0, cursor="hand2", width=12).pack(side=LEFT, padx=5)

    Button(row2, text="❌ CANCEL", command=cancel, bg="#7f8c8d", fg="white",
           font=('Arial', 10, 'bold'), padx=15, pady=8, bd=0, cursor="hand2", width=12).pack(side=LEFT, padx=5)


    Label(button_frame, text="QUEUE MANAGEMENT", font=('Arial', 9, 'bold'),
          bg="white", fg=TEXT_DARK).pack(anchor="w", padx=5, pady=(15, 10))

    row3 = Frame(button_frame, bg="white")
    row3.pack(fill="x", padx=5, pady=5)

    Button(row3, text="📌 ADD TO Q", command=add_queue, bg="#00ACC1", fg="white",
           font=('Arial', 10, 'bold'), padx=15, pady=8, bd=0, cursor="hand2", width=12).pack(side=LEFT, padx=5)

    Button(row3, text="⚙️ PROCESS", command=process_queue, bg="#00897B", fg="white",
           font=('Arial', 10, 'bold'), padx=15, pady=8, bd=0, cursor="hand2", width=12).pack(side=LEFT, padx=5)

    Button(row3, text="📋 SHOW Q", command=show_queue, bg="#5E35B1", fg="white",
           font=('Arial', 10, 'bold'), padx=15, pady=8, bd=0, cursor="hand2", width=12).pack(side=LEFT, padx=5)


    db_card = LabelFrame(win, text=" STUDENTS DATABASE ", font=('Arial', 10, 'bold'),
                         bg="white", fg=TEXT_DARK, padx=10, pady=10)
    db_card.pack(padx=15, pady=10, fill="both", expand=True)


    listbox = Listbox(db_card, height=12, font=('Courier', 9), bg="white", fg=TEXT_DARK,
                      selectmode=SINGLE, relief=SOLID, bd=1)
    listbox.pack(fill="both", expand=True, padx=5, pady=5)


    scrollbar = Scrollbar(db_card, command=listbox.yview)
    scrollbar.pack(side=RIGHT, fill=Y, padx=(0, 5), pady=5)
    listbox.config(yscrollcommand=scrollbar.set)

    refresh()


if __name__ == "__main__":
    root = Tk()
    show_login_screen(root, lambda: show_main_app(root))
    root.mainloop()
