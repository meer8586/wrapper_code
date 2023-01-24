import shutil
import os
import wrapper_utils
import datetime
import time
import stat
import sys

try:
    #path = os.path.join(os.getcwd())
    input_path = "./"
    path = os.path.join(input_path)
    date_time1=str(datetime.datetime.now().strftime("%Y%m%d_%H%M%S"))
    newfilename1 = "wrapper_"+date_time1
    
    output_path = os.path.join(path, newfilename1)
    print(output_path)    
    #if not os.path.exists(output_path):
    os.mkdir(output_path)
    print(output_path + " folder created.")
    os.chmod(output_path, stat.S_IRWXU)
    #else:
        #print(output_path + " folder already exists.")

    #output_path = "./wrapper"
    wrapper_utils.data_collector(path,output_path)
    wrapper_utils.rename_workloadfile(output_path)
    wrapper_utils.nativePlatformDetails(output_path)

    wrapper_utils.tarCreation(output_path)
    #time.sleep(120)
    #wrapper_utils.getTar()
except Exception as e:
    print(e,'exception occured')


