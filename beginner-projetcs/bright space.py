from tkinter import *
from tkinter import messagebox


class Node:
    def __init__(self, student_data):
        self.data = student_data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.size = 0

    def add(self, student):
        new = Node(student)
        if not self.head:
            self.head = new
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = new
        self.size += 1

    def get_all(self):
        students = []
        curr = self.head
        while curr:
            students.append(curr.data)
            curr = curr.next
        return students

    def get(self, student_id):
        curr = self.head
        while curr:
            if curr.data['id'] == student_id:
                return curr.data
            curr = curr.next
        return None

    def update(self, student_id, new_data):
        curr = self.head
        while curr:
            if curr.data['id'] == student_id:
                curr.data = new_data
                return True
            curr = curr.next
        return False

    def delete(self, student_id):
        if not self.head:
            return False
        if self.head.data['id'] == student_id:
            self.head = self.head.next
            self.size -= 1
            return True
        curr = self.head
        while curr.next:
            if curr.next.data['id'] == student_id:
                curr.next = curr.next.next
                self.size -= 1
                return True
            curr = curr.next
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

db, stack, queue = LinkedList(), Stack(), Queue()
updating = None


def refresh():
    listbox.delete(0, END)
    for student in db.get_all():
        listbox.insert(END, f"{student['id']} | {student['name']} | {student['program']} | Year {student['year']}")


def add_update():
    global updating
    student_id, name, program, year = id_e.get(), name_e.get(), prog_e.get(), year_e.get()
    if not (student_id and name and program and year):
        messagebox.showerror("Error", "All fields required!")
        return

    student = {"id": student_id, "name": name, "program": program, "year": year}

    if updating:
        old_student = db.get(updating)
        stack.push({'type': 'UPDATE', 'old': old_student, 'id': updating})
        db.update(updating, student)
        messagebox.showinfo("Success", "Updated!")
        updating = None
        add_btn.config(text="ADD", bg="#4CAF50")
    else:
        if db.get(student_id):
            messagebox.showerror("Error", "ID exists!")
            return
        stack.push({'type': 'ADD', 'student': student})
        db.add(student)
        messagebox.showinfo("Success", "Added!")

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
        messagebox.showinfo("Found", "Student found!")
    else:
        messagebox.showerror("Error", "Not found!")


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
        add_btn.config(text="UPDATE", bg="#FF9800")
    except:
        messagebox.showerror("Error", "Select a student!")


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
            messagebox.showinfo("Success", "Deleted!")
    except:
        messagebox.showerror("Error", "Select a student!")


def undo():
    if stack.is_empty():
        messagebox.showinfo("Undo", "Nothing to undo!")
        return
    operation = stack.pop()
    if operation['type'] == 'ADD':
        db.delete(operation['student']['id'])
    elif operation['type'] == 'DELETE':
        db.add(operation['student'])
    elif operation['type'] == 'UPDATE':
        db.update(operation['id'], operation['old'])
    refresh()
    messagebox.showinfo("Undo", "Undone!")


def add_queue():
    try:
        selected_index = listbox.curselection()[0]
        student = db.get_all()[selected_index]
        queue.enqueue(student['id'])
        messagebox.showinfo("Queue", f"{student['name']} added to queue!")
    except:
        messagebox.showerror("Error", "Select a student!")


def process_queue():
    if queue.is_empty():
        messagebox.showinfo("Queue", "Queue empty!")
        return
    student_id = queue.dequeue()
    student = db.get(student_id)
    if student:
        messagebox.showinfo("Processing", f"Processing: {student['name']}")
    else:
        messagebox.showwarning("Warning", "Student not found!")


def show_queue():
    if queue.is_empty():
        messagebox.showinfo("Queue", "Queue empty!")
        return
    message_text = "Registration Queue:\n"
    for position, student_id in enumerate(queue.items, 1):
        student = db.get(student_id)
        if student:
            message_text += f"{position}. {student['name']} ({student_id})\n"
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
    add_btn.config(text="ADD", bg="#4CAF50")

win = Tk()
win.title("Student Record System")
win.geometry("650x500")

Label(win, text='STUDENT RECORD SYSTEM', font=('Arial', 14, 'bold')).pack(pady=5)

f = Frame(win, padx=10, pady=5)
f.pack()
Label(f, text='ID:').grid(row=0, column=0)
id_e = Entry(f)
id_e.grid(row=0, column=1)
Label(f, text='Name:').grid(row=1, column=0)
name_e = Entry(f)
name_e.grid(row=1, column=1)
Label(f, text='Program:').grid(row=2, column=0)
prog_e = Entry(f)
prog_e.grid(row=2, column=1)
Label(f, text='Year:').grid(row=3, column=0)
year_e = Entry(f)
year_e.grid(row=3, column=1)

bf = Frame(win)
bf.pack(pady=5)
add_btn = Button(bf, text="ADD", command=add_update, bg="#4CAF50", fg="white", width=10)
add_btn.grid(row=0, column=0)
Button(bf, text="UPDATE", command=select_update, bg="#FF9800", fg="white", width=10).grid(row=0, column=1)
Button(bf, text="DELETE", command=delete, bg="#f44336", fg="white", width=10).grid(row=0, column=2)
Button(bf, text="SEARCH", command=search, bg="#2196F3", fg="white", width=10).grid(row=0, column=3)
Button(bf, text="CLEAR", command=clear, bg="#9C27B0", fg="white", width=10).grid(row=0, column=4)
Button(bf, text="UNDO", command=undo, bg="#795548", fg="white", width=12).grid(row=2, column=0, columnspan=2)
Button(bf, text="ADD TO Q", command=add_queue, bg="#00ACC1", fg="white", width=8).grid(row=2, column=2)
Button(bf, text="PROCESS", command=process_queue, bg="#00897B", fg="white", width=8).grid(row=2, column=3)
Button(bf, text="SHOW Q", command=show_queue, bg="#5E35B1", fg="white", width=8).grid(row=2, column=4)
Button(bf, text="CANCEL", command=cancel, bg="#757575", fg="white", width=52).grid(row=3, column=0, columnspan=5,
                                                                                   pady=5)
lf = LabelFrame(win, text=" STUDENTS DATABASE ")
lf.pack(pady=5, fill="both", expand=True)
listbox = Listbox(lf, height=8)
listbox.pack(fill="both", expand=True, padx=5, pady=5)
refresh()
win.mainloop()







