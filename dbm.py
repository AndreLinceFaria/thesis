import utils.file_utils as fs
from settings import *

files_dir = join(BASE_DIR,'database/')
filename = join(BASE_DIR,'database.sqlite')

def create_db():
    if os.path.exists(files_dir):
        fs.join(fromdir=files_dir, tofile=filename,zip = False)
        return True
    return False

def clear_db():
    if not os.path.exists(files_dir):
        fs.split(fromfile=filename, todir=files_dir, zip=False)

if __name__ == "__main__":
    if not create_db():
        clear_db()


