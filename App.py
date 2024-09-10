import customtkinter
from tkinter import *
from tkinter import ttk
import tkinter as tk
from tkinter import messagebox
import database
import pandas as pd 
root = customtkinter.CTk()
root.title('Employee Management System')
root.geometry('900x450')
root.config(bg='#1e272e')
root.resizable(False, False)

font1 = ('Arial', 20, 'bold')
font2 = ('Arial', 12, 'bold')


def add_to_treeview():
    employees = database.fetch_employees()
    tree.delete(*tree.get_children())
    for employee in employees:
        tree.insert('', END, values=employee)


def insert():
    id = id_entry.get()
    name = name_entry.get()
    role = role_entry.get()
    gender = variable1.get()
    status = status_entry.get()
    if not (id and name and role and gender and status):
        messagebox.showerror('Error', 'Enter all fields.')
    elif database.id_exists(id):
        messagebox.showerror('Error', 'ID already exists.')
    else:
        database.insert_employee(id, name, role, gender, status)
        add_to_treeview()
        messagebox.showinfo('Success', 'Data has been inserted.')


def clear(*clicked):
    if clicked:
        tree.selection_remove(tree.focus())
    id_entry.delete(0, END)
    name_entry.delete(0, END)
    role_entry.delete(0, END)
    variable1.set('')
    status_entry.delete(0, END)


def display_data(event):
    selected_item = tree.focus()
    if selected_item:
        row = tree.item(selected_item)['values']
        clear()
        id_entry.insert(0, row[0])
        name_entry.insert(0, row[1])
        role_entry.insert(0, row[2])
        variable1.set(row[3])
        status_entry.insert(0, row[4])
    else:
        pass


def delete():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose an employee to delete.')
    else:
        id = id_entry.get()
        database.delete_employee(id)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success', 'Data has been deleted.')


def update():
    selected_item = tree.focus()
    if not selected_item:
        messagebox.showerror('Error', 'Choose an employee to update.')
    else:
        id = id_entry.get()
        new_name = name_entry.get()
        new_role = role_entry.get()
        new_gender = variable1.get()
        new_status = status_entry.get()
        database.update_employee(new_name, new_role, new_gender, new_status, id)
        add_to_treeview()
        clear()
        messagebox.showinfo('Success', 'Data has been updated.')


def save_to_excel():

    rows = []
    for item in tree.get_children():
        rows.append(tree.item(item)['values'])


    df = pd.DataFrame(rows, columns=['ID', 'Name', 'Role', 'Gender', 'Status'])


    df.to_excel('employee_data.xlsx', index=False)
    messagebox.showinfo('Success', 'Data has been saved to Excel.')


id_label = customtkinter.CTkLabel(root, font=font1, text='ID:', text_color='#fff', bg_color='#1e272e')
id_label.place(x=20, y=20)

id_entry = customtkinter.CTkEntry(root, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                border_width=2, width=180)
id_entry.place(x=100, y=20)

name_label = customtkinter.CTkLabel(root, font=font1, text='Name:', text_color='#fff', bg_color='#1e272e')
name_label.place(x=20, y=80)

name_entry = customtkinter.CTkEntry(root, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                    border_width=2, width=180)
name_entry.place(x=100, y=80)

role_label = customtkinter.CTkLabel(root, font=font1, text='Role:', text_color='#fff', bg_color='#1e272e')
role_label.place(x=20, y=140)

role_entry = customtkinter.CTkEntry(root, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                    border_width=2, width=180)
role_entry.place(x=100, y=140)

gender_label = customtkinter.CTkLabel(root, font=font1, text='Gender:', text_color='#fff', bg_color='#1e272e')
gender_label.place(x=20, y=200)

options = ['Male', 'Female']
variable1 = StringVar()

gender_options = customtkinter.CTkComboBox(root, font=font1, text_color='#000', fg_color='#fff',
                                        dropdown_hover_color="#0C9295", border_color='#0C9295', width=180,
                                        variable=variable1, values=options, state="readonly")
gender_options.place(x=100, y=200)

status_label = customtkinter.CTkLabel(root, font=font1, text='Status:', text_color='#fff', bg_color='#1e272e')
status_label.place(x=20, y=260)

status_entry = customtkinter.CTkEntry(root, font=font1, text_color='#000', fg_color='#fff', border_color='#0C9295',
                                    border_width=2, width=180)
status_entry.place(x=100, y=260)

add_button = customtkinter.CTkButton(root, font=font1, text_color='#fff', command=insert, text='Add Employee',
                                    fg_color='#0077CC', hover_color='#005BB5', bg_color='#1e272e', cursor='hand2',
                                    corner_radius=15, width=260)
add_button.place(x=20, y=310)

clear_button = customtkinter.CTkButton(root, command=lambda: clear(True), font=font1, text_color='#fff', text='New Employee',
                                    fg_color='#1e272e', hover_color='#FF5002', bg_color='#1e272e', border_color='#F15704',
                                    border_width=2, cursor='hand2', corner_radius=15, width=260)
clear_button.place(x=20, y=360)

update_button = customtkinter.CTkButton(root, command=update, font=font1, text_color='#fff', text='Update Employee',
                                        fg_color='#1e272e', hover_color='#FF5002', bg_color='#1e272e', border_color='#F15704',
                                        border_width=2, cursor='hand2', corner_radius=15, width=260)
update_button.place(x=300, y=360)

delete_button = customtkinter.CTkButton(root, command=delete, font=font1, text_color='#fff', text='Delete Employee',
                                        fg_color='#E40404', hover_color='#AE0000', bg_color='#1e272e', border_color='#E40404',
                                        border_width=2, cursor='hand2', corner_radius=15, width=260)
delete_button.place(x=580, y=360)


save_button = customtkinter.CTkButton(root, command=save_to_excel, font=font1, text_color='#fff', text='Save to Excel',
                                        fg_color='#05A312', hover_color='#00850B', bg_color='#1e272e', border_color='#05A312',
                                        border_width=2, cursor='hand2', corner_radius=15, width=260)
save_button.place(x=20, y=410)

style = ttk.Style(root)

style.theme_use('clam')

style.configure('Treeview', font=font2, foreground='#fff', background='#000', fieldbackground='#313837')
style.map('Treeview', background=[('selected', '#1A8F2d')])

tree = ttk.Treeview(root, height=15)

tree['columns'] = ('ID', 'Name', 'Role', 'Gender', 'Status')

tree.column('#0', width=0, stretch=tk.NO)
tree.column('ID', anchor=tk.CENTER, width=120)
tree.column('Name', anchor=tk.CENTER, width=120)
tree.column('Role', anchor=tk.CENTER, width=120)
tree.column('Gender', anchor=tk.CENTER, width=100)
tree.column('Status', anchor=tk.CENTER, width=120)

tree.heading('ID', text='ID', anchor=tk.CENTER)
tree.heading('Name', text='Name', anchor=tk.CENTER)
tree.heading('Role', text='Role', anchor=tk.CENTER)
tree.heading('Gender', text='Gender', anchor=tk.CENTER)
tree.heading('Status', text='Status', anchor=tk.CENTER)

tree.place(x=300, y=20)

add_to_treeview()

tree.bind('<ButtonRelease>', display_data)

root.mainloop()
