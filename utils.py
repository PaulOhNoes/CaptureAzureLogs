import os
from datetime import datetime
from constants import last_checked_path, logs_directory_path

def sorter(string):
  try:
    iso_timestamp = string[0:28] 
    return datetime.fromisoformat(iso_timestamp).timestamp()
  except:
    return 0 

def sort_log_lines(lines):
  return sorted(lines, key=sorter)

def sort_log(string):
  date = string[0:10] 
  section = 0 

  if(string[-5].isnumeric()): 
    section = int(string[-5])

  return datetime.strptime(date, '%Y_%m_%d').timestamp() + section

def get_all_dates(filenames):
  dates = set()

  for file in filenames:
    dates.add(file[0:10])

  dates = sorted(dates, key=sort_log)
  dates.reverse()

  return dates

def get_last_checked_date():
  if(not os.path.exists(last_checked_path)):
    open(last_checked_path, "x").close()
  
  with open(last_checked_path, "r") as file:
      return file.readline()

def filter_files(filenames):
  last_checked_date = get_last_checked_date()
  sorted_files = sorted(filenames, key=sort_log)
  sorted_files.reverse()
  file_list = []

  for file in sorted_files:
    if(last_checked_date == file[0:10]):
      break
    else:
      file_list.append(file)
  
  return file_list

def delete_incomplete_logs(filenames):
  last_checked_date = get_last_checked_date()
  incomplete_logs = get_all_dates(filenames)

  if(last_checked_date != ""):
    for file in incomplete_logs:
      try:
        os.remove(os.path.join(logs_directory_path, f"{file}.log"))
      except:
        print(f"Could not delete incomplete {file}.log")

def stamp_last_checked(filenames):
  last_checked_date = get_last_checked_date()
  with open(last_checked_path, "w") as file:
    try:
      # update file with the 2nd day before
      file.write(get_all_dates(filenames)[2])
    except IndexError:
      file.write(last_checked_date)

    file.truncate()