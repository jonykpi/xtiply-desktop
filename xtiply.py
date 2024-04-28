import base64
import json
import re
import tkinter as tk
import webbrowser
from tkinter import filedialog
import os
import threading
import datetime
import time
from tkinter import messagebox
import subprocess
import platform
import shutil
import requests
import mimetypes




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
            try:
                if folder_path.get() and self.email:
                    send_email_with_attachment()
                   # receive_file_to_api()
                    time.sleep(10)  # Wait for 10 seconds
                    result.config(text=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    stop_api()
                    messagebox.showerror("Error", "Please provide both folder path and email.")
            except Exception as e:
                messagebox.showerror("Error",str(e))


    def stop_api_calling(self):
        self.running = False


def print_file(file_path):
    system = platform.system()
    if system == "Windows":
        print("print-windwoes",file_path)
        os.startfile(file_path, "print")
    elif system == "Darwin":  # macOS
        os.system(f"open -a Preview {file_path}")
    elif system == "Linux":
        os.system(f"xdg-open {file_path}")
    else:
        print("Unsupported operating system")


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


def download_file(id,host,url, save_path):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            with open(save_path, 'wb') as f:
                f.write(response.content)
            # messagebox.showinfo("showinfo", "File downloaded successfully at:"+save_path)
            # print("File downloaded successfully at:", save_path)
            viewed = host + "/api/update-downloadable-file?id=" + str(id)
            requests.get(viewed)
        else:
            print("Failed to download file. Status code:", response.status_code)
    except Exception as e:
        messagebox.showerror("Error",str(e))


def receive_file_to_api():
    host = "https://beta-admin.docs2ai.com"
    api_url = host+"/api/get-latest-downloadable-files?email=" + email_entry.get()

    response = requests.get(api_url)
    if response.status_code == 200:
        files = response.json()  # Assuming the API returns a JSON list of file URLs
        for index, file in enumerate(files['data']):
            print(file)
            downloaded_path = folder_path.get()+"/downloaded/"
            file_new_save_path = folder_path.get()+"/downloaded/"+(file['media'][0]['file_name'])
           # file_new_save_path = remove_special_characters(file_new_save_path)
            if not os.path.exists(downloaded_path):
             os.makedirs(downloaded_path)
            download_file(file['id'],host,file['media'][0]['original_url'],file_new_save_path)
            if file['printable'] == 1 :
             print_file(file_new_save_path)


    else:
        print("Failed to fetch files from the API.")


# print(api_url,"this is print froom new")
def send_file_to_api():
    dir = folder_path.get()

    # Replace 'http://example.com/upload' with the URL of your API
    api_url = 'https://webhook.site/6d7154db-eb6e-47ef-bf9f-6d98e6080d11'

    for filename in os.listdir(folder_path.get()):
        file_path = os.path.join(folder_path.get(), filename)
        print(file_path)

        # #Create a multipart/form-data request with the file
        # with open(file_path, 'rb') as file:
        #     files = {'file': file}
        #     response = requests.post(api_url, files=files)
        #
        # # Check if the request was successful
        # if response.status_code == 200:
        #     destination_path = dir + "/uploaded"
        #     os.makedirs(destination_path, exist_ok=True)
        #     filename = os.path.basename(file_path)
        #     timestamp = int(time.time())
        #     new_filename = f"{timestamp}_{filename}"
        #     destination_path = os.path.join(destination_path, new_filename)
        #     shutil.move(file_path, destination_path)

        # else:
    #  print(f"Failed to send file {file_path}. Status code: {response.status_code}")
def send_email_with_attachment():
    email = email_entry.get()
    for filename in os.listdir(folder_path.get()):
        file_path = os.path.join(folder_path.get(), filename)
        file_extension = file_path.split('.')[-1].lower()
        mime_type_mapping = {
            'png': 'image/png',
            'xlsx': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'doc': 'application/msword',
            'docs': 'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'jpg': 'image/jpeg',
            'jpeg': 'image/jpeg'
        }
        content_type = mime_type_mapping.get(file_extension, "None")

        # If content type not found in mapping, use the default from mimetypes
        print(content_type, "content_type")
        if content_type != "None":
            print(file_path,"file_pathfile_pathfile_path")
            with open(file_path, 'rb') as file:
              file_content = file.read()
            # Encode the file content in base64
            encoded_file_content = base64.b64encode(file_content).decode('utf-8')

            # Determine the content type based on the file extension
            content_type, _ = mimetypes.guess_type(file_path)

            # Construct the email data
            email_data = {
                "headers": {
                    "to": email,
                    "subject": "",
                    "mime_version": "1.0",
                    "content_type": "multipart/mixed; boundary=00000000000041a55706112728cd"
                },
                "envelope": {
                    "to": email,
                    "recipients": [email],
                    "from": "your_email@example.com",
                    "helo_domain": "your_domain.com",
                    "remote_ip": "your_remote_ip",
                    "tls": True,
                    "tls_cipher": "TLSv1.3",
                    "md5": "your_md5_hash",
                    "spf": {
                        "result": "neutral",
                        "domain": "example.com"
                    }
                },
                "plain": "-- \r\n*Best regards*\r\n*Your Name*\r\nYour Job Title",
                "html": "<div dir=\"ltr\"><br clear=\"all\"><div><br></div><span class=\"gmail_signature_prefix\">-- </span><br><div dir=\"ltr\" class=\"gmail_signature\" data-smartmail=\"gmail_signature\"><div dir=\"ltr\"><b style=\"color:rgb(56,118,29);font-family:&quot;comic sans ms&quot;,sans-serif\">Best regards</b><div><font face=\"comic sans ms, sans-serif\"><i><b><font style=\"background-color:rgb(255,255,255)\" color=\"#666666\">Your Name</font></b></i><br></font><div><span style=\"color:rgb(68,68,68);font-family:&quot;comic sans ms&quot;,sans-serif\">Your Job Title</span></div></div></div></div></div>",
                "reply_plain": None,
                "attachments": [
                    {
                        "content": encoded_file_content,
                        "file_name": file_path.split("/")[-1],
                        "content_type": content_type or "application/octet-stream",
                        "size": str(len(encoded_file_content)),
                        "disposition": "attachment",
                        "content_id": "<f_lsie9zgc0>"
                    }
                ]
            }

            # Convert to JSON
            email_json = json.dumps(email_data)

            # # Call your API
            api_url = "https://webhook.site/6d7154db-eb6e-47ef-bf9f-6d98e6080d11"
            headers = {'Content-Type': 'application/json'}
            response = requests.post(api_url, data=email_json, headers=headers)

            if response.status_code == 200:
                destination_path = folder_path.get() + "/uploaded"
                if not os.path.exists(destination_path):
                    os.makedirs(destination_path)

                filename = os.path.basename(file_path)
                timestamp = int(time.time())
                new_filename = f"{timestamp}_{filename}"
                destination_path = os.path.join(destination_path, new_filename)
                shutil.move(file_path, destination_path)

            # Print the response
            print(response.text)



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


def open_link(event):
    webbrowser.open("https://www.xtiply.com/")


def remove_special_characters(text):
    # Define the pattern to match special characters
    pattern = r'[^a-zA-Z0-9\s]'  # Matches anything that is not alphanumeric or whitespace

    # Use the sub() function to replace matches with an empty string
    clean_text = re.sub(pattern, '', text)

    return clean_text


# Create the main Tkinter window
window = tk.Tk()
window.title("Docs2ai Agent")

# Set the size of the window
window.geometry("600x400")  # Set width to 600 pixels and height to 400 pixels

# Replace with the path to your logo file
# logo = ImageTk.PhotoImage(Image.open("logo.png"), width=100)
# logo_label = tk.Label(window, image=logo)
# logo_label.pack(pady=10)

# Create email entry
email_label = tk.Label(window, text="Enter email:", width="200")
email_label.pack()
email_entry = tk.Entry(window)
email_entry.pack()

folder_label = tk.Label(window, text="Folder path:", width="200", state="disabled")
folder_label.pack()
folder_path = tk.Entry(window)
folder_path.pack()

choose_button = tk.Button(window, text="Choose Destination", command=choose_folder)
choose_button.pack()

# Create start button
start_button = tk.Button(window, text="Start", command=start_api)
start_button.pack()

# Create stop button
stop_button = tk.Button(window, text="Stop", command=stop_api)
stop_button.config(state=tk.DISABLED)
stop_button.pack()

# Footer
footer_frame = tk.Frame(window)
footer_frame.pack(side="bottom", fill="x")

powered_by_label = tk.Label(footer_frame, text="Docs2ai Agent v1 by XTIPLY", fg="gray", cursor="hand2")
powered_by_label.pack(side="bottom", padx=10, pady=5)
powered_by_label.bind("<Button-1>", open_link)

result = tk.Label(window, text="")
result.pack()

# Run the Tkinter event loop
window.mainloop()
