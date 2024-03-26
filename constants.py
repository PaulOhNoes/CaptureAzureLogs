import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env

hostname = os.getenv("hostname")
username = os.getenv("username")
password = os.getenv("password")
path = os.getenv("path") or "logs"
logs_directory_path = os.path.join(os.getcwd(), path)
last_checked_path = os.path.join(logs_directory_path, "last_check.txt")

