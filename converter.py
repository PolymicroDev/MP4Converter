import customtkinter as ctk
from customtkinter import filedialog
from pytube import YouTube
from pytube.exceptions import PytubeError
from tkinter import *
from PIL import Image

def path_out():
    global out_path
    out_path = filedialog.askdirectory(mustexist=True)
    if out_path:
        details_frame.pack(padx=10, pady=12)
        label_path.configure(text = f"{out_path}")

def download():
    link = entry.get()  # Retrieve the link from the entry widget
    finished.configure(text = 'Downloading...')
    try:
        yt = YouTube(link)
        title = yt.title
        if check_audio.get() == 1:
            streams = yt.streams.filter(only_audio=True).order_by("abr").desc()
        else:
            streams = yt.streams.filter(progressive=True, mime_type="video/mp4").order_by('resolution').desc()

        
        streams.first().download(out_path)
        finished.configure(text = 'Download successful!', text_color = "green")

    except PytubeError as e:
        print("Error downloading the video:", str(e))
        finished.configure(text = "Error: invalid URL", text_color = "red")


out_path = ""       
ctk.set_appearance_mode("Dark")

root = ctk.CTk()
root.geometry("550x500")

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

title = ctk.CTkLabel(master=frame, text="YouTube to MP4 converter", font=("Montserrat", 24))
title.pack(pady=12, padx=10)

entry_frame = ctk.CTkFrame(master=frame)
entry_frame.pack(padx=10, pady=18)

# Place the "Video URL" entry field and "Only Audio" checkbox in the same line
entry = ctk.CTkEntry(master=entry_frame, placeholder_text="Video URL", width=250)
entry.pack(side="left", padx=13)

browse_image = ctk.CTkImage(light_image=Image.open("./mp4-converter/folder_icon.png"),size=(10,12))
browse_button = ctk.CTkButton(master=entry_frame, text="Select folder",
                        command=path_out, image=browse_image,
                        width=130, fg_color = "#06a5c4",
                        hover_color="#046b80", font=ctk.CTkFont(family='Roboto', size=14) )
browse_button.pack(side="left",pady=20, padx=10)

details_frame = ctk.CTkFrame(master=frame)
label_path = ctk.CTkLabel(master=details_frame, text="", font=("Roboto", 15))
label_path.pack(padx=10, pady=10)

download_frame = ctk.CTkFrame(master=frame)
download_frame.pack(ipadx = 40, ipady = 10, pady=20)
dw_button = ctk.CTkButton(master=download_frame, text="Download",
                        command=download, width=150,
                        height=40, fg_color="#009933", hover_color="#006622",
                        font=ctk.CTkFont(family='Roboto', size=16)
                        )
dw_button.pack(pady = 20, padx = 10)


check_audio = ctk.CTkCheckBox(master=download_frame, text="Only Audio", font=ctk.CTkFont(family='Roboto', size=14))
check_audio.pack(padx = 10, pady = 6)


finished = ctk.CTkLabel(master = download_frame, text="", font=("Roboto", 15))
finished.pack()


root.mainloop()