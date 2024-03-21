from datetime import datetime

def sort_log(string):
  date = string[0:10] 
  section = 0 

  if(string[-5].isnumeric()): 
    section = int(string[-5])

  return datetime.strptime(date, '%Y_%m_%d').timestamp() + section