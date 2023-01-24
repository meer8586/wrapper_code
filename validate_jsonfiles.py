#Validate json format for workload

import pandas as pd
import json

def validate_workload_file(json_file_path: str) -> bool:

  if json_file_path.endswith('.json'):
    print('it is a json file')

    try:

      demo_list = ['timestamp', 'identity', 'os_release', 'lscpu', 'cpu_total', 'proc_meminfo', 'disks', 'networks']

      df = pd.read_json(json_file_path,nrows=1,lines=True)

      col_list = list(df)

      if any(x in demo_list for x in col_list):
        print('Loaded file is a valid json format')
      else:
        print('loaded file is not valid match')
        print(col_list)
        # If we reach this point, the JSON file is valid
    except Exception as e:
       print(e,"Please load valid json file")
  else:
    print('its not json file')

#for platform profiler file

def validate_platform_file(json_file_path2: str) -> bool:


    if json_file_path2.endswith('.json'):

        print('it is a json file')

        try:

            demo_list2 = ['Chassis']

            df = pd.read_json(json_file_path2)#nrows=1,lines=True

            col_list2 = list(df)



            if any(x in demo_list2 for x in col_list2):
                print('Loaded file is a valid json format')
            else:
                print('loaded file is not valid match')
                print(col_list2)
        # If we reach this point, the JSON file is valid
        except Exception as e:
        # If we catch a JSONDecodeError, the JSON file is not valid
            print(e,"Please load valid json file")
    else:
        print('its not json file')

validate_workload_file("/home/rio/project/wrapper_20230119_050903/WorkloadProfile.json")
