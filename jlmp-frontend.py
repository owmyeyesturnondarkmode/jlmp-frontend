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
root.resizable(False, False)
root.title("JLMP")
root.geometry("442x300")
if os.path.exists(os.path.expanduser("~/.local/share/jlmp-frontend/init")):
    with open(os.path.expanduser("~/.local/share/jlmp-frontend/config.ini"),"r") as f:
        config = f.read().splitlines()
    JLMP.homedir = os.path.expanduser(config[0])
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
        fiction = str(fiction_var.get())
        year = entry_year.get()
        isbn = entry_isbn.get()
        JLMP.book.add(title, author, genre, fiction, year, isbn)
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
            JLMP.book.remove(barcode)
            remove_book_dialog.destroy()
    submit_button = tk.Button(remove_book_dialog, text="Submit", command=submit_remove)
    submit_button.grid(column=0,row=2,padx=5,pady=5,sticky="w")
    cancel_button = tk.Button(remove_book_dialog, text="Cancel", command=remove_book_dialog.destroy)
    cancel_button.grid(column=1,row=2,padx=5,pady=5,sticky="e")

def settings():
    settings_dialog = tk.Toplevel(root)
    settings_dialog.title("Settings")
    settings_dialog.geometry("325x275")
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
    save_button.grid(column=0,row=5,padx=5,pady=5,)
    cancel_button = tk.Button(settings_dialog, text="Cancel", command=settings_dialog.destroy)
    cancel_button.grid(column=1,row=5,padx=5,pady=5)
    def jlmpinit(barcode_length, loan_period):
        data_dir = os.path.expanduser("~/.local/share/jlmp-frontend")
        if entry_barcode.get() != "" and entry_loan_period.get() != "" and entry_library_directory.get() != "":
            os.makedirs(data_dir, exist_ok=True)
            os.system(f"touch {data_dir}/init")
            os.system(f"touch {data_dir}/config.ini")
            with open(f"{data_dir}/config.ini","w") as f:
                f.write(entry_library_directory.get())
            JLMP.homedir = os.path.expanduser(entry_library_directory.get())
            JLMP.library.init(barcode_length, loan_period)
            settings_dialog.destroy()
            success = tk.Toplevel(root)
            success.title("Success")
            success.geometry("200x100")
            success_label = tk.Label(success, text="JLMP Initialized Successfully!")
            success_label.pack(padx=10,pady=10)
            ok_button = tk.Button(success, text="OK", command=success.destroy)
            ok_button.pack(padx=10,pady=10)
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

def manage_patron():
    card_number_dialog = tk.Toplevel(root)
    card_number_dialog.title("Manage Patron")
    card_number_dialog.geometry("300x100")
    label_card_number = tk.Label(card_number_dialog, text="Card Number:")
    label_card_number.grid(column=0,row=0,padx=5,pady=5)
    entry_card_number = tk.Entry(card_number_dialog)
    entry_card_number.grid(column=1,row=0,padx=5,pady=5)
    submit_button = tk.Button(card_number_dialog, text="Submit",command=lambda: submit_card_number(entry_card_number.get()))
    submit_button.grid(columnspan=2,row=1,padx=5,pady=5,sticky="w")
    cancel_button = tk.Button(card_number_dialog,text="Cancel",command=card_number_dialog.destroy)
    cancel_button.grid(columnspan=2,row=1,padx=5,pady=5,sticky="e")
    def submit_card_number(card_number):
        patron_number = card_number
        try:
            patron_info = JLMP.patron.get_info(patron_number)
        except:
            alert_dialog = tk.Toplevel(card_number_dialog)
            alert_dialog.title("Error")
            alert_dialog.geometry("200x100")
            alert_label = tk.Label(alert_dialog, text="Patron not found!")
            alert_label.pack(padx=10,pady=10)
            ok_button = tk.Button(alert_dialog, text="OK", command=alert_dialog.destroy)
            ok_button.pack(padx=10,pady=10)
            return
        card_number_dialog.destroy()
        patron_dialog = tk.Toplevel(root)
        patron_dialog.title("Manage Patron")
        patron_dialog.geometry("260x260")
        label_name = tk.Label(patron_dialog,text="Name: " + patron_info[0])
        label_name.grid(columnspan=2,row=0,padx=10,pady=5)
        label_email = tk.Label(patron_dialog,text="Email: " + patron_info[1])
        label_email.grid(columnspan=2,row=1,padx=10,pady=5)
        label_phone = tk.Label(patron_dialog,text="Phone: " + patron_info[2])
        label_phone.grid(columnspan=2,row=2,padx=10,pady=5)
        label_notes = tk.Label(patron_dialog,text="Notes: " + patron_info[3])
        label_notes.grid(columnspan=2,row=3,padx=10,pady=5)
        label_card_number = tk.Label(patron_dialog,text="Card Number: " + card_number)
        label_card_number.grid(columnspan=2,row=4,padx=10,pady=5)
        loans_button = tk.Button(patron_dialog,text="View Loans",command=lambda:veiw_loans(card_number))
        loans_button.grid(column=0,row=5,padx=10,pady=5)
        delete_button = tk.Button(patron_dialog,text="Delete Patron",fg="red",command=lambda: delete_patron(card_number))
        delete_button.grid(column=1,row=5,padx=10,pady=5)
        close_button = tk.Button(patron_dialog,text="Close",command=patron_dialog.destroy)
        close_button.grid(columnspan=2,row=6,padx=10,pady=10)
        def veiw_loans(card_number):
            loans_dialog = tk.Toplevel(patron_dialog)
            loans_dialog.title("Loans")
            loans_dialog.geometry("400x300")
            loans_canvas = tk.Canvas(loans_dialog)
            loans_scrollbar = tk.Scrollbar(loans_dialog, orient="vertical", command=loans_canvas.yview)
            loans_frame = tk.Frame(loans_canvas,relief="sunken",borderwidth=5)
            loans_canvas.create_window((0,0), window=loans_frame, anchor="nw")
            loans_canvas.configure(yscrollcommand=loans_scrollbar.set)
            loans_frame.bind("<Configure>", lambda e: loans_canvas.configure(scrollregion=loans_canvas.bbox("all")))

            def _on_mousewheel(event):
                loans_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

            def _on_mousewheel_linux(event):
                if event.num == 4:
                    loans_canvas.yview_scroll(-1, "units")
                elif event.num == 5:
                    loans_canvas.yview_scroll(1, "units")

            loans_canvas.bind("<MouseWheel>", _on_mousewheel)
            loans_canvas.bind("<Button-4>", _on_mousewheel_linux)
            loans_canvas.bind("<Button-5>", _on_mousewheel_linux)

            button_frame = tk.Frame(loans_dialog)
            close_button = tk.Button(button_frame, text="Close", command=loans_dialog.destroy)
            close_button.pack(padx=10, pady=5)
            button_frame.pack(side="bottom", fill="x")

            loans_canvas.pack(side="left", fill="both", expand=True)
            loans_scrollbar.pack(side="right", fill="y")

            barcodes = JLMP.patron.list_loans(card_number)
            for loan in barcodes:
                book_info = JLMP.book.get_info(loan[0])
                formated_info = f"{book_info[0]}: {book_info[1]} by {book_info[3]} - Due {loan[1]}, Renewed {loan[2]} times"
                label_loan = tk.Label(loans_frame, text=formated_info, justify="left", anchor="w")
                label_loan.pack(padx=10,pady=5,anchor="w")
        def delete_patron(card_number):
            confirm_dialog = tk.Toplevel(patron_dialog)
            confirm_dialog.title("Confirm Delete")
            confirm_dialog.geometry("300x100")
            label_confirm = tk.Label(confirm_dialog, text="Are you sure you want to delete this patron?")
            label_confirm.pack(padx=10,pady=10)
            ok_button = tk.Button(confirm_dialog, text="OK", command=lambda: [confirm_dialog.destroy(), JLMP.patron.remove(card_number),patron_dialog.destroy()],fg="red")
            ok_button.pack(ipadx=10,padx=10,pady=10,side="left")
            cancel_button = tk.Button(confirm_dialog, text="Cancel", command=confirm_dialog.destroy)
            cancel_button.pack(padx=10,pady=5,side="right")

def add_patron():
    add_patron_dialog = tk.Toplevel(root)
    add_patron_dialog.title("Add Patron")
    add_patron_dialog.geometry("300x300")
    label_name = tk.Label(add_patron_dialog, text="Name:")
    label_name.grid(column=0,row=0,padx=10,pady=5)
    entry_name = tk.Entry(add_patron_dialog)
    entry_name.grid(column=1,row=0,padx=10,pady=5)
    label_email = tk.Label(add_patron_dialog, text="Email:")
    label_email.grid(column=0,row=1,padx=10,pady=5)
    entry_email = tk.Entry(add_patron_dialog)
    entry_email.grid(column=1,row=1,padx=10,pady=5)
    label_phone = tk.Label(add_patron_dialog,text="Phone No.:")
    label_phone.grid(column=0,row=2,padx=10,pady=5)
    entry_phone = tk.Entry(add_patron_dialog)
    entry_phone.grid(column=1,row=2,padx=10,pady=5)
    label_notes = tk.Label(add_patron_dialog,text="Notes:")
    label_notes.grid(column=0,row=3,padx=10,pady=5,sticky="n")
    entry_notes = tk.Text(add_patron_dialog,height=5,width=20)
    entry_notes.grid(column=1,row=3,padx=10,pady=5,sticky="n")
    label_card_number = tk.Label(add_patron_dialog,text="Card Number:")
    label_card_number.grid(column=0,row=4,padx=10,pady=5)
    entry_card_number = tk.Entry(add_patron_dialog)
    entry_card_number.grid(column=1,row=4,padx=10,pady=5)
    submit_button = tk.Button(add_patron_dialog,text="Submit",command=lambda: submit_patron(entry_name.get(), entry_email.get(), entry_phone.get(), entry_notes.get("1.0","end-1c"), entry_card_number.get()))
    submit_button.grid(column=0,row=5,padx=5,pady=10,sticky="w")
    cancel_button = tk.Button(add_patron_dialog,text="Cancel",command=add_patron_dialog.destroy)
    cancel_button.grid(column=1,row=5,padx=5,pady=10,sticky="e")
    def submit_patron(name, email, phone, notes, card_number):
        JLMP.patron.add(card_number, name, email, phone, notes)
        add_patron_dialog.destroy()

def search():
    search_dialog = tk.Toplevel(root)
    search_dialog.title("Search")
    search_dialog.geometry("300x150")
    type_dropdown_label = tk.Label(search_dialog, text="Search Type:")
    type_dropdown_label.grid(column=0,row=0,padx=10,pady=5)
    search_type_var = tk.StringVar()
    type_dropdown = tk.OptionMenu(search_dialog, search_type_var, "Choose One", "Title", "Author", "Genre", "ISBN","Year")
    search_type_var.set("Choose One")
    type_dropdown.grid(column=1,row=0,padx=10,pady=5)
    label_search = tk.Label(search_dialog, text="Search Query:")
    label_search.grid(column=0,row=1,padx=10,pady=5)
    entry_search = tk.Entry(search_dialog)
    entry_search.grid(column=1,row=1,padx=10,pady=5)
    submit_button = tk.Button(search_dialog,text="Submit",command=lambda: submit_search(search_type_var.get(), entry_search.get()))
    submit_button.grid(columnspan=2,row=2,padx=10,pady=5,sticky="w")
    cancel_button = tk.Button(search_dialog,text="Cancel",command=search_dialog.destroy)
    cancel_button.grid(columnspan=2,row=2,padx=10,pady=5,sticky="e")
    def submit_search(search_type, query):
        if search_type == "Choose One":
            alert_dialog = tk.Toplevel(search_dialog)
            alert_dialog.title("Error")
            alert_dialog.geometry("200x100")
            alert_label = tk.Label(alert_dialog, text="Please select a search type!")
            alert_label.pack(padx=10,pady=10)
            ok_button = tk.Button(alert_dialog, text="OK", command=alert_dialog.destroy)
            ok_button.pack(padx=10,pady=10)
            return
        search_dialog.destroy()
        results_dialog = tk.Toplevel(root)
        results_dialog.title("Search Results")
        results_dialog.geometry("400x300")
        results = JLMP.library.search(search_type.lower(),query)
        result_canvas = tk.Canvas(results_dialog)
        result_scrollbar = tk.Scrollbar(results_dialog, orient="vertical", command=result_canvas.yview)
        result_frame = tk.Frame(result_canvas)
        result_canvas.create_window((0,0),window=result_frame,anchor="nw")
        result_canvas.configure(yscrollcommand=result_scrollbar.set)
        result_frame.bind("<Configure>", lambda e: result_canvas.configure(scrollregion=result_canvas.bbox("all")))

        def _on_mousewheel(event):
            result_canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _on_mousewheel_linux(event):
            if event.num == 4:
                result_canvas.yview_scroll(-1, "units")
            elif event.num == 5:
                result_canvas.yview_scroll(1, "units")

        result_canvas.bind("<MouseWheel>", _on_mousewheel)
        result_canvas.bind("<Button-4>", _on_mousewheel_linux)
        result_canvas.bind("<Button-5>", _on_mousewheel_linux)

        result_canvas.pack(side="left", fill="both", expand=True)
        result_scrollbar.pack(side="right", fill="y")
        for result in results:
            formatted_result = f"""{result[1]}:
    Author: {result[5]}
    Genre: {result[2]}
    Year: {result[4]}
    Barcode: {result[0]}\n""" + (f"    Fiction\n" if result[3] == 'True' else "    Non-Fiction\n")
            label_result = tk.Label(result_frame, text=formatted_result, justify="left", anchor="w")
            label_result.pack(padx=10,pady=5,anchor="w")

def checknew(barcode,card_no):
    try:
        JLMP.book.renew_loan(barcode)
        entry_barcode.delete("0",tk.END)
    except:
        JLMP.book.loan(barcode,card_no)
        entry_card_no.delete("0",tk.END)
        entry_barcode.delete("0",tk.END)

def check_in(barcode):
    JLMP.book.return_loan(barcode)
    entry_barcode.delete("0",tk.END)

root.grid_rowconfigure(2,weight=1)

book_add_button = tk.Button(root, text="Add Book", command=lambda: add_book())
book_add_button.grid(column=0,row=0,padx=10,pady=10,sticky="ew",ipadx=10)

book_remove_button = tk.Button(root, text="Remove Book", command=lambda: remove_book())
book_remove_button.grid(column=0,row=1,padx=10,pady=10,sticky="ew")

settings_button = tk.Button(root, text="Settings", command=lambda: settings())
settings_button.grid(column=2,row=0,padx=10,pady=10,sticky="ew",ipadx=7)

manage_patron_button = tk.Button(root, text="Manage Patron", command=lambda: manage_patron())
manage_patron_button.grid(column=1,row=1,padx=10,pady=10,sticky="ew")

add_patron_button = tk.Button(root, text="Add Patron", command=lambda:add_patron())
add_patron_button.grid(column=1,row=0,padx=10,pady=10,sticky="ew",ipadx=10)

search_button = tk.Button(root,text="Search",command=lambda:search())
search_button.grid(column=2,row=1,padx=10,pady=10,sticky="ew")

checknew_loan_button = tk.Button(root,text="Check Out/Renew",command=lambda:checknew(entry_barcode.get(),entry_card_no.get()))
checknew_loan_button.grid(column=2,row=3,padx=10,pady=10,sticky="sew")

check_in_button = tk.Button(root,text="Check In",command=lambda: check_in(entry_barcode.get()))
check_in_button.grid(column=2,row=4,pady=10,padx=10,sticky="ew")

label_barcode = tk.Label(root,text="Barcode:")
label_barcode.grid(column=0,row=3,pady=10,padx=10)
entry_barcode = tk.Entry(root,width=10)
entry_barcode.grid(column=1,row=3,padx=10,pady=10,sticky="ew")

label_card_no = tk.Label(root,text="Patron Card No.:")
label_card_no.grid(column=0,row=4,pady=10,padx=10)
entry_card_no = tk.Entry(root,width=10)
entry_card_no.grid(column=1,row=4,padx=10,pady=10,sticky="ew")

banner_path = os.path.join(os.path.dirname(__file__), "package", "usr", "lib", "jlmp", "banner.png")
if os.path.exists(banner_path):
    image_banner = tk.PhotoImage(file=banner_path)
    banner_label = tk.Label(root, image=image_banner)
    banner_label.image = image_banner
    banner_label.grid(column=0, row=2, columnspan=3, pady=5)
else:
    banner_label = tk.Label(root, text="Banner image not found")
    banner_label.grid(column=0, row=2, columnspan=3, padx=10, pady=5)


root.mainloop()