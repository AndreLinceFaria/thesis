import logging

def get_log(name, file,level=logging.INFO, file_log=True, global_log=None):
    logger = logging.getLogger(name)
    logger.setLevel(level)

    #logging formatter
    formatter = logging.Formatter('%(asctime)s: %(message)s ', "%Y-%m-%d %H:%M:%S")

    consoleHandler = logging.StreamHandler()
    consoleHandler.setLevel(level)
    consoleHandler.setFormatter(formatter)
    logger.addHandler(consoleHandler)

    if file_log:
        fileHandler = logging.FileHandler(file)
        fileHandler.setLevel(level)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    if global_log != None:
        fileHandler = logging.FileHandler(global_log)
        fileHandler.setLevel(level)
        fileHandler.setFormatter(formatter)
        logger.addHandler(fileHandler)

    return logger