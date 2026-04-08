#!/usr/bin/env python3
'''
JLMP-frontend - A frontend for JLMP (J's Library Management Program) using tkinter.
Copyright (C) 2026 owmyeyesturnondarkmode <https://github.com/owmyeyesturnondarkmode>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>
'''

import tkinter as tk
import JLMP
import os
from xml.etree import ElementTree as ET

root = tk.Tk()
root.title("JLMP")
root.geometry("400x300")
if os.path.exists(os.path.expanduser("~/.local/share/jlmp-frontend/init")):
    with open(os.path.expanduser("~/.local/share/jlmp-frontend/config.ini"),"r") as f:
        config = f.read().splitlines()
    JLMP.homedir = config[0]
else:
    config = []

def add_book():
    add_book_dialog = tk.Toplevel(root)
    add_book_dialog.title("Add Book")
    add_book_dialog.geometry("300x300")
    label_title = tk.Label(add_book_dialog, text="Title:")
    label_title.grid(column=0,row=0,padx=10,pady=5)
    entry_title = tk.Entry(add_book_dialog)
    entry_title.grid(column=1,row=0,padx=10,pady=5)
    author_title = tk.Label(add_book_dialog, text="Author:")
    author_title.grid(column=0,row=1,padx=10,pady=5)
    entry_author = tk.Entry(add_book_dialog)
    entry_author.grid(column=1,row=1,padx=10,pady=5)
    genre_title = tk.Label(add_book_dialog, text="Genre:")
    genre_title.grid(column=0,row=2,padx=10,pady=5)
    entry_genre = tk.Entry(add_book_dialog)
    entry_genre.grid(column=1,row=2,padx=10,pady=5)
    fiction_var = tk.BooleanVar()
    fiction_checkbox = tk.Checkbutton(add_book_dialog, text="Fiction", variable=fiction_var)
    fiction_checkbox.grid(column=0,row=5,padx=10,pady=5)
    year_title = tk.Label(add_book_dialog, text="Year:")
    year_title.grid(column=0,row=4,padx=10,pady=5)
    entry_year = tk.Entry(add_book_dialog)
    entry_year.grid(column=1,row=4,padx=10,pady=5)
    isbn_title = tk.Label(add_book_dialog, text="ISBN:")
    isbn_title.grid(column=0,row=3,padx=10,pady=5)
    entry_isbn = tk.Entry(add_book_dialog)
    entry_isbn.grid(column=1,row=3,padx=10,pady=5)
    def submit_book():
        title = entry_title.get()
        author = entry_author.get()
        genre = entry_genre.get()
        fiction = fiction_var.get()
        year = entry_year.get()
        isbn = entry_isbn.get()
        JLMP.add_book(title, author, genre, fiction, year, isbn)
        add_book_dialog.destroy()
    submit_button = tk.Button(add_book_dialog, text="Submit", command=submit_book)
    submit_button.grid(column=0,row=6,padx=5,pady=10)
    cancel_button = tk.Button(add_book_dialog, text="Cancel", command=add_book_dialog.destroy)
    cancel_button.grid(column=1,row=6,padx=5,pady=10,sticky="e")

def remove_book():
    remove_book_dialog = tk.Toplevel(root)
    remove_book_dialog.title("Remove Book")
    remove_book_dialog.geometry("300x125")
    label_barcode = tk.Label(remove_book_dialog, text="Barcode:")
    label_barcode.grid(column=0,row=0,padx=5,pady=5)
    entry_barcode = tk.Entry(remove_book_dialog)
    entry_barcode.grid(column=1,row=0,padx=5,pady=5)
    areyousure_var = tk.BooleanVar()
    areyousure_checkbox = tk.Checkbutton(remove_book_dialog, text="Are you sure?", variable=areyousure_var)
    areyousure_checkbox.grid(column=0,row=1,padx=5,pady=5)
    def submit_remove():
        barcode = entry_barcode.get()
        if areyousure_var.get():
            JLMP.remove_book(barcode)
            remove_book_dialog.destroy()
    submit_button = tk.Button(remove_book_dialog, text="Submit", command=submit_remove)
    submit_button.grid(column=0,row=2,padx=5,pady=5,sticky="w")
    cancel_button = tk.Button(remove_book_dialog, text="Cancel", command=remove_book_dialog.destroy)
    cancel_button.grid(column=1,row=2,padx=5,pady=5,sticky="e")

def settings():
    settings_dialog = tk.Toplevel(root)
    settings_dialog.title("Settings")
    settings_dialog.geometry("325x300")
    label_library_directory = tk.Label(settings_dialog,text="Library Directory:")
    label_library_directory.grid(column=0,row=0,padx=5,pady=5)
    entry_library_directory = tk.Entry(settings_dialog,state="normal" if not os.path.exists(os.path.expanduser("~/.local/share/jlmp-frontend/init")) else "disabled")
    entry_library_directory.grid(column=1,row=0,padx=5,pady=5)
    label_barcode = tk.Label(settings_dialog, text="Barcode Length:")
    barcode_note = tk.Label(settings_dialog, text="         Barcode length and directory can ONLY be set before init",fg="red",font=("Arial",8))
    label_barcode.grid(column=0,row=1,padx=5,pady=5,sticky="w")
    entry_barcode = tk.Entry(settings_dialog,state="normal" if not os.path.exists(os.path.expanduser("~/.local/share/jlmp-frontend/init")) else "disabled")
    entry_barcode.grid(column=1,row=1,padx=5,pady=5)
    barcode_note.grid(column=0,row=2,padx=5,pady=5,columnspan=2,sticky="w")
    label_loan_period = tk.Label(settings_dialog, text="Loan Period (days):")
    label_loan_period.grid(column=0,row=3,padx=5,pady=5)
    entry_loan_period = tk.Entry(settings_dialog)
    entry_loan_period.grid(column=1,row=3,padx=5,pady=5)
    init_button = tk.Button(settings_dialog, text="Init", command=lambda: jlmpinit(entry_barcode.get(), entry_loan_period.get()),state="normal" if not os.path.exists(os.path.expanduser("~/.local/share/jlmp-frontend/init")) else "disabled")
    init_button.grid(column=0,row=4,padx=5,pady=10,sticky="w")
    save_button = tk.Button(settings_dialog, text="Save", command=lambda: savesettings(entry_loan_period.get()))
    save_button.grid(column=0,row=5,padx=5,pady=5,ipady=10)
    cancel_button = tk.Button(settings_dialog, text="Cancel", command=settings_dialog.destroy)
    cancel_button.grid(column=1,row=5,padx=5,pady=5,ipady=10)
    def jlmpinit(barcode_length, loan_period):
        data_dir = os.path.expanduser("~/.local/share/jlmp-frontend")
        if entry_barcode.get() != "" and entry_loan_period.get() != "" and entry_library_directory.get() != "":
            os.makedirs(data_dir, exist_ok=True)
            os.system(f"touch {data_dir}/init")
            os.system(f"touch {data_dir}/config.ini")
            with open(f"{data_dir}/config.ini","w") as f:
                f.write(entry_library_directory.get())
            JLMP.homedir = os.path.expanduser(entry_library_directory.get())
            if not os.path.exists(f"{JLMP.homedir}"):
                os.makedirs(f"{JLMP.homedir}")
            JLMP.Library.init(barcode_length, loan_period)
            settings_dialog.destroy()
        else:
            alert_dialog = tk.Toplevel(settings_dialog)
            alert_dialog.title("Error")
            alert_dialog.geometry("200x100")
            alert_label = tk.Label(alert_dialog, text="All fields must be filled out!")
            alert_label.pack(padx=10,pady=10)
            ok_button = tk.Button(alert_dialog, text="OK", command=alert_dialog.destroy)
            ok_button.pack(padx=10,pady=10)
    def savesettings(loan_period):
        if entry_loan_period.get() != "":
            with open(f"{JLMP.homedir}settings.xml", "r") as f:
                    settings_tree = ET.parse(f)
                    settings_root = settings_tree.getroot()
            settings_root.find("loan_period").text = loan_period
            settings_tree.write(f"{JLMP.homedir}settings.xml")
            settings_dialog.destroy()
        else:
            alert_dialog = tk.Toplevel(settings_dialog)
            alert_dialog.title("Error")
            alert_dialog.geometry("200x100")
            alert_label = tk.Label(alert_dialog, text="Loan period must be filled out!")
            alert_label.pack(padx=10,pady=10)
            ok_button = tk.Button(alert_dialog, text="OK", command=alert_dialog.destroy)
            ok_button.pack(padx=10,pady=10)

book_add_button = tk.Button(root, text="Add Book", command=lambda: add_book())
book_add_button.grid(column=0,row=0,padx=10,pady=10,sticky="w")

book_remove_button = tk.Button(root, text="Remove Book", command=lambda: remove_book())
book_remove_button.grid(column=0,row=1,padx=10,pady=10,sticky="w")

settings_button = tk.Button(root, text="Settings", command=lambda: settings())
settings_button.grid(column=2,row=0,padx=10,pady=10,sticky="e")

manage_patron_button = tk.Button(root, text="Manage Patron", command=lambda: print("Manage Patron"))
manage_patron_button.grid(column=1,row=1,padx=10,pady=10)

add_patron_button = tk.Button(root, text="Add Patron", command=lambda: print("Add Patron"))
add_patron_button.grid(column=1,row=0,padx=10,pady=10)

root.mainloop()