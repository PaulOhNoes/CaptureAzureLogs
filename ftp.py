import ftplib
import os
from constants import logs_directory_path, hostname, password, username

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
    for file in filenames:
      try:
        print("Downloading " + file)

        # download azure logs
        with open(os.path.join(logs_directory_path, file), "wb") as f:
          self.ftp.retrbinary('RETR ' + file, f.write)

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
      
      finally:
        # delete downloaded azure log
        os.remove(os.path.join(logs_directory_path, file))
  
  def close(self):
    self.ftp.quit()
    print("Connection closed.")
