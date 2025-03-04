import sqlite3
from tkinter import *
from tkinter import messagebox
import subprocess  # To open home.py after successful login

# Create SQLite Database
conn = sqlite3.connect('users.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS users (
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )''')
conn.commit()

# Function for Signup
def signup():
    def register_user():
        username = entry_user_signup.get()
        password = entry_pass_signup.get()

        if username == "" or password == "":
            messagebox.showerror("Error", "All fields are required")
            return

        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Success", "Registration Successful")
            signup_window.destroy()
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

    # Signup Window
    signup_window = Toplevel(root)
    signup_window.title("Signup Page")
    signup_window.geometry("1270x800")
    signup_window.configure(bg="#1f4e79")  # A more attractive background color

    # Signup Form
    Label(signup_window, text="Create Account", font=("Helvetica", 30, "bold"), bg="#1f4e79", fg="white").pack(pady=40)

    Label(signup_window, text="Username:", bg="#1f4e79", fg="white", font=("Helvetica", 16)).pack(pady=10)
    entry_user_signup = Entry(signup_window, width=30, font=("Helvetica", 14), bd=2, relief=SOLID)
    entry_user_signup.pack(pady=10)

    Label(signup_window, text="Password:", bg="#1f4e79", fg="white", font=("Helvetica", 16)).pack(pady=10)
    entry_pass_signup = Entry(signup_window, show="*", width=30, font=("Helvetica", 14), bd=2, relief=SOLID)
    entry_pass_signup.pack(pady=10)

    Button(signup_window, text="Register", width=20, font=("Helvetica", 14), bg="#28a745", fg="white", command=register_user, bd=0, activebackground="#218838", activeforeground="white").pack(pady=20)

# Function for Login
def login():
    username = entry_user_login.get()
    password = entry_pass_login.get()

    if username == "" or password == "":
        messagebox.showerror("Error", "All fields are required")
        return

    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    result = c.fetchone()

    if result:
        messagebox.showinfo("Success", f"Welcome {username}")
        root.destroy()  # Close the login window
        subprocess.Popen(["python", "FinalProject.py"])  
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

# Main Tkinter Window (Login Page)
root = Tk()
root.title("Login Page")
root.resizable(False,False)
root.geometry("1270x800")
root.configure(bg="#1f4e79")  # A more attractive background color

# Login Form
Label(root, text="Login", font=("Helvetica", 30, "bold"), bg="#1f4e79", fg="white").pack(pady=40)

Label(root, text="Username:", bg="#1f4e79", fg="white", font=("Helvetica", 16)).pack(pady=10)
entry_user_login = Entry(root, width=30, font=("Helvetica", 14), bd=2, relief=SOLID)
entry_user_login.pack(pady=10)

Label(root, text="Password:", bg="#1f4e79", fg="white", font=("Helvetica", 16)).pack(pady=10)
entry_pass_login = Entry(root, show="*", width=30, font=("Helvetica", 14), bd=2, relief=SOLID)
entry_pass_login.pack(pady=10)

Button(root, text="Login", width=20, font=("Helvetica", 14), bg="#007bff", fg="white", command=login, bd=0, activebackground="#0056b3", activeforeground="white").pack(pady=20)

Label(root, text="Don't have an account?", bg="#1f4e79", fg="white", font=("Helvetica", 12)).pack(pady=10)
Button(root, text="Signup", width=20, font=("Helvetica", 14), bg="#ffc107", fg="black", command=signup, bd=0, activebackground="#e0a800", activeforeground="black").pack(pady=10)

root.mainloop()
