from tkinter import *
from tkinter import messagebox
from random import *
import pyperclip
import json


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def password_gen():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
               'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R',
               'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    letter_list = [choice(letters) for _ in range(randint(8, 10))]
    symbol_list = [choice(symbols) for _ in range(randint(2, 4))]
    number_list = [choice(numbers) for _ in range(randint(2, 4))]

    password_list = letter_list + symbol_list + number_list
    shuffle(password_list)

    password_rand = "".join(password_list)

    password_entry.insert(0, password_rand)

    pyperclip.copy(password_rand)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = str(website_entry.get()).title()
    email = str(email_entry.get())
    password = str(password_entry.get())
    new_data = {
        website: {
            "email": email,
            "password": password,
        }
    }

    if len(website) == 0 or len(email) == 0 or len(password) == 0:
        messagebox.showinfo(title="Oops", message="Please don't leave any fields empty")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            with open("data.json", "w") as data_file:
                json.dump(new_data, data_file, indent=4)
        else:
            # Updating old data with new data
            data.update(new_data)

            with open("data.json", "w") as data_file:
                json.dump(data, data_file, indent=4)
        finally:
            website_entry.delete(0, END)
            password_entry.delete(0, END)


# ---------------------------- DELETE FUNCTION ------------------------------- #
def delete():
    website = str(website_entry.get()).title()
    if len(website) == 0:
        messagebox.showinfo(title="Oops", message="CompleteThe Website Entry To Delete It.")
    else:
        try:
            with open("data.json", "r") as data_file:
                # Reading old data
                data = json.load(data_file)
        except FileNotFoundError:
            messagebox.showerror(title="Not Found", message="No Data File Found")
        else:
            data.pop(website)

            if website in data:
                with open("data.json", "w") as data_file:
                    json.dump(data, data_file, indent=4)

                website_entry.delete(0, END)
            else:
                messagebox.showerror(title="Not Found", message="Website Not Found")


# ---------------------------- FIND PASSWORD ------------------------------- #
def find_password():
    website = str(website_entry.get()).title()
    try:
        with open("data.json", "r") as data_file:
            # Reading old data
            data = json.load(data_file)
    except FileNotFoundError:
        messagebox.showerror(title="Not Found", message="No Data File Found")
    else:
        if website in data:
            messagebox.showinfo(title=website, message=f"Email: {data[website]['email']} \n"
                                                       f"Password: {data[website]['password']}")
        else:
            messagebox.showerror(title="Not Found", message="No details for the website exists")


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas(width=200, height=200)
logo_img = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo_img)
canvas.grid(column=1, row=0)

# WEBSITE ROW
website_label = Label(text="Website:")
website_label.grid(column=0, row=1)

website_entry = Entry(width=34)
website_entry.grid(column=1, row=1)

search_button = Button(text="Search", command=find_password, width=14)
search_button.grid(column=2, row=1)

# EMAIL ROW
email_label = Label(text="Email/Username:")
email_label.grid(column=0, row=2)

email_entry = Entry(width=52)
email_entry.grid(column=1, row=2, columnspan=2)
email_entry.insert(0, "youremail@gmail.com")

# PASSWORD ROW
password_label = Label(text="Password:")
password_label.grid(column=0, row=3)

password_entry = Entry(width=34)
password_entry.grid(column=1, row=3)

password_button = Button(text="Generate password", command=password_gen)
password_button.grid(column=2, row=3)

# ADD BUTTON ROW
add_button = Button(text="Add", width=44, command=save_password)
add_button.grid(column=1, row=4, columnspan=2)

# DELETE BUTTON
delete_button = Button(text="Delete existing site", width=44, command=delete)
delete_button.grid(column=1, row=5, columnspan=2)

window.mainloop()