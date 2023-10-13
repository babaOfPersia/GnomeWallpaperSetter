#!/usr/bin/env python3

import requests
import os
import json
import random
from datetime import datetime, timedelta

# Get the user's home directory

home_dir = os.path.expanduser('~')
if(home_dir == '/root'):
    home_dir = '/home/kamyar'

# Directory to store downloaded wallpapers
WALLPAPER_DIR = home_dir+'/Pictures/Wallpapers'

def readSave():
    save = open("details.sv", "r")
    saveJson = json.loads(save.readline())
    # Set your Unsplash API key
    global UNSPLASH_API_KEY
    global COLLECTION_CODE
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
            print(f"Failed to download the image from Unsplash. Status code: {response.status_code}")
    else:
        print(f"Failed to fetch a random image from Unsplash. Status code: {response.status_code}")

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
def write_last_fetch_timestamp(timestamp):
    save_path = "details.sv"
    save_data = {}
    if os.path.exists(save_path):
        with open(save_path, "r") as save:
            save_data = json.load(save)
    save_data["last_fetch_timestamp"] = timestamp
    with open(save_path, "w") as save:
        json.dump(save_data, save, default = str)


if __name__ == '__main__':
    readSave()
    last_fetch_timestamp = read_last_fetch_timestamp()
    
    # If there's no last fetch timestamp or a week has passed, fetch a new wallpaper
    if last_fetch_timestamp is "":
        download_random_wallpaper()
        write_last_fetch_timestamp(datetime.now())
    elif ((datetime.now() - last_fetch_timestamp) >= timedelta(days=7)):
        download_random_wallpaper()
        write_last_fetch_timestamp(datetime.now())
        
    
