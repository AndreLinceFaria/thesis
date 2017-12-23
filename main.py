from mining.algorithms.mlearning.classifiers.MasterAlgorithm import MasterAlgorithm
from settings import *
from dbm import create_db, clear_db

alg = None
def init():
    alg = MasterAlgorithm()
    alg.setup()

if __name__ == "__main__":
    try:
        create_db()
        print("\n1-train\n2-predict\n3-train & predict\n4-clear results\n5-end\n")
        choice = raw_input("your choice: ")
        if choice=="1":
            init()
            alg.train()
        elif choice=="2":
            init()
            alg.predict()
        elif choice=="3":
            init()
            alg.train()
            alg.predict()
        elif choice=="4":
            clean_dirs()
        else:
            clear_db()
    except (KeyboardInterrupt) as e:
        clear_db()
        raise KeyboardInterrupt("Process ended by Keyboard Interrupt")