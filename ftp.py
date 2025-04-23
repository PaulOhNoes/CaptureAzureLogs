import ftplib
from datetime import datetime
import os
from constants import logs_directory_path, hostname, password, username
from utils import sort_log_lines

class FTP:
  def __init__(self):
    self.hostname = hostname
    self.username = username
    self.password = password
    self.ftp = None

  def init(self):
    self.ftp = ftplib.FTP(self.hostname)
    self.ftp.login(self.username, self.password)

    print("Connecting with username: ", self.username)
    print(self.ftp.getwelcome(), "connected!")

  def cwd(self, path):
    self.ftp.cwd(path)

  def get_log_list(self):
    logs = []
    
    for file in self.ftp.nlst():
      if(".log" in file and "default_docker" in file):
        logs.append(file)

    return logs
  
  def generate_logs(self, filenames):
    files_by_days = {}

    for file in filenames:
      date = file[0:10]
      if( date in files_by_days):
        files_by_days[date].append(file)
      else:
        files_by_days[date] = [file]
    
    for date in files_by_days:
      log_lines = []

      new_log_file_path = os.path.join(logs_directory_path, f"{date}.log")
          
      # create new log file
      if(not os.path.exists(new_log_file_path)):
        open(new_log_file_path, "x").close()
      else:
        with open(new_log_file_path, "r+") as file:
          file.truncate(0)

      for filename in files_by_days[date]:
        try:
          print("Downloading " + filename)

          # download azure logs
          with open(os.path.join(logs_directory_path, filename), "wb") as f:
            self.ftp.retrbinary('RETR ' + filename, f.write)

          # append azure logs into new log file
          with open(os.path.join("logs", filename), "r") as azure_log:
            log_lines = log_lines + azure_log.readlines()
        
        except Exception as error:
          print("Error: ", error)
        
        finally:
          # delete downloaded azure log
          os.remove(os.path.join(logs_directory_path, filename))
          
      log_lines = sort_log_lines(log_lines)

      log_lines = [line for line in log_lines if line.strip() != ""]

      # populate log file
      with open(new_log_file_path, "a") as log:
        log.writelines(log_lines)

  def close(self):
    self.ftp.quit()
    print("Connection closed.")
