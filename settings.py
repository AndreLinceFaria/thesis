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
    fu.remove_from_dir(CLASS_LOGS_DIR,".gitkeep")
    fu.remove_from_dir(CLASS_MODELS_DIR,".gitkeep")
    fu.remove_from_dir(FIGURES_DIR,".gitkeep")
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
PARTIES_TWITTER_JSON = join(BASE_DIR,"static/config/parties-config/parties-twitter-cfg-1.json")

# === User input Configs ===

USER_INPUT_CONFIG_JSON = join(BASE_DIR,"static/config/input-configs/input-cfg-template.json")

FROM_USERS_FILE = True
USERS_FILE = join(BASE_DIR,"static/config/input-configs/users.txt")

# ======================
# Algorithms
# ======================

GET_MATCHES = False

FEATURE_STEMMING = False
FEATURE_SYNSET = False # not configured

REMOVE_LIMITS = True
LIMITS_PERCENTAGE = 0.1

# === RAKE ===
RAKE_ACTIVE = True
#RAKE_RANDOM_CHOICE = False # -> mix between Rake ACTIVE/NON ACTIVE
TIMEOUT_RAKE = 30
CANDIDATE_THRESHOLD = 100
CANDIDATES_TO_DISCARD = 0.3
REGEX_FILE = join(BASE_DIR,"static/config/rake/regex.txt")
STOPWORDS_FILES = [join(BASE_DIR,"static/config/rake/stopwords-pt.txt"),
                   join(BASE_DIR,"static/config/rake/stopwords-en.txt")]

SUPPRESS_WARNINGS = True
# === KNN ===

KNN_NAME = "K-Nearest Neighbours"
KNN_INITIALS = "KNN"
KNN_NEIGHBOURS_COUNT = 7
KNN_FNAME = None

# === NBayes ===

NB_NAME = "Naive Bayes"
NB_INITIALS = "NB"
NB_FNAME = None
# === NNet ===

NN_NAME = "Multi-Layer Perceptron"
NN_INITIALS = "MLP"
NN_SOLVER = 'lbfgs' #sgd
NN_ALPHA = 1e-5
NN_HIDDEN_LAYERS_SIZE = (7,4)
NN_RANDOM_STATE = 1
NN_ACTIVATION = 'relu'
NN_FNAME = None

# === SVM ===

SVM_NAME = "Support Vector Machine"
SVM_INITIALS = "SVM"
SVM_SVC_RANDOM_STATE = 0
SVM_SVC_KERNEL = 'rbf'
SVM_NEIGHBOURS_COUNT = 30
SVM_FNAME = None

# === LR (Mult) ===

LR_NAME = "Multinomial Logistic Regression"
LR_INITIALS = "MLR"
LR_FNAME = None
# === Master ALgorithm ===

MA_FEATURES_NR_TWEETS_GROUP = 100
MA_FEATURES_NR_FEATURES = 100
MA_ALGS = None

MA_TWEETS_TRAIN = 200
MA_TRAIN_SAVE = True
MA_TRAIN_LOAD_PREV = False
MA_TWEETS_PREDICT = 36
MA_PREDICT_LOAD = True

MA_DECISION = 'weighted'

COUNT_BY_USER = True

# === Stratified KF ===

SKF_N_SPLITS = 5
SKF_SHUFFLE = True