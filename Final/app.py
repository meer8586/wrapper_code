import shutil
import os
import wrapper_utils
import datetime


try:
    #path = os.path.join(os.getcwd())
    input_path = "./"
    path = os.path.join(input_path)
    date_time1=str(datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
    newfilename1 = "wrapper_"+date_time1
    
    output_path = os.path.join(path, newfilename1)
    print(output_path)    
    if not os.path.exists(output_path):
        os.mkdir(output_path)
        print(output_path + " folder created.")

    else:
        print(output_path + " folder already exists.")

    #output_path = "./wrapper"
    wrapper_utils.data_collector(path,output_path)
    wrapper_utils.rename_workloadfile(output_path)
    wrapper_utils.nativePlatformDetails(output_path)

    wrapper_utils.tarCreation(output_path)

except Exception as e:
    print(e,'exception occured')


