import sys,os
sys.path.insert(0, str(os.path.realpath(__file__)))

import datetime

# Files and Directories

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

DB_DIR = os.path.join(BASE_DIR,"database.sqlite")

CLASS_MODELS_DIR = os.path.join(BASE_DIR,"mining/algorithms/mlearning/models/")

CLASS_LOGS_DIR = os.path.join(BASE_DIR,"mining/algorithms/mlearning/logs/")

# Functions

def join(path1,path2):
    return str(os.path.join(path1,path2))

# Logs

#LOGS_DIR =
PREDICT_LOG_FORMAT = 'predict-log[' + datetime.datetime.today().strftime('%Y-%m-%d') + '].log'
TRAIN_LOG_FORMAT = 'predict-log[' + datetime.datetime.today().strftime('%Y-%m-%d') + '].log'