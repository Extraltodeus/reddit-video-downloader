#!/usr/bin/env python
from tkinter import Entry,Button,Tk,END
import tkinter.font as tkFont
import tkinter.ttk
import requests
import os
import subprocess
import clipboard
from urllib.request import urlopen, URLError

real_path = os.path.dirname(os.path.realpath(__file__))
os.system("mkdir " + real_path+"/Output")

win = Tk()
win.attributes("-fullscreen", False)
myFont = tkFont.Font(family = 'Mono', size = 15, weight = 'bold')
win.title("Reddit-video-downloader")
win.geometry('1280x90')
win.configure(background='black')

isUrl = False

def validate_web_url(url):
    try:
        urlopen(url)
        return True
    except:
        return False


def redditDownloader():
    print(isUrl)

    if isUrl:
        post_url = pressepape
    else:
        post_url = urlInput.get()

    # use UA headers to prevent 429 error
    headers = {
        'User-Agent': 'My User Agent 1.0',
        'From': 'testyouremail@domain.com'
    }
    url = post_url + ".json"
    data = requests.get(url, headers=headers).json()
    media_data = data[0]["data"]["children"][0]["data"]["media"]
    title = data[0]["data"]["children"][0]["data"]["title"]

    video_url = media_data["reddit_video"]["fallback_url"]
    audio_url = video_url.split("DASH_")[0] + "audio"

    os.system("curl -o video.mp4 {}".format(video_url))
    os.system("curl -o audio.wav {}".format(audio_url))

    video_path  = os.path.join(real_path,"Output",title)+".mp4"
    folder_path = os.path.join(real_path,"Output")

    os.system('ffmpeg -y -i video.mp4 -i audio.wav -c:v copy -c:a aac -strict experimental "{}"'.format(video_path))
    os.system('xdg-open "{}"'.format(folder_path))
    os.system('start "{}"'.format(folder_path)) # fallback for Windows users

def quitter():
    win.destroy()

pressepape = clipboard.paste()

if isinstance(pressepape, str) and validate_web_url(pressepape):
    isUrl = True
    redditDownloader()
else:
    pressepape = ""

    bDownload = Button(win, text = "Download", font = myFont, command = redditDownloader)
    bDownload.place(x=20,   y=20, height = 50, width =120 )

    urlInput = Entry(win)
    urlInput.place(x=150,   y=20, height = 50, width =980 )
    urlInput.insert(END,pressepape)

    bQuitter = Button(win, text = "Exit", font = myFont, command = quitter)
    bQuitter.place(x=1140,   y=20, height = 50, width =120 )

    win.mainloop()
