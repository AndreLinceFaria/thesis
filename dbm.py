import utils.file_utils as fs
from settings import *

files_dir = join(BASE_DIR,'database/')
filename = join(BASE_DIR,'database.sqlite')

if os.path.exists(files_dir):
    fs.join(fromdir=files_dir, tofile=filename,zip = False)
else:
    fs.split(fromfile=filename, todir=files_dir, zip = False)