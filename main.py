
import customtkinter
from tkinter import *
from PIL import Image, ImageTk
import sqlite3

customtkinter.set_appearance_mode('dark')
customtkinter.set_default_color_theme('dark-blue')

def add(task, window_to_close, loaded_id=None):
    if not task.strip(): window_to_close.destroy(); return

    conn = sqlite3.connect('tasks.db'); cursor = conn.cursor()
    if loaded_id is None:
        cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)");
        cursor.execute("INSERT INTO tasks (task) VALUES (?)", (task,));
        task_id = cursor.lastrowid
    else: task_id = loaded_id
    conn.commit(); conn.close()

    f = customtkinter.CTkFrame(root)
    f.task_id = task_id

    customtkinter.CTkLabel(f, text=task, wraplength=400, justify=LEFT).pack(anchor=NW, side=LEFT, padx=5, pady=5)

    customtkinter.CTkButton(f, image=img_del_task, text='', width=30, command=lambda frame=f: delete_task(frame)).pack(anchor=NE,side=RIGHT,padx=10,pady=5)
    f.pack(fill='x', padx=5, pady=5)

    if window_to_close: window_to_close.destroy()

def delete_task(frame):
    conn = sqlite3.connect('tasks.db'); cursor = conn.cursor()
    cursor.execute("DELETE FROM tasks WHERE id = ?", (frame.task_id,));
    conn.commit(); conn.close()
    frame.pack_forget()

def add_task():
    window = customtkinter.CTkToplevel(root)
    window.title("Додати задачу")
    window.geometry("300x120")
    window.transient(root)
    window.grab_set()
    window.wm_attributes('-topmost', True)
    task_text = customtkinter.CTkEntry(window, width=250)
    task_text.pack(pady=5)

    customtkinter.CTkButton(window, text='Додати', font=('arial', 13, 'bold'),command=lambda: add(task_text.get(), window)).pack(pady=5)
    task_text.bind("<Return>", lambda event=None: add(task_text.get(), window))

root = customtkinter.CTk()
root.title('ToDoList')
root.geometry('700x500')


img_del_task = ImageTk.PhotoImage(Image.open('del_task.png.png').resize((20, 20)))

btn_add_task = customtkinter.CTkButton(root, text='Додати задачу', font=('arial', 13, 'bold'), command=add_task)
btn_add_task.pack(anchor='center', side=BOTTOM, pady=5)

conn = sqlite3.connect('tasks.db'); cursor = conn.cursor()
cursor.execute("CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY AUTOINCREMENT, task TEXT)");
for task_id, task_text in cursor.execute("SELECT id, task FROM tasks").fetchall():
    add(task_text, None, task_id)
conn.close()

root.mainloop()
