from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import os
try:
    from mutagen.mp3 import MP3
except ImportError:
    MP3 = None

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("MP3 Spiller")
        self.root.geometry("720x700")
        self.root.config(bg="black")
        
        pygame.mixer.init()
        
        self.playlist = []
        self.current_song_index = 0
        self.is_paused = False
        
        # Title Label
        title_label = Label(self.root, text="MP3 Spiller", fg="white", bg="black", font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Import and delete buttons frame
        top_buttons_frame = Frame(self.root, bg="black")
        top_buttons_frame.pack(pady=5)
        
        import_btn = Button(top_buttons_frame, text="Importer MP3 filer", command=self.import_files, bg="gray", fg="white", font=("Arial", 12))
        import_btn.grid(row=0, column=0, padx=5)
        
        delete_btn = Button(top_buttons_frame, text="🗑 Slett sang", command=self.delete_song, bg="#8B0000", fg="white", font=("Arial", 12))
        delete_btn.grid(row=0, column=1, padx=5)
        
        # Playlist display
        playlist_label = Label(self.root, text="Sangliste:", fg="white", bg="black", font=("Arial", 12))
        playlist_label.pack(anchor=W, padx=20)
        
        self.songlist = Listbox(self.root, bg="gray20", fg="white", width=90, height=12, font=("Arial", 10))
        self.songlist.pack(padx=20, pady=5)
        self.songlist.bind('<<ListboxSelect>>', self.select_song)
        
        # Current song label
        self.current_song_label = Label(self.root, text="Ingen sang spilles", fg="yellow", bg="black", font=("Arial", 11))
        self.current_song_label.pack(pady=5)
        
        # Control frame
        control_frame = Frame(self.root, bg="black")
        control_frame.pack(pady=10)
        
        # Control buttons
        self.previous_btn = Button(control_frame, text="⏮ Forrige", command=self.previous_song, bg="gray", fg="white", font=("Arial", 11), width=15)
        self.previous_btn.grid(row=0, column=0, padx=5)
        
        self.play_btn = Button(control_frame, text="▶ Spill", command=self.play_song, bg="green", fg="white", font=("Arial", 11), width=15)
        self.play_btn.grid(row=0, column=1, padx=5)
        
        self.pause_btn = Button(control_frame, text="⏸ Pause", command=self.pause_song, bg="orange", fg="white", font=("Arial", 11), width=15)
        self.pause_btn.grid(row=0, column=2, padx=5)
        
        self.next_btn = Button(control_frame, text="Neste ⏭", command=self.next_song, bg="gray", fg="white", font=("Arial", 11), width=15)
        self.next_btn.grid(row=0, column=3, padx=5)
        
        self.stop_btn = Button(control_frame, text="⏹ Stopp", command=self.stop_song, bg="red", fg="white", font=("Arial", 11), width=15)
        self.stop_btn.grid(row=0, column=4, padx=5)
    
    
    def import_files(self):
        """Importer MP3 filer fra datamaskinen"""
        files = filedialog.askopenfilenames(
            title="Velg MP3 filer",
            filetypes=[("MP3 Files", "*.mp3"), ("All Files", "*.*")],
            initialdir=os.path.expanduser("~")
        )
        
        if files:
            self.playlist.extend(files)
            self.update_playlist_display()
    
    def update_playlist_display(self):
        """Oppdater sanglisten på skjermen"""
        self.songlist.delete(0, END)
        for i, song in enumerate(self.playlist):
            song_name = os.path.basename(song)
            self.songlist.insert(END, f"{i+1}. {song_name}")
    
    def select_song(self, event):
        """Velg sang fra listen"""
        selection = self.songlist.curselection()
        if selection:
            self.current_song_index = selection[0]
    
    def play_song(self):
        """Spill av sang"""
        if not self.playlist:
            self.current_song_label.config(text="Ingen sanger i listen!")
            return
        
        if self.is_paused:
            # Resume if paused
            pygame.mixer.music.unpause()
            self.is_paused = False
        else:
            # Play from current song index
            song = self.playlist[self.current_song_index]
            try:
                pygame.mixer.music.load(song)
                pygame.mixer.music.play()
                song_name = os.path.basename(song)
                self.current_song_label.config(text=f"Nå spiller: {song_name}")
            except Exception as e:
                self.current_song_label.config(text=f"Feil: Kunne ikke spille av {os.path.basename(song)}")
    
    def pause_song(self):
        """Pause sang"""
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.is_paused = True
            self.current_song_label.config(text="⏸ Pauset")
    
    def stop_song(self):
        """Stopp sang"""
        pygame.mixer.music.stop()
        self.is_paused = False
        self.current_song_label.config(text="Stoppet")
    
    def next_song(self):
        """Spill neste sang"""
        if self.playlist:
            self.current_song_index = (self.current_song_index + 1) % len(self.playlist)
            self.songlist.selection_clear(0, END)
            self.songlist.selection_set(self.current_song_index)
            self.songlist.see(self.current_song_index)
            self.play_song()
    
    def previous_song(self):
        """Spill forrige sang"""
        if self.playlist:
            self.current_song_index = (self.current_song_index - 1) % len(self.playlist)
            self.songlist.selection_clear(0, END)
            self.songlist.selection_set(self.current_song_index)
            self.songlist.see(self.current_song_index)
            self.play_song()
    
    def delete_song(self):
        """Slett valgt sang fra listen"""
        selection = self.songlist.curselection()
        if not selection:
            self.current_song_label.config(text="Velg en sang å slette!")
            return
        
        song_index = selection[0]
        song_name = os.path.basename(self.playlist[song_index])
        
        # Stop playing if deleting current song
        if song_index == self.current_song_index:
            pygame.mixer.music.stop()
            self.is_paused = False
        
        # Remove song from playlist
        self.playlist.pop(song_index)
        
        # Adjust current song index if needed
        if self.playlist:
            if song_index >= len(self.playlist):
                self.current_song_index = len(self.playlist) - 1
            else:
                self.current_song_index = song_index
        else:
            self.current_song_index = 0
            self.current_song_label.config(text="Ingen sanger i listen")
        
        # Update display
        self.update_playlist_display()
        self.current_song_label.config(text=f"Slettet: {song_name}")

if __name__ == "__main__":
    root = Tk()
    player = MusicPlayer(root)
    root.mainloop()
