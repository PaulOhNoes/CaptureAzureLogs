from datetime import datetime

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

def get_latest_files(filenames, date):
  sorted_files = sorted(filenames, key=sort_log)
  sorted_files.reverse()
  file_list = []

  for file in sorted_files:
    if(date == file[0:10]):
      break
    else:
      file_list.append(file)
  
  return file_list