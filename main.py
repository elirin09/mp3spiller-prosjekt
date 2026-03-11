from tkinter import *
# linje 3-10 er skrevet med KI
from tkinter import filedialog
from PIL import Image, ImageTk
import pygame
import os
try:
    from mutagen.mp3 import MP3
except ImportError:
    MP3 = None

root = Tk()
root.title("Music Player")
root.geometry("720x480")

pygame.mixer.init()

songlist = Listbox(root, bg="black", fg="white", width=100, height=20)
songlist.pack()

