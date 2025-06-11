import os
from datetime import datetime, date, timedelta
from constants import last_checked_path

def sorter(string):
  try:
    iso_timestamp = string[0:28] 
    return datetime.fromisoformat(iso_timestamp).timestamp()
  except:
    return 0 

def sort_log_lines(lines):
  return sorted(lines, key=sorter)


def get_last_checked_date():
  if(not os.path.exists(last_checked_path)):
    open(last_checked_path, "x").close()
  
  with open(last_checked_path, "r") as file:
      return file.readline()

def stamp_last_checked():
  # stamp the day before because a process could hold a log file for a whole day
  yesterday = (date.today()-timedelta(days=1)).strftime("%Y_%m_%d")
  
  try: 
    with open (last_checked_path, "w") as file:
      file.write(yesterday)
  except Exception as error:
      print("An unexpected error occurred during stamping the last checked date: ", error)