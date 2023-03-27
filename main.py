"""---------------------------------------- Password Generator ----------------------------------------
In this code, a simple program is written to generate and store (local) passwords for different sites.
"""

# ---------------------------------------- Add Required Library ----------------------------------------

import json
from json import JSONDecodeError
from random import choice, randint, shuffle
from tkinter import *
from tkinter import messagebox

import pyperclip


# ---------------------------------------- Password Generation ----------------------------------------


def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P',
               'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_letters = [choice(letters) for _ in range(randint(8, 10))]
    password_symbols = [choice(symbols) for _ in range(randint(2, 4))]
    password_numbers = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = password_letters + password_symbols + password_numbers
    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------------------- Save Password ----------------------------------------


def save():
    website = website_entry.get()
    email = email_entry.get()
    password = password_entry.get()
    new_data = {
        website: {
            "email": email,
            "password": password
        }
    }

    if website == "" or password == "":
        empty_fild = messagebox.showinfo(title="Oops", message="Please don't leave any fields empty!")
    else:
        try:
            with open("data.json", "r") as data_file:
                data = json.load(data_file)
        except (FileNotFoundError, JSONDecodeError):
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            data.update(new_data)
            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------------------- Search Password ----------------------------------------


def search():
    website = website_entry.get()
    try:
        with open("data.json", "r") as data_file:
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showinfo(title="Error", message="No datafile found.")
    else:
        if website in data:
            username = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title=website, message=f"Email/ Username: {username}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Error", message=f"No details for {website} exists.")


# ---------------------------------------- UI SETUP ----------------------------------------

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, background='#F7DB6A')
canvas = Canvas(height=200, width=200, bg='#F7DB6A', highlightthickness=0)
logo_img = PhotoImage(file="logo.png", height=200, width=200)
canvas.create_image(100, 100, image=logo_img)
canvas.grid(row=0, column=1, pady=10)
website_label = Label(text="Website:", bg='#F7DB6A')
website_label.grid(row=1, column=0, pady=5)
email_label = Label(text="Email/Username:", bg='#F7DB6A')
email_label.grid(row=2, column=0, pady=5)
password_label = Label(text="Password:", bg='#F7DB6A')
password_label.grid(row=3, column=0, pady=5)
website_entry = Entry(width=21)
website_entry.grid(row=1, column=1, pady=5)
website_entry.focus()
email_entry = Entry(width=37, fg='grey')
email_entry.grid(row=2, column=1, columnspan=2)
email_entry.insert(0, "Your account@gmail.com")
password_entry = Entry(width=21)
password_entry.grid(row=3, column=1, pady=5)
generate_password_button = Button(text="Generate Password", width=15, command=generate_password, bg='#E21818',
                                  fg='yellow')
generate_password_button.grid(row=3, column=2, pady=5)
add_button = Button(text="Add", width=35, command=save, bg='#E21818', fg='yellow')
add_button.grid(row=4, column=1, columnspan=2)
add_button = Button(text="Search", width=15, command=search, bg='#E21818', fg='yellow')
add_button.grid(row=1, column=2, pady=5)

window.mainloop()
