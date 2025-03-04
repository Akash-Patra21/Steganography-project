from tkinter import *
from tkinter import filedialog
import tkinter as tk
from PIL import Image, ImageTk
import os
from stegano import lsb
import smtplib  # For sending email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

root = Tk()
root.title("Steganography - Hide a secret text message in an image")
root.geometry("1270x800")
root.resizable(False, False)
root.configure(bg="#2f4155")

# Simulate email sending function   
def send_email(to_email, message_body, image_path):
    try:
        # Create the email
        msg = MIMEMultipart()
        msg['From'] = "abhai8350@gmail.com"  # Replace with your email
        msg['To'] = to_email
        msg['Subject'] = "Steganography - Data Hidden Successfully"

        # Attach the message body
        msg.attach(MIMEText(message_body, 'plain'))

        with open(image_path, "rb") as attachment:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(attachment.read())

        # Encode the attachment in base64 and add the necessary headers
        encoders.encode_base64(part)
        part.add_header(
            "Content-Disposition",
            f"attachment; filename= {os.path.basename(image_path)}",
        )

        # Attach the image to the email
        msg.attach(part)

        # Simulate sending email via console output
        print(f"Email sent to {to_email}:\n{message_body}")
        
        # Uncomment below to actually send the email using smtplib
        
        # Setup your email server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()

        # Log into the email account
        server.login("abhai8350@gmail.com", "spyz dzvj ubcc tbrp")  # Replace with your credentials
        
        # Send email
        server.send_message(msg)
        server.quit()
        print(f"Email sent to {to_email} with the image attached.")
        
        return True
    except Exception as e:
        print(f"Failed to send email: {str(e)}")
        return False

def showimage():
    global filename
    filename = filedialog.askopenfilename(initialdir=os.getcwd(),
                                          title='Select Image File',
                                          filetype=(("JPG File", "*.jpg"), ("PNG file", "*.png")))
    # Check if a file was selected
    if filename:
        print(f"Selected file: {filename}")

        # Get the directory of the selected file
        file_directory = os.path.dirname(filename)
        print(f"File directory: {file_directory}")

        # Get the base name (file name with extension)
        file_name = os.path.basename(filename)
        print(f"File name: {file_name}")

        # You can use the file path for further operations
        # Example: Checking if the file exists
        if os.path.exists(filename):
            print("File exists and is ready for further processing.")
        else:
            print("File does not exist.")
    else:
        print("No file selected.")

    img = Image.open(filename)
    img = ImageTk.PhotoImage(img)
    lbl.configure(image=img, width=250, height=250)
    lbl.image = img

def Hide():
    global secret
    message = text1.get(1.0, END).strip()
    email = email_entry.get().strip()

    if message and email:
        # Hide the message inside the image
        secret = lsb.hide(str(filename), message)
        text1.delete(1.0, END)  # Clear the text area
        text1.insert(END, "Data hidden successfully!")  # Display a success message

        # Save the image with hidden data
        hidden_image_path = filename.split(".")[0] + "_hidden.png"
        secret.save(hidden_image_path)

        # Send an email with the hidden image attached
        email_sent = send_email(email, "Your data has been successfully hidden within the image.", hidden_image_path)
        
        if email_sent:
            text1.insert(END, f"\nEmail sent to {email} with the hidden image attached.")
        else:
            text1.insert(END, "\nFailed to send email.")
    else:
        text1.delete(1.0, END)
        text1.insert(END, "Please enter both message and email.")


def Show():
    try:
        clear_message = lsb.reveal(filename)
        text1.delete(1.0, END)
        text1.insert(END, clear_message)
    except IndexError:
        text1.delete(1.0, END)
        text1.insert(END, "No hidden message found in the image.")

def save():
    try:
        if 'filename' in globals():
            f, _ = filename.split(".")
            secret.save("".join((f, "_hidden.png")))
        else:
            secret.save("hidden.png")
    except:
        secret.save("hidden.png")

# UI Components
# Icon
image_icon = PhotoImage(file="./img/logo.jpg")
root.iconphoto(False, image_icon)

# Logo
logo = PhotoImage(file="./img/logo1.png")
Label(root, image=logo, bg="#2f4155").place(x=10, y=0)

# Title
Label(root, text="CodeCrypt", bg="#2f4155", fg="White", font="arial 25 bold").place(x=100, y=20)

# First Frame
f = Frame(root, bd=3, bg="black", width=340, height=280, relief=GROOVE)
f.place(x=10, y=80)

lbl = Label(f, bg="black")
lbl.place(x=40, y=10)

# Second Frame for TextArea
frame2 = Frame(root, bd=3, bg="white", width=340, height=280, relief=GROOVE)
frame2.place(x=350, y=80)

# Text Area
text1 = Text(frame2, font="Robote 20", bg="White", fg="black", relief=GROOVE)
text1.place(x=0, y=0, width=320, height=295)

# Scrollbar
scrollbar1 = Scrollbar(frame2)
scrollbar1.place(x=320, y=0, height=300)
scrollbar1.configure(command=text1.yview)
text1.configure(yscrollcommand=scrollbar1.set)

# Third Frame for Buttons
frame3 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame3.place(x=10, y=370)

Button(frame3, text="Open Image", width=10, height=2, font="arial 14 bold", command=showimage).place(x=20, y=30)
Button(frame3, text="Save Image", width=10, height=2, font="arial 14 bold", command=save).place(x=180, y=30)
Label(frame3, text="Picture, Image, Photo file", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Fourth Frame for Hide/Show Buttons
frame4 = Frame(root, bd=3, bg="#2f4155", width=330, height=100, relief=GROOVE)
frame4.place(x=360, y=370)

Button(frame4, text="Hide Data", width=10, height=2, font="arial 14 bold", command=Hide).place(x=20, y=30)
Button(frame4, text="Show Data", width=10, height=2, font="arial 14 bold", command=Show).place(x=180, y=30)
Label(frame4, text="Picture, Image, Photo file", bg="#2f4155", fg="yellow").place(x=20, y=5)

# Email Entry
Label(root, text="Enter Email:", bg="#2f4155", fg="white", font="arial 14").place(x=720, y=80)
email_entry = Entry(root, font="arial 14", width=30)
email_entry.place(x=720, y=120)

# To refresh entire application
def refresh():
    global filename
    filename = None
    text1.delete(1.0, END)
    lbl.config(image=None)
    email_entry.delete(0, END)

Button(root, text="Refresh", width=10, height=2, font="arial 14 bold", command=refresh).place(relx=1.0, rely=0.0, anchor=NE)

root.mainloop()
