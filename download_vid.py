import tkinter as tk
from tkinter import ttk, messagebox
import os
from datetime import datetime
import yt_dlp


DOWNLOAD_FOLDER = os.path.join(os.path.expanduser("~"), "Downloads", "VideoDownloader")

if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

class VideoDownloader:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Short Form Video Downloader")
        self.window.geometry("600x400")
        self.setup_ui()

    def setup_ui(self):
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        ttk.Label(main_frame, text="Enter Video URL:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.url_entry = ttk.Entry(main_frame, width=50)
        self.url_entry.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)

        ttk.Button(main_frame, text="Download", command=self.download_video).grid(row=2, column=0, pady=20)

        self.progress = ttk.Progressbar(main_frame, length=400, mode='determinate')
        self.progress.grid(row=3, column=0, columnspan=2, pady=10)

        self.status_label = ttk.Label(main_frame, text="Ready to download...")
        self.status_label.grid(row=4, column=0, columnspan=2, pady=5)

        ttk.Label(main_frame, text="Download History:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.history_text = tk.Text(main_frame, height=10, width=50)
        self.history_text.grid(row=6, column=0, columnspan=2, pady=5)

    def update_status(self, message):

        self.status_label.config(text=message)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.history_text.insert('1.0', f"[{timestamp}] {message}\n")

    def download_video(self):
        #Main download function
        url = self.url_entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        self.update_status("Downloading video...")

        # Reset progress bar
        self.progress['value'] = 0
        self.window.update_idletasks()

        output_template = os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s")

        ydl_opts = {
            'outtmpl': output_template,
            'format': 'best',  # Get best quality available
            'progress_hooks': [self.update_progress],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
                self.update_status("Download completed successfully!")
                messagebox.showinfo("Success", "Video downloaded successfully!")
        except Exception as e:
            self.update_status(f"Error: {str(e)}")
            messagebox.showerror("Error", f"Download failed: {str(e)}")

    def update_progress(self, d):
        """Update progress bar during download"""
        if d['status'] == 'downloading':
            percentage = d.get('_percent_str', '0%').strip('%')
            try:
                self.progress['value'] = float(percentage)
                self.window.update_idletasks()
            except ValueError:
                pass

    def run(self):
        #Start the application
        self.window.mainloop()

if __name__ == "__main__":
    app = VideoDownloader()
    app.run()
