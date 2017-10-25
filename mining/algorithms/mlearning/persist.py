import pickle

def load_model(filename):
    print("Loading model from: " + filename + ".pk")
    with open(filename + ".pk", 'rb') as f:
        model = pickle.load(f)
    return model

def save_model(model, filename):
    print("Saving model to: " + filename + ".pk")
    with open(filename + ".pk", 'wb') as f:
        pickle.dump(model, f)