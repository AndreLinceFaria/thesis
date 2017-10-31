import pickle

def load_model(filename):
    fname = filename + ".pk"
    print("Loading model from: " + fname)
    with open(fname, 'rb') as f:
        model = pickle.load(f)
    return model

def save_model(model, filename):
    print("Saving model to: " + filename + ".pk")
    with open(filename + ".pk", 'wb') as f:
        pickle.dump(model, f)