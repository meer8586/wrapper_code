import subprocess
import os
import fnmatch
import shutil
# Get the ID of the latest running container
container_id = subprocess.run(["docker", "ps", "-qa"], capture_output=True, text=True).stdout.strip().split("\n")[0]

print("Latest container ID:", container_id)
#pattern = 'wrapper_.tar.gz'
#file_name = input("Enter the file name : ")

file_extension =".tar.gz"
files = os.popen('docker exec '+container_id+' ls').read().split("\n")
for file in files:
        if file.endswith(file_extension):
            os.system('docker cp '+container_id+':/'+file+' .')
            print(file+" Copied Successfully")
            break


