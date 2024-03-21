import os
from datetime import datetime

print("start test script")

def make_log(date): 
  newlog = open(f"newlogs/{date}.log", "w")
  newlog.close()

def sort_log(string):
  date = string[0:10] 
  section = 0 

  if(string[-5].isnumeric()): 
    section = int(string[-5])

  return datetime.strptime(date, '%Y_%m_%d').timestamp() + section

logs_dir_parth = os.path.join(os.getcwd(), "logs")
logs_dir = os.listdir(logs_dir_parth)
logs_dir.sort(key=sort_log, reverse=True)

for log in logs_dir:
  print(log)

for filename in logs_dir:
  new_logs_dir_path = os.path.join(os.getcwd(), "newlogs")
  new_log_file_path = os.path.join(new_logs_dir_path, f"{filename[0:10]}.log")
  if(not os.path.exists(new_log_file_path)):
    file = open(new_log_file_path, "x")
    file.close()
  
  log = open(new_log_file_path, "a")

  with open(os.path.join(logs_dir_parth, filename), "r") as file:
    log.write(f"--- merging {filename} ---\n")
    log.writelines(file.readlines())
    file.close()

  log.close()

print("end script")