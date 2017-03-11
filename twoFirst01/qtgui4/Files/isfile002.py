import os, fnmatch
for file in os.listdir('.') :
    if fnmatch.fnmatch(file, '*.py') :
        print(file)