import os

file_names = os.listdir(os.path.curdir + "/Files")
print(os.path)
print(os.path.curdir)

print(os.listdir(os.path.curdir + "/Files"))

for file in os.path.curdir:
    print(file)
    file_names.append(file)