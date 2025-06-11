import ftplib
from datetime import date
import os
from constants import logs_directory_path

class FTP:
  def __init__(self, hostname, username, password):
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

  def get_logs(self, logs_by_days, last_checked_date):
    filenames = []

    # Append filenames. Filter files by last checked date
    for file in self.ftp.nlst():
      if(".log" in file and "default_docker" in file):
        if(last_checked_date):
          file_date = date(year=int(file[:4]), month=int(file[5:7]), day=int(file[8:10]))
          end_date = date(year=int(last_checked_date[:4]), month=int(last_checked_date[5:7]), day=int(last_checked_date[8:10])) if last_checked_date else None
          
          if(file_date > end_date):
            filenames.append(file)
        else:
          filenames.append(file)
    
    # Get log lines
    for filename in filenames:
        try:
          print("Downloading " + filename)

          # download azure logs
          with open(os.path.join(logs_directory_path, filename), "wb") as f:
            self.ftp.retrbinary('RETR ' + filename, f.write)

          # append azure log lines to logs_by_days by date
          with open(os.path.join("logs", filename), "r") as azure_log:
            log_date = filename[:10]

            if(log_date in logs_by_days):
              logs_by_days[log_date] = logs_by_days[log_date] + azure_log.readlines()
            else: 
              logs_by_days[log_date] = azure_log.readlines()
        
        except Exception as error:
            print("Error: ", error)
          
        finally:
            # delete downloaded azure log
            os.remove(os.path.join(logs_directory_path, filename))

  def get_log_list(self):
    logs = []
    
    for file in self.ftp.nlst():
      if(".log" in file and "default_docker" in file):
        logs.append(file)

    return logs
  
  def close(self):
    self.ftp.quit()
    print("Connection closed.")
