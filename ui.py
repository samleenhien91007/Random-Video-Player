import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import cv2
from PIL import Image, ImageTk
import os
import random

class VideoPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Random Video Player")
        self.root.geometry("800x600")

        self.title_label = tk.Label(root, text=u"Máy Kiểm Tra Độ Đẹp Gái", font=("Helvetica", 24))
        self.title_label.pack(pady=20)

        self.open_button = tk.Button(root, text="Open Folder", command=self.open_folder)
        self.open_button.pack(pady=10)

        self.play_random_button = tk.Button(root, text="Play Random Video", command=self.open_random_video)
        self.play_random_button.pack(pady=10)

        self.video_label = tk.Label(root)
        self.video_label.pack()

        self.play_button = tk.Button(root, text="Play", command=self.play_video)
        self.play_button.pack(side=tk.LEFT, padx=10)

        self.pause_button = tk.Button(root, text="Pause", command=self.pause_video)
        self.pause_button.pack(side=tk.RIGHT, padx=10)

        self.cap = None
        self.playing = False
        self.video_files = []

    def open_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.video_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith(('.mp4', '.avi', '.mkv'))]
            if self.video_files:
                messagebox.showinfo("Folder Loaded", "Videos loaded successfully!")

    def open_random_video(self):
        if self.video_files:
            video_path = random.choice(self.video_files)
            self.cap = cv2.VideoCapture(video_path)
            self.play_video()

    def play_video(self):
        if self.cap and not self.playing:
            self.playing = True
            self.update_frame()

    def pause_video(self):
        self.playing = False

    def update_frame(self):
        if self.playing:
            ret, frame = self.cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)
                imgtk = ImageTk.PhotoImage(image=img)
                self.video_label.imgtk = imgtk
                self.video_label.configure(image=imgtk)
                self.root.after(10, self.update_frame)
            else:
                self.cap.release()
                self.playing = False

if __name__ == "__main__":
    root = tk.Tk()
    player = VideoPlayer(root)
    root.mainloop()
