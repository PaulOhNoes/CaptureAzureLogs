import os
import ftplib
from datetime import datetime
from dotenv import load_dotenv
from utils import get_latest_files, get_all_dates

load_dotenv()  # take environment variables from .env

# Credentials
hostname = os.getenv("hostname")
username = os.getenv("username")
password = os.getenv("password")

print("username", username)

filenames = []
logs_directory_path = os.path.join(os.getcwd(), "logs")
last_checked_path = os.path.join(logs_directory_path, "last_check.txt")
last_checked_date = ""

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

print("Script ran at", dt_string)
print("Log directory", logs_directory_path)


# Make logs directory if it does not exist
if(not os.path.exists(logs_directory_path)):
  os.mkdir(logs_directory_path)

# Make last_check.txt if it does not exist
if(not os.path.exists(last_checked_path)):
  open(last_checked_path, "x").close()

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

# get last date checked
with open(last_checked_path, "r") as file:
  last_checked_date = file.readline()

filenames = get_latest_files(filenames, last_checked_date)

# delete incomplete logs
incomplete_logs = get_all_dates(filenames)

if(last_checked_date is not None and last_checked_date != ""):
  for file in incomplete_logs:
    try:
      os.remove(os.path.join(logs_directory_path, f"{file}.log"))
    except Exception as error:
      print(f"Could not delete incomplete {file}.log")

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

# stamp with the day before
with open(last_checked_path, "w") as file:
  try:
    file.write(get_all_dates(filenames)[1])
  except IndexError:
    file.write(last_checked_date)

  file.truncate()

# Close connection
ftp.quit()
print("Connection closed.")