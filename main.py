import os
from datetime import datetime
from utils import stamp_last_checked, get_last_checked_date, sort_log_lines
from ftp import FTP
from constants import username, hostname, password,logs_directory_path

def main():
  logs_by_days = {}
  last_checked_date = get_last_checked_date()

  # loop through each ftp server and populate logs by days
  for i in range(len(hostname)):
    client = FTP(hostname[i], username[i], password[i])
    client.init()
    client.cwd("/LogFiles")
    client.get_logs(logs_by_days, last_checked_date)
    client.close()

  # loop through each day and create the log file
  for date in logs_by_days:
    deduped_log_lines = list(set(logs_by_days[date]))
    sorted_log_lines = sort_log_lines(deduped_log_lines)
    
    new_log_file_path = os.path.join(logs_directory_path, f"{date}.log")

    # create or replace the old log file
    with open (new_log_file_path, "w") as file:
      file.writelines(sorted_log_lines)

  if(len(list(logs_by_days.keys())) == 0):
    print("No log files created. Last checked date will not be updated.")
  else:
    stamp_last_checked()

if __name__ == "__main__":
  now = datetime.now()
  dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

  print("CaptureAzureLogs - release/4.0.1")
  print("Script ran at", dt_string)
  main()
  print("Script successful!")