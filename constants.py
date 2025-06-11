import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env

hostname = []
username = []
password = []

if(os.getenv("hostname")):
  hostname = os.getenv("hostname").split(";")
else:
  raise ValueError("Missing ftp hostname(s).")

if(os.getenv("username")):
  username = os.getenv("username").split(";")
else:
  raise ValueError("Missing ftp username(s).")

if(os.getenv("password")):
  password = os.getenv("password").split(";")
else:
  raise ValueError("Missing ftp password(s).")


if(len(hostname) != len(username) or len(hostname) != len(password)):
  raise ValueError(f"Found only {len(hostname)} hostname{'s' if len(hostname) > 1 else ''} "
                  f"but only {len(username)} username{'s' if len(username) > 1 else ''} "
                  f"and {len(password)} password{'s' if len(password) > 1 else ''}. "
                  "The number of usernames and passwords must match the number of hostnames.")

path = os.getenv("path") or "logs"
logs_directory_path = os.path.join(os.getcwd(), path)
last_checked_path = os.path.join(logs_directory_path, "last_check.txt")

