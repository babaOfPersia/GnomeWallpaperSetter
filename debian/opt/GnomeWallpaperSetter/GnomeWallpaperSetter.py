#!/usr/bin/env python3

import sys
import requests
import os
import json
import random
from datetime import datetime, timedelta
import multiprocessing

# Get the user's home directory

home_dir = os.path.expanduser('~')
if(home_dir == '/root'):
    home_dir = H_DIR

# Directory to store downloaded wallpapers
WALLPAPER_DIR = home_dir+'/Pictures/Wallpapers'

def readSave():
    save = open("details.sv", "r")
    saveJson = json.loads(save.readline())
    # Set your Unsplash API key
    global UNSPLASH_API_KEY
    global COLLECTION_CODE
    global H_DIR
    H_DIR = saveJson['Hdir']
    UNSPLASH_API_KEY = saveJson['APIKEY']
    COLLECTION_CODE = saveJson['Collection']



# Function to set the wallpaper
def set_wallpaper(image_path):
    os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri-dark 'file://{image_path}'")
    os.system(f"/usr/bin/gsettings set org.gnome.desktop.background picture-uri 'file://{image_path}'")



# Function to download a random wallpaper from Unsplash
def download_random_wallpaper():
    url = 'https://api.unsplash.com/collections/'+str(COLLECTION_CODE)+'/photos?orientation=landscape'
    headers = {
        'Authorization': f'Client-ID {UNSPLASH_API_KEY}'
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        json_obj = json.dumps(data)
        item_dict = json.loads(json_obj)
        json_size = len(item_dict)
        random_img_no = random.randint(0, json_size)
        image_url = data[random_img_no]['urls']['full']
        image_id = data[random_img_no]['id']
        image_extension = image_url.split('.')[-1]

        # Download the image
        image_path = os.path.join(WALLPAPER_DIR, f'{image_id}.{image_extension}')
        response = requests.get(image_url)

        if response.status_code == 200:
            with open(image_path, 'wb') as f:
                f.write(response.content)
            set_wallpaper(image_path)
        else:
            handle_error(response.status_code,"download the image from Unsplash")
    else:
        handle_error(response.status_code,"fetch the image from Unsplash")

# Function to read the save file and return the last fetch timestamp
def read_last_fetch_timestamp():
    save_path = "details.sv"
    if os.path.exists(save_path):
        with open(save_path, "r") as save:
            save_data = json.load(save)
            last_fetch_timestamp = save_data.get("last_fetch_timestamp", "")
            return last_fetch_timestamp
    return None

# Function to write the last fetch timestamp to the save file
def write_to_file(input,mode):
    save_path = "details.sv"
    save_data = {}
    if os.path.exists(save_path):
        with open(save_path, "r") as save:
            save_data = json.load(save)
    save_data[mode] = input
    with open(save_path, "w") as save:
        json.dump(save_data, save, default = str)

def argumentAnalyser(arg,input):
    readSave()
    match arg:
        case "-f":
            download_random_wallpaper()
            write_to_file(datetime.now(),"last_fetch_timestamp")
        case "-c":
            download_random_wallpaper()
            write_to_file(input,"Collection")
        case "-config":
            os.system("nano details.sv")
        case "-a":
            download_random_wallpaper()
            write_to_file(input,"APIKEY")
        case "-h":
            download_random_wallpaper()
            write_to_file(input,"Hdir")

def handle_error(errorType,message):
    print(f"Failed to {message}. Status code: {errorType}")

def runApp():
    readSave()
    last_fetch_timestamp = read_last_fetch_timestamp()
    
    # If there's no last fetch timestamp or a week has passed, fetch a new wallpaper
    if len(last_fetch_timestamp) == 0:
        download_random_wallpaper()
        write_to_file(datetime.now(),"last_fetch_timestamp")
    elif ((datetime.now() - last_fetch_timestamp) >= timedelta(days=7)):
        download_random_wallpaper()
        write_to_file(datetime.now(),"last_fetch_timestamp")


def helperRun():
    match len(sys.argv):        
        case 1:
            runApp()
        case 2:
            if sys.argv[1] in ["-f","-config"]:
                argumentAnalyser(sys.argv[1], "")
            elif (sys.argv[1] not in ["-c","-a","-h"]):
                handle_error(1, "read flag, flag does not exist")
            else:
                handle_error(2, "read flag, flag is used in the wrong place")
        case 3:
            if (sys.argv[1] not in ["-c","-a","-h"]):
                handle_error(2, "read flag, flag does not exist or is used in the wrong way")
            elif(sys.argv[1] in ["-c","-a","-h"]):
                argumentAnalyser(sys.argv[1],sys.argv[2])
            else:
                handle_error(1, "read flag, flag does not exist")
        case _:
            handle_error(1, "read flag, flag does not exist")

if __name__ == '__main__':
    # Your main code here

    # Wrap your runApp() call in a function to run as a background process
    def background_task():
        helperRun()
        print("ruuning in bg")

    background_process = multiprocessing.Process(target=background_task)
    background_process.daemon = True  # This makes the process run in the background.
    background_process.start()

    # The main application can continue running or simply wait in this loop.
    while True:
        pass

