import data.utils.fsplitter as fs

import os


base_dir = str(os.path.dirname(os.path.realpath(__file__)))
files_dir = str(str(base_dir) + '\database')
filename = str(str(base_dir) + '\database.sqlite')

print("Base Dir: " + str(base_dir))
print("Files Dir: " + str(files_dir))
print("Filename: " + str(filename))

if os.path.exists(files_dir):
    fs.join(fromdir=files_dir, tofile=filename,zip = False)
else:
    fs.split(fromfile=filename, todir=files_dir, zip = False)