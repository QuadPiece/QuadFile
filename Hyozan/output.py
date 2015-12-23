from datetime import datetime
import time

def print_log(source, message):
  if source == "Main":
    print('\033[92m' + source + ': \033[0m' + message)
  elif source == "Notice":
    print('\033[93m' + source + ': \033[0m' + message)
  elif source == "Warning":
    print('\033[91m' + source + ': \033[0m' + message)
  elif source == "Web":
    print('\033[95m' + source + ': \033[0m' + message)
  else:
    print('\033[94m' + source + ': \033[0m' + message)

def time_to_string(unixtime):
  return datetime.fromtimestamp(unixtime).strftime('%B %d, %Y (%H:%M - ' + time.tzname[time.daylight] + ')')
