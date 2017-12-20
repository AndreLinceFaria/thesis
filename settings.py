import sys,os
sys.path.insert(0, str(os.path.realpath(__file__)))
import datetime

# ======================
# Functions
# ======================

def join(path1,path2):
    return str(os.path.join(path1,path2))

# ======================
# Files and Directories
# ======================

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DB = os.path.join(BASE_DIR,"database.sqlite")

CLASS_MODELS_DIR = os.path.join(BASE_DIR,"static/results/models/")

CLASS_LOGS_DIR = os.path.join(BASE_DIR,"static/results/logs/")

# === Figures ===

FIGURES_DIR = join(BASE_DIR,"static/results/figures/")

FIGURES_SAVE_AS_FORMAT = "[" + datetime.datetime.today().strftime('%Y-%m-%d %H-%M') + "].png"

# === Logs ===

PREDICT_LOG_FORMAT = 'predict-log[' + datetime.datetime.today().strftime('%Y-%m-%d') + '].log'
TRAIN_LOG_FORMAT = 'predict-log[' + datetime.datetime.today().strftime('%Y-%m-%d') + '].log'


# === Parsers & Configs ===

CONFIG_1_JSON = join(BASE_DIR,"static/config/parties-config/parties-config-1.json")
RESULTS_CSV =join(BASE_DIR,"static/config/autarquicas17-resultados.csv")
PARTIES_TWITTER_JSON = join(BASE_DIR,"static/config/parties-config/parties-twitter.json")

# ======================
# Algorithms
# ======================

# === RAKE ===

REGEX_FILE = join(BASE_DIR,"static/config/rake/regex.txt")
STOPWORDS_FILE = join(BASE_DIR,"static/config/rake/stopwords-pt.txt")

# === KNN ===

KNN_NAME = "K-Nearest Neighbours"

KNN_NEIGHBOURS_COUNT = 25


# === NBayes ===

NB_NAME = "Naive Bayes"

# === NNet ===

NN_NAME = "Multi-Layer Perceptron"
NN_SOLVER = 'lbfgs'
NN_ALPHA = 1e-5
NN_HIDDEN_LAYERS_SIZE = (5,2)
NN_RANDOM_STATE = 0

# === SVM ===

SVM_NAME = "Support Vector Machine"
SVM_SVC_RANDOM_STATE = 0
SVM_SVC_KERNEL = 'rbf'
SVM_NEIGHBOURS_COUNT = 30


# === Master ALgorithm ===

MA_FEATURES_NR_TWEETS_GROUP = 500
MA_FEATURES_NR_FEATURES = 50
MA_ALGS = None

MA_TWEETS_TRAIN = 100
MA_TRAIN_SAVE = True
MA_TWEETS_PREDICT = 10
MA_PREDICT_LOAD = True

MA_DECISION = 'average'

