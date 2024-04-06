import tkinter as tk
import threading
import datetime
import time


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
            result.config(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"));
            time.sleep(3)  # Wait for 10 seconds

    def stop_api_calling(self):
        self.running = False


def start_api():
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
window.title("Docs2Ai")

# Set the size of the window
window.geometry("600x400")  # Set width to 600 pixels and height to 400 pixels

# Create email entry
email_label = tk.Label(window, text="Enter email:")
email_label.pack()
email_entry = tk.Entry(window)
email_entry.pack()

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
