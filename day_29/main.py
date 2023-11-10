# a password manager using tkinter module
from tkinter import *
from tkinter import messagebox
from random import randint, choice, shuffle
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u',
               'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q',
               'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    password_list = []
    password_list = [choice(letters) for _ in range(randint(8, 10))]
    password_list += [choice(symbols) for _ in range(randint(2, 4))]
    password_list += [choice(numbers) for _ in range(randint(2, 4))]

    shuffle(password_list)

    password = "".join(password_list)
    password_entry.insert(0, password)
    # pyperclip is a module hai helps in copy past stuff
    pyperclip.copy(password)


def find_password():
    website = website_entry.get()
    try:
        with open("password_file.json") as file:
            data = json.load(file)
    except FileNotFoundError:
        messagebox.showerror(title="Error", message="file not found.")
    except Exception as e:
        messagebox.showerror(title="Error", message=f"An error occurred: {str(e)}")
    else:
        if website in data:
            email = data[website]["email"]
            password = data[website]["password"]
            messagebox.showinfo(title="Info", message=f"Website: {website}\nEmail: {email}\nPassword: {password}")
        else:
            messagebox.showinfo(title="Info", message=f"No details of the {website} website found")

# ---------------------------- SAVE PASSWORD ------------------------------- #
def add_entry():
    email = email_entry.get()
    website = website_entry.get()
    password = password_entry.get()
    new_data = {
        website:
            {
                "email": email,
                "password": password,
            }
    }

    if len(email) == 0 or len(website) == 0 or len(password) == 0:
        messagebox.showwarning(title="Warning", message="Hey you cannot left the box empty")
    else:
        is_ok = messagebox.askokcancel(title=website,
                                       message=f"The details that you have entered: \nEmail: {email}"
                                               f" \nPassword: {password} \nis it ok to save??")
        if is_ok:
            try:
                with open("password_file.json", "r") as file:
                    # reading the old data
                    data = json.load(file)
            except FileNotFoundError:
                with open("password_file.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                # updating the old data with new data
                data.update(new_data)
                with open("password_file.json", "w") as file:
                    # saving the updated data
                    json.dump(data, file, indent=4)
            finally:
                # Clear the entry fields
                website_entry.delete(0, END)
                password_entry.delete(0, END)


# ---------------------------- UI SETUP ------------------------------- #
# creating the window
window = Tk()
window.title("Password Manager")
window.config(padx=20, pady=20)

# creating the canvas
canvas = Canvas(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# All labels
website_lable = Label(text="Website:")
website_lable.grid(column=0, row=1)
email_lable = Label(text="Email/Username:")
email_lable.grid(column=0, row=2)
password_lable = Label(text="Password:")
password_lable.grid(column=0, row=3)

# Entries
website_entry = Entry(width=33)
website_entry.grid(column=1, row=1)
website_entry.focus()
email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(END, "rohitprasad20022@gmail.com")
password_entry = Entry(width=33)
password_entry.grid(column=1, row=3)

# Button
generator_button = Button(text="Generate Password", command=generate_password)
generator_button.grid(column=2, row=3)
add_button = Button(text="Add", width=44, command=add_entry)
add_button.grid(column=1, row=4, columnspan=2)
search_button = Button(text="Search", width=15, command=find_password)
search_button.grid(column=2, row=1)

window.mainloop()
