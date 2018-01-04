from mining.algorithms.mlearning.classifiers.MasterAlgorithm import MasterAlgorithm
from settings import *
from dbm import create_db, clear_db


def init():
    alg = MasterAlgorithm()
    alg.setup()
    return alg

if __name__ == "__main__":
    try:
        create_db()
        print("\n"
              "1-train\n"
              "2-predict\n"
              "3-predict using config file\n"
              "4-train & predict\n"
              "5-train & predict using config file\n"
              "6-clear results\n"
              "7-exit\n"
        )
        choice = raw_input("Choose an option: ")
        if choice=="1":
            init().train()
        elif choice=="2":
            init().predict(load=True)
        elif choice=="3":
            init().predict_by_config(load=True)
        elif choice=="4":
            alg = init()
            alg.train()
            alg.predict()
        elif choice == "5":
            alg = init()
            alg.train()
            alg.predict_by_config()
        elif choice=="6":
            clean_dirs()
        else:
            clear_db()
    except (KeyboardInterrupt) as e:
        clear_db()
        raise KeyboardInterrupt("Process ended by Keyboard Interrupt")