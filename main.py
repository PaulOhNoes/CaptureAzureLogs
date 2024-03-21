import os
import ftplib
from datetime import datetime
from dotenv import load_dotenv
from utils import sort_log

load_dotenv()  # take environment variables from .env.

# Credentials
hostname = os.getenv("hostname")
username = os.getenv("username")
password = os.getenv("password")

print("username", username)

filenames = []
logs_directory_path = os.path.join(os.getcwd(), "logs")

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

print("Script ran at", dt_string)
print("Log directory", logs_directory_path)

# Create ftp instance
ftp = ftplib.FTP(hostname)
ftp.login(username, password)

print(ftp.getwelcome(), "connected!")

# Change directory
ftp.cwd("/LogFiles")

# Append filenames 
for file in ftp.nlst():
  if(".log" in file and "default_docker" in file):
    filenames.append(file)

# sort logs by the date and section in descending order
filenames.sort(key=sort_log, reverse=True)

# Make logs directory if it does not exist
if(not os.path.exists(logs_directory_path)):
  os.mkdir(logs_directory_path)

# Download files and squash them into a new log file
for file in filenames:
  try:
    print("Downloading " + file)

    # download azure logs
    with open(os.path.join(logs_directory_path, file), "wb") as f:
      ftp.retrbinary('RETR ' + file, f.write)

    new_log_file_path = os.path.join(logs_directory_path, f"{file[0:10]}.log")
    
    # create new log file
    if(not os.path.exists(new_log_file_path)):
      open(new_log_file_path, "x").close()
    
    # append azure logs into new log file
    with open(new_log_file_path, "a") as log:
      with open(os.path.join("logs", file), "r") as azure_log:
        log.write(f"--- merging {file} ---\n")
        log.writelines(azure_log.readlines())

  except Exception as error:
    print("Error: ", error)


# Delete azure logs
for file in filenames:
    os.remove(os.path.join(logs_directory_path, file))

# Close connection
ftp.quit()
print("Connection closed.")