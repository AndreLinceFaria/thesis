import pickle
import os, re

def load_model(filename, load_literal=False):
    files = get_files_from_dir(filename)
    if len(files[0]) > 0:
        fname = os.path.join(files[1], files[0][len(files)-1])
        print("Loading model from: " + files[0][len(files[0])-1])
        with open(fname, 'rb') as f:
            model = pickle.load(f)
        return model
    return None

def save_model(model, filename, save_literal=False):
    files = get_files_from_dir(filename)
    fname = filename + "-" + str(len(files[0])) + ".pk"
    print("Saving model to: " + fname)
    with open(fname, 'wb') as f:
        pickle.dump(model, f)

def get_files_from_dir(filename):
        path, file = os.path.split(filename)
        match = "\S*(" + file + "-)(\d+)(.pk|.xlsx)"
        pt = re.compile(match)
        files = [f for f in os.listdir(path) if re.match(pt, f)]
        files.sort()
        return files,path