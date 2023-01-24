import os

pod_name = os.popen("kubectl get pods --sort-by=.metadata.creationTimestamp -o jsonpath='{.items[-1].metadata.name}'").read()

print(pod_name)

file_extension =".tar.gz"
files = os.popen("kubectl exec "+pod_name+" -- ls").read().split("\n")

for file in files:
        if file.endswith(file_extension):
            os.system("kubectl cp "+pod_name+":"+file+" "+file)
            print(file+" Copied Successfully")
            break

