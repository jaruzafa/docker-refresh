import sys
import configparser
import os.path
from datetime import *
import docker

refresh_interval = None
images_to_refresh = None
REFRESH_DATE_FILE = "lastrefresh.txt"

def read_last_refresh_date():
    if os.path.exists(REFRESH_DATE_FILE):
        f = open(REFRESH_DATE_FILE, "r")
        last_refresh = date.fromisoformat(f.readline())
        f.close()
        return last_refresh
    else:
        #If lastrefresh.txt doesn't exist, assume that it has never refreshed anything. Set a date in a distant past...
        return date.fromisoformat("2000-01-01")

def update_last_refresh_date():
    f = open(REFRESH_DATE_FILE, "w")
    f.writelines(date.today().isoformat())
    f.close()

def read_configuration():
    global refresh_interval
    global images_to_refresh
    config = configparser.ConfigParser()
    config.read('settings.ini')
    refresh_interval = int(config['default']['refresh_interval_days'])
    images_to_refresh = config['default']['images_to_refresh'].split(",")

def is_time_for_a_refresh():
    last_refresh = read_last_refresh_date()
    if date.today() >= last_refresh + timedelta(days = refresh_interval) :
        return True
    else: 
        return False

def refresh_images():
    print("Refreshing docker images, go go go...")

    client = docker.from_env()
    try:
        client.ping()
    except:
        print("Error: Whooops! is the docker daemon running?")
        return

    try:
        for image in images_to_refresh:
            print("Pulling " + image)
            client.images.pull(image)
        update_last_refresh_date()      
    except docker.errors.APIError as error:
        print("Error: ", format(error))
    except:
        raise

read_configuration()
if is_time_for_a_refresh():
    print("It's time for a refresh")
    refresh_images()
else:
    print("Images are not refreshed today")
