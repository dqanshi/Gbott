import json
import os


def get_user_list(config, key):
    with open("{}/Emilia/{}".format(os.getcwd(), config), "r") as json_file:
        return json.load(json_file)[key]


class Config(object):
    API_HASH = "b89d2ee79c70c5fbf9299e34f16e27e0" # API_HASH from my.telegram.org
    API_ID = 1207230 # API_ID from my.telegram.org

    BOT_ID = 1060722149 # BOT_ID
    BOT_USERNAME = "am_angel_bot" # BOT_USERNAME

    MONGO_DB_URL = "mongodb+srv://Dqanshi:an12if..@cluster0.awr1r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0" # MongoDB URL from MongoDB Atlas

    SUPPORT_CHAT = "dbots_supportchat" # Support Chat Username
    UPDATE_CHANNEL = "SpiralUpdates" # Update Channel Username
    START_PIC = "https://pic-bstarstatic.akamaized.net/ugc/9e98b6c8872450f3e8b19e0d0aca02deff02981f.jpg@1200w_630h_1e_1c_1f.webp" # Start Image
    DEV_USERS = [] # Dev Users
    TOKEN = "1060722149:AAGEWokvznyR4dHrau1LFVTHs2iN4x_thgg" # Bot Token from @BotFather
    CLONE_LIMIT = 1 # Number of clones your bot can make

    EVENT_LOGS =-1002423841190 # Event Logs Chat ID
    OWNER_ID = 820596651 # Owner ID
 
    TEMP_DOWNLOAD_DIRECTORY = "./" # Temporary Download Directory
    BOT_NAME = "ANGEL" # Bot Name
    WALL_API = "6950f53" # Wall API from wall.alphacoders.com
    ORIGINAL_EVENT_LOOP = True # Do not Change


class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
