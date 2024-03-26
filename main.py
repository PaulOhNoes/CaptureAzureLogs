import os
from datetime import datetime
from utils import filter_files, delete_incomplete_logs, stamp_last_checked
from ftp import FTP
from constants import logs_directory_path

def main():
  print("Log directory", logs_directory_path)
  client = FTP()
  client.init()
  client.cwd("/LogFiles")

  filenames = filter_files(client.get_log_list())
  
  # Make logs directory if it does not exist
  if(not os.path.exists(logs_directory_path)):
    os.mkdir(logs_directory_path)

  delete_incomplete_logs(filenames)
  client.generate_logs(filenames)
  stamp_last_checked(filenames)
  client.close()

if __name__ == "__main__":
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

  print("Script ran at", dt_string)
  main()
  print("Script successful!")