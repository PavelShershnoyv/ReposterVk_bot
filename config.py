from dotenv import load_dotenv
import os


load_dotenv()
AUTHORIZATION_LINK = os.getenv('AUTHORIZATION_LINK')
BOT_TOKEN = os.getenv('BOT_TOKEN')
REDIRECT_URI = os.getenv('REDIRECT_URI')
VK_API_VERSION = os.getenv('VK_API_VERSION')
