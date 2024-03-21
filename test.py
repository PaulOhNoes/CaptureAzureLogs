import os
from datetime import datetime

def make_log(date): 
  newlog = open(f"testLogs/{date}.log", "w")
  newlog.close()

def sort_log(string):
  date = string[0:10] 
  section = 0 

  if(string[-5].isnumeric()): 
    section = int(string[-5])

  return datetime.strptime(date, '%Y_%m_%d').timestamp() + section

def main():
  logs_dir_path = os.path.join(os.getcwd(), "logs")
  logs_dir = os.listdir(logs_dir_path)
  logs_dir.sort(key=sort_log, reverse=True)

  test_logs_dir_path = os.path.join(os.getcwd(), "testlogs")

  # Make testlogs directory if it does not exist
  if(not os.path.exists(test_logs_dir_path)):
    os.mkdir(test_logs_dir_path)

  for filename in logs_dir:
    new_log_file_path = os.path.join(test_logs_dir_path, f"{filename[0:10]}.log")
    if(not os.path.exists(new_log_file_path)):
      file = open(new_log_file_path, "x")
      file.close()
    
    log = open(new_log_file_path, "a")

    with open(os.path.join(logs_dir_path, filename), "r") as file:
      log.write(f"--- merging {filename} ---\n")
      log.writelines(file.readlines())
      file.close()

    log.close()

print("start test script")
main()
print("end test script")