import os
import json
import pandas as pd
import datetime
import subprocess
import time
import glob
from tqdm import tqdm
import tarfile
import shutil
import sys

#----------------------------------nativePlatformProfilier-----------------------------------



def installation():
    os.system("sudo apt update")
    os.system("sudo apt install python3-pip")
    os.system("sudo pip3 install -e .")

def njmon_installation():
    os.system("sudo apt install unzip")
    os.system("sudo wget http://sourceforge.net/projects/nmon/files/njmon_linux_binaries_v71.zip -P workload_profiler/")
    os.system("sudo unzip workload_profiler/njmon_linux_binaries_v71.zip -d workload_profiler/installation_files")
    os.system("sudo chmod u+x workload_profiler/installation_files/ninstall")
    os.chdir("workload_profiler/installation_files")
    os.system("sudo ./ninstall njmon_Ubuntu20_x86_64_v71")

def njmon_collect(output_path,count):
    os.chdir(output_path)
    print(os.getcwd())
    os.system("njmon -s 5 -c "+count+" -m . -f WorkloadProfile.json")
    os.chdir("..")
def nativePlatformDetails(output_path):

    core = os.popen(" lscpu | grep 'Core(s) per socket' | cut -f 2 -d ':' | awk '{$1=$1}1'").read()
    model_name = os.popen("lscpu | grep 'Model name' | cut -f 2 -d ':' | awk '{$1=$1}1'").read()
    Vcpu_count = os.popen("lscpu | grep 'On-line' | cut -f 2 -d ':' | awk '{$1=$1}1'").read()

    mem_max = os.popen(" vmstat -s |grep 'total memory'| awk '{$1=$1/(1024^2); print $1}'").read()
    mem_max1=float(mem_max)
    mem_max2=str(round(mem_max1,1))+"GB"
    mem_max2=mem_max2.replace(".","_")

    disk_capacity = getTotalDiskSize()

    nettype = os.popen('ls /sys/class/net').read()

    nettype = list(nettype.split())

    native_platform_name = model_name.replace(" ","").strip()+str(Vcpu_count).strip()+"c"+str(mem_max2).strip()+disk_capacity.strip()

    timestamp=str(datetime.datetime.now().strftime("%d%m%Y%H%M%S"))

    native_platform_id = native_platform_name + timestamp

#making Dictionary of all Commands    
    nativeplatformdetails = {
        "nativePlatformID" : native_platform_id,
        "nativePlatformName" : native_platform_name,
        "cores" : core.strip(),
        "model_name" : model_name.strip(),
        "vcpu_count" : str(Vcpu_count).strip(),
        "mem_max" : mem_max2.strip(),
        "disk_capacity" : disk_capacity.strip(),
        "net_type" : nettype
        }

 #Creating json file of the dictionary
    native_path= os.path.join(output_path,"nativePlatformDetails.json")
    with open(native_path,'w') as outfile:
        json.dump(nativeplatformdetails,outfile)
        print("native platform json file created")


def getDiskSize():
    os.system('lsblk --json > lsblk.json')

    with open('lsblk.json', 'r') as f:
        demo= json.load(f)
        df = pd.DataFrame(demo)
        name, size = [], []


    if (df['blockdevices'].count() > 0):
        for i in range(df['blockdevices'].count()):
            if(df['blockdevices'][i]['type'] == 'disk'):
                name.append(df[ 'blockdevices' ][i]['name'])
                size.append(df[ 'blockdevices' ][i]['size'])
    

    for i in size:
        if 'G' in i:
            index= size. index(i)
            i = i.translate({ord('G'): None})
            i = float(i)
            i = str(round(i, 1)) + "G"
            size[index] = i

    df2 = pd.DataFrame()
    df2['name'] = [i for i in name]
    df2['size'] = [i for i in size]

    
    json_rec = json.dumps (json.loads(df2.to_json(orient="records")))

    os.remove('lsblk.json')
    return json_rec


def getTotalDiskSize():
    size = []
    demo2 = getDiskSize()
    df = pd.read_json(demo2)
   

    for i in list(df['size']):
        i=i.translate({ord('G'): None})
        size.append(float(i))

    totalSize = str(round(sum(size), 4))+'g'
    totalSize = totalSize.replace(".", "_")
    
    
    return totalSize
#Renaming the workload profiler file and removing the .err file
def rename_workloadfile(output_path):
    file_extension = ".err"
    files = os.listdir(output_path)
    #date_time=str(datetime.datetime.now().strftime("%d%m%Y%H%M%S"))
    newfilename = "WorkloadProfile.json"
    #removing .err file
    for file in files:
        if file.endswith(file_extension):
            os.remove(os.path.join(output_path,file))
            break
    #renaming the workload file
    list_of_Files = glob.glob(output_path + "/*.json")    
    latest_file = max(list_of_Files, key = os.path.getctime)
    path, old_filename = os.path.split (latest_file)
    if not old_filename.startswith("Workload"):
        new_file = os.path.join(path, newfilename)
        os.rename (latest_file, new_file)

#Collecting data using  njomn
def data_collector(path,output_path):

    
    if not os.path.isfile("/usr/local/bin/njmon"):
        print("NJMON is installing...")
        time.sleep(1)
        #subprocess.call(["bash","./njmon_installation.sh"])
        njmon_installation()
        print("NJMON is intalled")
        os.system("njmon -@")
    
    else:
        print("NJMON is already installed")
        os.system("njmon -@")

    #Adding platform profiler file
    pattern = path + "/PlatformProfile" + ".json"
    #print(pattern)
    result = glob.glob(pattern)
    #print(result)
    for fname in result:
        shutil.copy2(os.path.join(path,fname), output_path)


    #count = sys.argv[1]
    count = input("Enter number of Count : ")
    #pro = subprocess.call(["bash",'./njmon_collect.sh',count])
    njmon_collect(output_path,count)
    print
    print("Collecting Data ...")
    #Adding Progress Bar
    
    for i in tqdm (range (100),
            desc="Loading…",
            ascii=False):
        count1 = (5*int(count)/100)
        time.sleep(count1)
        
    time.sleep(count1)
    print("Data Collected")

#creating tar file from wrapper dir
def tarCreation(output_path):
    output_filename = output_path + ".tar.gz"
    tar = tarfile.open(output_filename, "w:gz")
    tar.add(output_path)
    tar.close()
    print("Tar file created successfully")

