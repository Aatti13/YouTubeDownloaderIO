from tkinter import *
from tkinter import messagebox

from PIL import Image, ImageTk
from pytube import YouTube
from googleapiclient.discovery import build
import requests
from datetime import date
from pathlib import Path



class Window:
    def __init__(self, window, master=None):
        # --------------------------------------------------------------------------------------------------------------
        # Default settings & init.
        # YouTube API: AIzaSyB3NEPJMng2JJ1cDOZyuI6W58EGsyC7Pbs
        self.root = window
        self.leel_font = "Leelawadee UI Semilight"
        self.light_bg = "white"
        self.dark_bg = "#0F0F0F"
        self.font = "Roboto"
        self.api = "AIzaSyB3NEPJMng2JJ1cDOZyuI6W58EGsyC7Pbs"
        self.button_checker = False
        self.theme_button_mode = True
        # --------------------------------------------------------------------------------------------------------------
        # Functions

        def you_tube():
            try:
                text = self.text_entry.get()
                link = f"https://www.youtube.com/watch?v={text}"
                p = YouTube(link)
                s = p.thumbnail_url
                rr = requests.get(s)
                y = p.streams.get_highest_resolution()
                file_size = y.filesize_mb
                if file_size >= 1000:
                    file_size = f"{y.filesize_gb} GB"
                else:
                    file_size = f"{y.filesize_mb} MB"
                channel_id = p.channel_id
                duration = p.length // 60
                if duration > 59:
                    duration //= 60
                    ll = "hours"
                else:
                    duration += 1
                    ll = "minutes"
                youtube = build('youtube', 'v3', developerKey=self.api)
                channel_response = youtube.channels().list(part='snippet,statistics', id=channel_id).execute()
                video_response = youtube.videos().list(part='snippet, statistics', id=text).execute()
                subscriber_count = channel_response['items'][0]['statistics']['subscriberCount']
                views = video_response['items'][0]['statistics']['viewCount']
                pda = date.isoformat(p.publish_date)
                cc = pda.split("-")
                published_date = "-".join(cc[::-1])
                with open('images/i.png', 'wb') as f:
                    f.write(rr.content)
                self.thumbnail = Image.open('images/i.png')
                self.thumbnail = ImageTk.PhotoImage(self.thumbnail)
                self.video_thumbnail_label.config(image=self.thumbnail)
                self.video_title_label.config(text=p.title)
                self.creator_label.config(text=f"{views} views | Duration: {duration} {ll} | "
                                               f"Uploaded: {published_date} | File Size: {file_size}")
                self.channel_name_label.config(text=p.author)
                self.subscribers_label.config(text=f"{subscriber_count} subs", bg="red")
                self.download_now_label.config(text="Download Video: ")
                self.button_checker = True
                self.download_button.config(image=self.download_image, command=download)
                self.download_button.place(x=1054, y=477)
            except Exception as e:
                messagebox.showerror("YT Downloader", "Status: ERROR")


        def on_progress(stream, chunk, bytes_remaining):
            previousprogress = 0
            total_size = stream.filesize
            bytes_downloaded = total_size - bytes_remaining

            liveprogress = (int(bytes_downloaded / total_size * 100))
            if liveprogress > previousprogress:
                previousprogress = liveprogress
                print(liveprogress, "*" * liveprogress, sep="\n")


        def download():
            if self.button_checker is True:
                self.download_button.place(x=10000, y=6060)
                text = self.text_entry.get()
                link = f"https://www.youtube.com/watch?v={text}"
                p = YouTube(link)
                p.register_on_progress_callback(on_progress)
                vid = p.streams.filter(progressive=True)
                highest_res = p.streams.get_highest_resolution()
                downloads_path = str(Path.home() / "Downloads")
                vid[vid.index(highest_res)].download(downloads_path)
                self.download_now_label.config(text="Status: Completed")
                self.button_checker = False
            else:
                print("error")


        def theme_change():
            if self.button_checker:

                self.root.config(bg=self.dark_bg)

                self.logo_text.config(fg="white", bg=self.dark_bg)
                self.theme_button.config(image=self.light_mode_img, bg=self.dark_bg)
                self.logo_label.config(image=self.logo_img, bg=self.dark_bg)

                self.search_label.config(image=self.search_img)
                self.text_entry.config(bg=self.dark_bg, fg="white")
                self.search_button.config(image=self.search_button_img, bg=self.dark_bg)
                self.search_button.place(x=955, y=14)

                self.steps_label.config(bg=self.dark_bg, fg="white")
                self.inst_labels.config(bg=self.dark_bg, fg="white")
                self.inst_one_label.config(bg=self.dark_bg, fg="white")
                self.inst_two_label.config(bg=self.dark_bg, fg="white")
                self.inst_three_label.config(bg=self.dark_bg, fg="white")

                self.video_thumbnail_label.config(bg=self.dark_bg)
                self.video_title_label.config(bg=self.dark_bg, fg="white")
                self.creator_label.config(bg=self.dark_bg, fg="white")
                self.channel_name_label.config(bg=self.dark_bg, fg="white")
                # self.subscribers_label.config(bg=self.dark_bg)

                self.download_now_label.config(bg=self.dark_bg, fg="white")
                self.download_button.config(bg=self.dark_bg)

                self.button_checker = False

            elif self.button_checker is False:

                self.root.config(bg=self.light_bg)

                self.logo_text.config(fg="black", bg=self.light_bg)
                self.logo_label.config(bg=self.light_bg, image=self.logo_img_lite)

                self.search_label.config(image=self.search_img_light, bg=self.light_bg)
                self.text_entry.config(bg=self.light_bg, fg="black")
                self.search_button.config(image=self.search_button_img_lite, bg=self.light_bg)
                self.search_button.place(x=955, y=12)

                self.steps_label.config(bg=self.light_bg, fg="black")
                self.inst_labels.config(bg=self.light_bg, fg="black")
                self.inst_one_label.config(bg=self.light_bg, fg="black")
                self.inst_two_label.config(bg=self.light_bg, fg="black")
                self.inst_three_label.config(bg=self.light_bg, fg="black")

                self.video_thumbnail_label.config(bg=self.light_bg)

                self.video_title_label.config(bg=self.light_bg, fg="black")
                self.creator_label.config(bg=self.light_bg, fg="black")
                self.channel_name_label.config(bg=self.light_bg, fg="black")
                # self.subscribers_label.config(bg=self.light_bg)

                self.steps_label.config(bg=self.light_bg, fg="black")

                self.download_now_label.config(bg=self.light_bg, fg="black")
                self.download_button.config(bg=self.light_bg)
                self.theme_button.config(image=self.dark_mode_img, bg=self.light_bg)
                self.button_checker = True

        # --------------------------------------------------------------------------------------------------------------
        # Configurations
        self.root.config(bg=self.dark_bg)
        # --------------------------------------------------------------------------------------------------------------
        # Images
        self.logo_img = Image.open("images/downloaderlogo.png")
        self.logo_img = self.logo_img.resize((75, 50), Image.Resampling.LANCZOS)
        self.logo_img = ImageTk.PhotoImage(self.logo_img)

        self.logo_img_lite = Image.open("images/downloaderlogolight.png")
        self.logo_img_lite = self.logo_img_lite.resize((75, 50), Image.Resampling.LANCZOS)
        self.logo_img_lite = ImageTk.PhotoImage(self.logo_img_lite)

        self.search_img = Image.open("images/search_bar.png")
        self.search_img = ImageTk.PhotoImage(self.search_img)

        self.search_img_light = Image.open("images/search bar light.png")
        self.search_img_light = ImageTk.PhotoImage(self.search_img_light)

        self.search_button_img = Image.open("images/search_icon.png")
        self.search_button_img = ImageTk.PhotoImage(self.search_button_img)

        self.search_button_img_lite = Image.open("images/search button light.png")
        self.search_button_img_lite = ImageTk.PhotoImage(self.search_button_img_lite)

        self.download_image = Image.open("images/download image.png")
        self.download_image = self.download_image.resize((60, 60), Image.Resampling.LANCZOS)
        self.download_image = ImageTk.PhotoImage(self.download_image)

        self.dark_mode_img = Image.open("images/dark mode button.png")
        self.dark_mode_img = self.dark_mode_img.resize((90, 40), Image.Resampling.LANCZOS)
        self.dark_mode_img = ImageTk.PhotoImage(self.dark_mode_img)

        self.light_mode_img = Image.open("images/light mode button.png")
        self.light_mode_img = self.light_mode_img.resize((90, 40), Image.Resampling.LANCZOS)
        self.light_mode_img = ImageTk.PhotoImage(self.light_mode_img)

        self.inst_one_img = Image.open("images/inst-1.png")
        self.inst_one_img = self.inst_one_img.resize((466, 54), Image.Resampling.LANCZOS)
        self.inst_one_img = ImageTk.PhotoImage(self.inst_one_img)

        # --------------------------------------------------------------------------------------------------------------
        # Labels
        self.logo_label = Label(self.root, image=self.logo_img, bd=0, bg=self.dark_bg)
        self.logo_label.place(x=10, y=10)

        self.logo_text = Label(self.root, text="YT Downloader-IO", font=(self.leel_font, 27),
                               bd=-0, bg=self.dark_bg, fg="white")
        self.logo_text.place(x=100, y=10)

        self.search_label = Label(self.root, image=self.search_img, bd=0, bg=self.dark_bg)
        self.search_label.place(x=500+50, y=12)

        self.steps_label = Label(self.root, text="*STEPS*", font=(self.leel_font, 19), bg=self.dark_bg,
                                 fg="white")
        self.steps_label.place(x=900, y=90)

        self.inst_labels = Label(self.root, text="1. Copy the Video I.D of a youtube video & search",
                                 font=(self.leel_font, 16), bg=self.dark_bg, fg=self.light_bg)
        self.inst_labels.place(x=700, y=150)

        self.inst_one_label = Label(self.root, image=self.inst_one_img, bd=0)
        self.inst_one_label.place(x=720, y=190)

        self.inst_two_label = Label(self.root, text="2. Click on the button next to Download now",
                                    font=(self.leel_font, 16), bg=self.dark_bg, fg=self.light_bg)
        self.inst_two_label.place(x=700, y=280)

        self.inst_three_label = Label(self.root, text="3. Wait a few minutes & then enjoy !!",
                                      font=(self.leel_font, 16), bg=self.dark_bg, fg=self.light_bg)
        self.inst_three_label.place(x=700, y=360)

        self.video_title_label = Label(self.root, bd=0, font=(self.leel_font, 16, "bold"), bg=self.dark_bg, fg="white")
        self.video_title_label.place(x=30, y=600)

        self.video_thumbnail_label = Label(self.root, bd=0, bg=self.dark_bg)
        self.video_thumbnail_label.place(x=30, y=100)

        self.creator_label = Label(self.root, bd=0, font=(self.leel_font, 12), bg=self.dark_bg, fg="white")
        self.creator_label.place(x=30, y=640)

        self.subscribers_label = Label(self.root, bd=0, font=(self.leel_font, 14, "bold"), bg=self.dark_bg, fg="white")
        self.subscribers_label.place(x=550, y=680)

        self.channel_name_label = Label(self.root, bd=0, font=("Roboto", 16), bg=self.dark_bg, fg="white")
        self.channel_name_label.place(x=30, y=680)

        self.download_now_label = Label(self.root, bd=0, bg=self.dark_bg, text="",
                                        fg="white", font=(self.leel_font, 25))
        self.download_now_label.place(x=790, y=480)

        self.bottom_right_label = Label(self.root, bg="red", fg="red", height=1, width=100)
        self.bottom_right_label.place(x=840, y=723)


        # --------------------------------------------------------------------------------------------------------------
        # Buttons
        self.search_button = Button(self.root, image=self.search_button_img, bd=0, bg=self.dark_bg,
                                    command=you_tube)
        self.search_button.place(x=905+50, y=14)

        self.download_button = Button(self.root, bd=0, bg=self.dark_bg)
        self.download_button.place(x=1100, y=437)

        self.theme_button = Button(self.root, image=self.light_mode_img, bd=0, bg=self.dark_bg, command=theme_change)
        self.theme_button.place(x=1150, y=15)
        # --------------------------------------------------------------------------------------------------------------
        # Text Entries
        self.text_entry = Entry(self.root, font=(self.leel_font, 14), width=30, bd=0, bg=self.dark_bg, fg="white")
        self.text_entry.place(x=600+50, y=21)
        # --------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    window = Tk()
    window.geometry("1280x730")
    window.title("YouTube Downloader-IO")
    window.resizable(False, False)
    x = Window(window)
    window.mainloop()