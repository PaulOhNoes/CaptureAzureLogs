import os
import ftplib
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.

# Credentials
hostname = os.getenv("hostname")
username = os.getenv("username")
password = os.getenv("password")

print("username", username)

filenames = []
logs_directory = os.path.join(os.getcwd(), "logs")

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

print("Script ran at", dt_string)
print("Log directory", logs_directory)

# Create ftp instance
ftp = ftplib.FTP(hostname)
ftp.login(username, password)

print(ftp.getwelcome(), "connected!")

# Change directory
ftp.cwd("/LogFiles")

# Append filenames 
for line in ftp.nlst():
  if(".log" in line and not "default" in line):
    filenames.append(line)

# Make logs directory if it does not exist
if(not os.path.exists(logs_directory)):
  os.mkdir(logs_directory)

# Download files
for line in filenames:
  try:
    print("Downloading " + line)
    with open(os.path.join(logs_directory, line), "wb") as f:
      ftp.retrbinary('RETR ' + line, f.write)
  except Exception as error:
    print(error)

# Close connection
ftp.quit()
print("Connection closed.")