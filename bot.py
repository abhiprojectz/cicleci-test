import random
import requests # to get image from the web
import shutil
from images_db import urls
from PIL import Image
import os, sys
from PIL import Image
import string
from moviepy.editor import *
import time
import os 
import subprocess
from os.path import exists
import schedule
from time import sleep
import argparse
import logging
from argparse import ArgumentError
import os
import datetime

# ========================= ONLY FOR META3 (INSPIRA) =====================

dir_path = os.path.dirname(os.path.realpath(__file__))
fps = 24

curr = 'nil'
a = 'meta1' # countdx
b = 'meta2' # ayush11 (Ai facts)
c = 'meta3' # inspira

def id_generator(size=20, chars=string.ascii_uppercase + string.digits):
  return ''.join(random.choice(chars) for _ in range(size))

def deleteDownloads():
    dir = os.path.join(dir_path, "downloaded")
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

def deleteResized():
    dir = os.path.join(dir_path, "resized")
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

def deleteVid():
    dir = os.path.join(dir_path, "outputs")
    for files in os.listdir(dir):
        path = os.path.join(dir, files)
        try:
            shutil.rmtree(path)
        except OSError:
            os.remove(path)

def getImage():
	pics = []
	for _ in range(3):
		x = random.choice(urls)
		pics.append(x)
	return pics

def resizer(f):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    fz = os.path.join(dir_path, "resized")
    now = datetime.datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    im = Image.open(f)
    new_img = im.resize((720,im.height))
    x, y = im.size
    # size = max(720, x, y)
    fill_color=(0, 0, 0, 0)
    new_im = Image.new('RGBA', (720, 1280), fill_color)
    # new_im.paste(im, (int((size - x) / 2), int((size - y) / 2)))
    size_h = int((1280 - y)/2)
    size_w = int(0)
    new_im.paste(new_img, (size_w, size_h))
    new_im.convert('RGB').save(os.path.join(fz ,'111111' + now + '.jpg'), 'JPEG')

def downloadImg():
    imgs = getImage()
    heads = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    # imgs = ["89994Xinspirational-quote-life-unknown-author-pretty-monarch-butterfly-perched-flower-43678437.jpg", "D3IK1Linspirational-quote-happiness-c-e-jerningham-two-adorable-poodles-enjoying-life-to-fullest-43678289.jpg","SE8AJ8inspirational-phrases-be-positive-believe-yourself-enjoy-life-motivational-notes-papers-48980497.jpg" ]
    for i in imgs:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        image_url = i
        filename = id_generator() + ".jpg"
        fz = os.path.join(dir_path, "downloaded")
        r = requests.get(image_url,headers=heads, stream = True)
        if r.status_code == 200:
            r.raw.decode_content = True
            with open(filename,'wb') as f:
                shutil.copyfileobj(r.raw, f)

            shutil.move(str(filename), fz)
            print('Image sucessfully Downloaded: ', id_generator() + filename)

            tp = os.path.join(fz, filename)
            resizer(tp)
        else:
            print('Image Couldn\'t be retreived')
    deleteDownloads()

def getRandomItems(list, n):
    import random
    import math
    random_items = []
    for i in range(n):
        random_items.append(list[int(math.floor(random.random() * len(list)))])
    return random_items

def getRandomImg():
    import os 
    dir_path = os.path.dirname(os.path.realpath(__file__))
    files = []
    fz = os.path.join(dir_path, "resized")
    for file in os.listdir(os.path.join(dir_path, "resized")):
        if file.endswith(".png") or file.endswith(".jpg"):
            files.append(os.path.join(fz, file))
            # print(os.path.join(file))
    return files

def generateVedio(file_name):
    dest = os.path.join(dir_path, "outputs")
    images_list = getRandomImg()

    clips = [ImageClip(m).set_duration(5)
            for m in images_list]

    ms = ['music1.mp3', 'music2.mp3', 'music3.mp3', 'music4.mp3', 'music5.mp3', 'music6.mp3']
    music = os.path.join(dir_path, random.choice(ms))
    audioclip = AudioFileClip(music).set_duration(15)
    target = os.path.join(dest, f"{file_name}.mp4")
    concat_clip = concatenate_videoclips(clips, method="compose").set_audio(audioclip)
    # concat_clip.write_videofile(target, fps=fps, codec="mpeg4")
    concat_clip.write_videofile(target, fps=fps)
    deleteResized()

def bulkGenerate():
    fs = ["vid_a", "vid_b", "vid_c", "vid_d"]
    for i in range(4):
        downloadImg()
        sleep(3)
        generateVedio(fs[i])
        print(f"{i +1} Short generated!")


def uploadVid(vid, acc, times):
    today = datetime.date.today()
    raw_t = str(today) + "T" + str(times)
    subprocess.call(f"python /home/circleci/project/main.py --browser=chrome --login-cookies-path=/home/circleci/project/{acc}.json  --title='hjh' --description='uujhj' /home/circleci/project/outputs/{vid}.mp4 --upload_time={raw_t}", shell=True)
    
    # subprocess.call(f"python C:\\Users\\abhis\\Desktop\\YT\\__YTEngine\\main.py --browser=chrome --login-cookies-path=C:\\Users\\abhis\\Desktop\\YT\\__YTEngine\\{acc}.json  --title='tss' --description='dfdfd' C:\\Users\\abhis\\Desktop\\YT\\__YTEngine\\outputs\\{vid}.mp4 --upload_time={raw_t}")


# def bulkUpload():
#     parser = get_arg_parser()
#     args = parser.parse_args()

#     acc_ = args.acc
#     time_slot = args.slot
#     fs = ["vid_a", "vid_b", "vid_c", "vid_d"]

#     if time_slot == "AM":
#         times = ["03:00:00", "06:00:00", "09:00:00", "11:30:00"]
#     else:
#         times = ["15:00:00", "18:00:00", "21:00:00", "23:30:00"]

#     print("Uploading vid to youtube....")
#     print(f"{time_slot} detected!")
#     for i in range(4):
#         uploadVid(fs[i], acc_, times[i])
#         print(f"Successfully uploaded {i +1} shorts!")
#         sleep(60)


def createContent():
    bulkGenerate()
    # bulkUpload()
    print("Mission pass !")
    

if __name__ == "__main__":
    createContent()