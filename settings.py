import sys,os
sys.path.insert(0, str(os.path.realpath(__file__)))
import datetime
import utils.log as log
import utils.file_utils as fu

# ======================
# Functions
# ======================

def join(path1,path2):
    return str(os.path.join(path1,path2))

def clean_dirs():
    fu.remove_from_dir(CLASS_LOGS_DIR)
    fu.remove_from_dir(CLASS_MODELS_DIR)
    fu.remove_from_dir(FIGURES_DIR)
# ======================
# Files and Directories
# ======================

CLEAN_DIRS = False

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DB = os.path.join(BASE_DIR,"database.sqlite")

CLASS_MODELS_DIR = os.path.join(BASE_DIR,"static/results/models/")

CLASS_LOGS_DIR = os.path.join(BASE_DIR,"static/results/logs/")

FIGURES_DIR = join(BASE_DIR,"static/results/figures/")

if CLEAN_DIRS:
    clean_dirs()

# === Figures ===

FIGURES_SAVE_AS_FORMAT = "[" + datetime.datetime.today().strftime('%Y-%m-%d %H-%M') + "].png"

# === Logs ===

PREDICT_LOG_FORMAT = 'predict-log[' + datetime.datetime.today().strftime('%Y-%m-%d') + '].log'
TRAIN_LOG_FORMAT = 'train-log[' + datetime.datetime.today().strftime('%Y-%m-%d') + '].log'
MAIN_LOG_FORMAT = 'main-log[' + datetime.datetime.today().strftime('%Y-%m-%d') + '].log'
GLOBAL_LOG_FORMAT = 'global-log[' + datetime.datetime.today().strftime('%Y-%m-%d') + '].log'
GLOBAL_LOG = join(CLASS_LOGS_DIR,GLOBAL_LOG_FORMAT)

logtr = log.get_log('train_log',join(CLASS_LOGS_DIR,TRAIN_LOG_FORMAT),global_log=GLOBAL_LOG)
logts = log.get_log('predict_log',join(CLASS_LOGS_DIR,PREDICT_LOG_FORMAT), global_log=GLOBAL_LOG)
logm = log.get_log('main_log',join(CLASS_LOGS_DIR,MAIN_LOG_FORMAT),global_log=GLOBAL_LOG)

# === Parsers & Configs ===

CONFIG_1_JSON = join(BASE_DIR,"static/config/parties-config/parties-config-1.json")
RESULTS_CSV =join(BASE_DIR,"static/config/autarquicas17-resultados.csv")
PARTIES_TWITTER_JSON = join(BASE_DIR,"static/config/parties-config/parties-twitter.json")

# ======================
# Algorithms
# ======================

FEATURE_STEMMING = False
FEATURE_SYNSET = False # not configured

REMOVE_LIMITS = True
LIMITS_PERCENTAGE = 0.1

# === RAKE ===
TIMEOUT_RAKE = 30
CANDIDATE_THRESHOLD = 100
CANDIDATES_TO_DISCARD = 0.3
REGEX_FILE = join(BASE_DIR,"static/config/rake/regex.txt")
STOPWORDS_FILES = [join(BASE_DIR,"static/config/rake/stopwords-pt.txt"),
                   join(BASE_DIR,"static/config/rake/stopwords-en.txt")]

# === KNN ===

KNN_NAME = "K-Nearest Neighbours"

KNN_NEIGHBOURS_COUNT = 7


# === NBayes ===

NB_NAME = "Naive Bayes"

# === NNet ===

NN_NAME = "Multi-Layer Perceptron"
NN_SOLVER = 'lbfgs' #sgd
NN_ALPHA = 1e-5
NN_HIDDEN_LAYERS_SIZE = (7,4)
NN_RANDOM_STATE = 1
NN_ACTIVATION = 'relu'

# === SVM ===

SVM_NAME = "Support Vector Machine"
SVM_SVC_RANDOM_STATE = 0
SVM_SVC_KERNEL = 'rbf'
SVM_NEIGHBOURS_COUNT = 30

# === LR (Mult) ===

LR_NAME = "Multinomial Logistic Regression"

# === Master ALgorithm ===

MA_FEATURES_NR_TWEETS_GROUP = 80
MA_FEATURES_NR_FEATURES = 100
MA_ALGS = None

MA_TWEETS_TRAIN = 200
MA_TRAIN_SAVE = True
MA_TRAIN_LOAD_PREV = False
MA_TWEETS_PREDICT = 1000
MA_PREDICT_LOAD = True

MA_DECISION = 'weighted'

COUNT_BY_USER = True

# === Stratified KF ===

SKF_N_SPLITS = 5
SKF_SHUFFLE = True