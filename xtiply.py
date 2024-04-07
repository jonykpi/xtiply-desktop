import tkinter as tk
from tkinter import filedialog
import os
import threading
import datetime
import time
import requests
import shutil
from tkinter import messagebox
from PIL import ImageTk, Image

class APICaller:
    def __init__(self, email):
        self.email = email
        self.running = False

    def start_api_calling(self):
        self.running = True
        while self.running:
            # Replace the URL with your API endpoint
            # response = requests.get("https://api.example.com")
            print(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            if folder_path.get() and self.email:
                send_file_to_api()
                time.sleep(10)  # Wait for 10 seconds
                result.config(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
            else:
                stop_api()
                messagebox.showerror("Error", "Please provide both folder path and email.")




    def stop_api_calling(self):
        self.running = False


def choose_folder():
    folder_ral_path = filedialog.askdirectory()
    folder_path.delete(0, tk.END)  # Clear the entry widget
    folder_path.insert(0, folder_ral_path)
    # try to read all file


def is_valid_file_type(file_path):
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.docx', '.pdf', '.xls',
                        '.xlsx']  # Add more extensions as needed
    extension = os.path.splitext(file_path)[1].lower()
    return extension in valid_extensions


def send_file_to_api():
    dir = folder_path.get()

    # Replace 'http://example.com/upload' with the URL of your API
    api_url = 'https://webhook.site/b1c10541-ba74-46b4-be62-18c77e9dfa4a'

    for filename in os.listdir(folder_path.get()):
        file_path = os.path.join(folder_path.get(), filename)

        if is_valid_file_type(file_path):

            # Create a multipart/form-data request with the file
            with open(file_path, 'rb') as file:
                files = {'file': file}
                response = requests.post(api_url, files=files)

            # Check if the request was successful
            if response.status_code == 200:
                destination_path = dir + "/uploaded"
                os.makedirs(destination_path, exist_ok=True)
                filename = os.path.basename(file_path)
                timestamp = int(time.time())
                new_filename = f"{timestamp}_{filename}"
                destination_path = os.path.join(destination_path, new_filename)
                shutil.move(file_path, destination_path)

            else:
                print(f"Failed to send file {file_path}. Status code: {response.status_code}")


def start_api():
    print(email_entry.get())
    print(folder_path.get())
    global api_caller
    api_caller = APICaller(email_entry.get())
    api_thread = threading.Thread(target=api_caller.start_api_calling)
    api_thread.start()
    start_button.config(state=tk.DISABLED)
    stop_button.config(state=tk.NORMAL)


def stop_api():
    global api_caller
    if api_caller:
        api_caller.stop_api_calling()
    start_button.config(state=tk.NORMAL)
    stop_button.config(state=tk.DISABLED)


# Create the main Tkinter window
window = tk.Tk()
window.title("Xtiply")

# Set the size of the window
window.geometry("600x400")  # Set width to 600 pixels and height to 400 pixels

logo_path = "logo.png"  # Replace with the path to your logo file
logo = ImageTk.PhotoImage(Image.open(logo_path),width=100)
logo_label = tk.Label(window, image=logo)
logo_label.pack(pady=10)

# Create email entry
email_label = tk.Label(window, text="Enter email:", width="200")
email_label.pack()
email_entry = tk.Entry(window)
email_entry.pack()

folder_label = tk.Label(window, text="Folder path:", width="200", state="disabled")
folder_label.pack()
folder_path = tk.Entry(window)
folder_path.pack()

choose_button = tk.Button(window, text="Choose File", command=choose_folder)
choose_button.pack()

# Create start button
start_button = tk.Button(window, text="Start", command=start_api)
start_button.pack()

# Create stop button
stop_button = tk.Button(window, text="Stop", command=stop_api)
stop_button.config(state=tk.DISABLED)
stop_button.pack()

result = tk.Label(window, text="")
result.pack()

# Run the Tkinter event loop
window.mainloop()
