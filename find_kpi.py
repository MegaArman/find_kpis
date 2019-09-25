#!/usr/bin/python3
import sys, getopt, csv, statistics, datetime
from decimal import Decimal

def help_message():
   print('usage: find_kpi.py --kpi_list <comma delimited list of kpis> --start <start date of time period> --stop <stop date of the time period>')
   print('example: python3 find_kpi.py --kpi_list occupancy,light,co2 --start "2/2/12" --stop "2/3/12"')

# dates in form "2/2/12"
def in_date_range(start, stop, test): 
   start = start.split('/') 
   stop  = stop.split('/')
   test  = test.split('/')

   start = list(map(int, start))
   stop = list(map(int, stop))
   test = list(map(int, test))

   start_date = datetime.date(start[2], start[0], start[1])
   stop_date = datetime.date(stop[2], stop[0], stop[1])
   test_date = datetime.date(test[2], test[0], test[1])

   return (test >= start and test <= stop)

def find_kpis(kpi_list, start, stop): 
  # Please see README.txt !
  reader = csv.reader(open('example.csv')) 
  keys = next(reader)
  keys = list(map(lambda x: x.lower(), keys)) 
  data = {}
  result = {} 

  for key in keys:
    data[key] = []

  # NOTE: this assumes date is the first column
  # convert the csv structure into a dictionary of lists:  {"occupancy" : [...], "light": [...]}
  for row in reader:
    if len(row) > 0:
      current_date = row[0].split(' ')[0] # remove time from date time
      
      # hold only values only for dates specified
      if (in_date_range(start, stop, current_date)):
        for key_num in range (1, len(keys)):
          current_key = keys[key_num]
          val = Decimal(row[key_num])
          data[current_key].append(val)

  # create the output
  for kpi in kpi_list:
    result[kpi] = {'percent_change': '' ,'average': -1, 'median': -1}
    first_val = data[kpi][0]
    last_val = data[kpi][len(data[kpi]) - 1]
    result[kpi]['percent_change'] = '{0:.4f}'.format((last_val - first_val) / first_val * 100) + '%'
    result[kpi]['average'] = '{0:.4f}'.format(statistics.mean(data[kpi]))
    result[kpi]['median'] = '{0:.4f}'.format(statistics.median(data[kpi]))
  
  return result 

def main(argv):
  kpi_list = ''
  start = ''
  stop = ''

  try:
    opts, args = getopt.getopt(argv, 'h',['kpi_list=', 'start=', 'stop='])
  except getopt.GetoptError:
    help_message()
    sys.exit()
 
  for opt, arg in opts:
    if opt == '-h':
      help_message()
      sys.exit()
    elif opt == '--kpi_list':
      kpi_list = arg.split(',')
    elif opt == '--start':
       start = arg
    elif opt == '--stop':
      stop = arg
  
  results = find_kpis(kpi_list, start, stop)
  # the following line shows the find_kpis function signature is in check:
  #results = find_kpis(kpi_list=["light", "occupancy"], start="2/2/12", stop="2/3/12")
  print('results:', results)

if __name__ == '__main__':
  main(sys.argv[1:])
 
