import re
import datetime
import tkinter as tk
import tkinter.font as tk_font

from googleapiclient.discovery import build


class Url:

    def __init__(self, master):
        self.master = master
        self.mainframe = tk.Frame(self.master, bg='lightblue')
        self.mainframe.pack(fill=tk.BOTH, expand=True)
        self.entry = tk.Entry(  # URL input
            self.mainframe,
            bd=3,
            width=50,
        )

        # Calling methods
        self.build_grid()
        self.build_header()
        self.build_widget()

    def build_grid(self):
        self.mainframe.columnconfigure(0, weight=3)
        self.mainframe.columnconfigure(1, weight=2)
        self.mainframe.columnconfigure(2, weight=1)
        self.mainframe.rowconfigure(0, weight=1)
        self.mainframe.rowconfigure(1, weight=1)
        self.mainframe.rowconfigure(2, weight=2)

    def build_header(self):
        banner = tk.Label(
            self.mainframe,
            text='Find out how long your playlist is',
            fg="white",
            bg='lightblue',
            font=("Courier", 24)
        )
        banner.grid(
            row=0, column=0,
            sticky='ew',
            padx=5, pady=10,
        )

    def build_widget(self):

        title = tk.Label(
            self.mainframe,
            text="URL: ",
            fg="grey",
            bg='lightblue',
            font=("Courier", 14),
        )
        title.grid(
            row=1, column=0,
            sticky='w',
            pady=10,
        )

        self.entry.grid(
            row=1, column=0,
            sticky='w',
            pady=10, padx=60,
        )

        button_font = tk_font.Font(family="Arial", size=8, weight="bold", slant="italic")

        button = tk.Button(
            self.mainframe,
            text="Submit",
            font=button_font,
            bd=2,
            command=self.url,
        )

        button.grid(
            row=1, column=0,
            sticky="w",
            padx=380,
        )

    def url(self):

        yt_url = re.compile(r'\b=(\w+)')
        get_id = yt_url.search(self.entry.get()).group(1)

        api_key = 'AIzaSyAwfXHyNN54LWmT_9IzAPdXT4iOb0QgauQ'

        hours_pattern = re.compile(r'(\d+)H')
        minutes_pattern = re.compile(r'(\d+)M')
        seconds_pattern = re.compile(r'(\d+)S')

        total_seconds = 0

        next_page_token = None
        while True:
            youtube = build('youtube', 'v3', developerKey=api_key)

            pl_request = youtube.playlistItems().list(
                part='contentDetails',
                playlistId=get_id,
                maxResults=50,
                pageToken=next_page_token,
            )

            pl_response = pl_request.execute()

            vid_ids = [item['contentDetails']['videoId'] for item in pl_response['items']]

            vid_request = youtube.videos().list(
                part="contentDetails",
                id=','.join(vid_ids),
            )

            vid_response = vid_request.execute()

            for item in vid_response['items']:
                duration = item['contentDetails']['duration']

                hours = hours_pattern.search(duration)
                minutes = minutes_pattern.search(duration)
                seconds = seconds_pattern.search(duration)

                hours = int(hours.group(1)) if hours else 0
                minutes = int(minutes.group(1)) if minutes else 0
                seconds = int(seconds.group(1)) if seconds else 0

                video_seconds = datetime.timedelta(
                    hours=hours,
                    minutes=minutes,
                    seconds=seconds
                ).total_seconds()

                total_seconds += video_seconds

            next_page_token = pl_response.get('next_page_token')

            if not next_page_token:
                break

        total_seconds = int(total_seconds)

        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)

        playlist_time = tk.Label(
            self.mainframe,
            text=f'playlist time: {hours}:{minutes}:{seconds}',
            fg='white',
            bg='lightblue',
            font=tk_font.Font(
                family="Courier",
                size=18,
                weight="bold",
                slant="italic"),
        )

        playlist_time.grid(
            row=1, column=1,
            sticky='ew',
        )

        print(f'playlist time: {hours}:{minutes}:{seconds}')


if '__main__' == __name__:
    root = tk.Tk()
    root.title("Playlist time")
    root.resizable(False, False)
    Url(root)
    root.mainloop()
